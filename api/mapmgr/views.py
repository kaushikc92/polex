from django.conf import settings

import math, io, os, queue, threading

import pandas as pd
import numpy as np
import imgkit
from PIL import Image

from mapmgr.models import TiledDocument

write_q = queue.Queue()

def convert_html(doc):
    uid = doc.uid
    df = pd.read_csv("{0}/documents/{1}.csv".format(settings.MEDIA_ROOT, uid))
    doc.rows = df.shape[0]
    doc.columns = df.shape[1]
    doc.save()

    df = df.astype(str).apply(lambda x: x.str[:settings.MAX_CHARS_PER_COLUMN])
    rows_per_image, max_width = get_subtable_dimensions(df)
    os.mkdir("{0}/tiles/{1}".format(settings.MEDIA_ROOT, uid))
    df1 = df[0 : rows_per_image]
    img1 = convert_subtable_html(df1, 0, max_width)
    img2 = None
    if df.shape[0] > rows_per_image:
        df2 = df[rows_per_image : 2 * rows_per_image]
        img2 = convert_subtable_html(df2, 1, max_width)
    img, start_row = create_subtable_image(img1, img2, 0)
    pil_img = Image.fromarray(img)
    subtable_path = "{0}/tiles/{1}/tile_0.jpg".format(settings.MEDIA_ROOT, uid)
    pil_img.save(subtable_path, 'jpeg', quality=60)

    add_subtable_entries(doc, 0, [img])

    if img2 is not None:
        t = threading.Thread(target=convert_remaining_html, args=(doc, df, rows_per_image, max_width,
            img2, start_row))
        t.start()

def convert_remaining_html(doc, csv, rows_per_image, max_width, img1, start_row):
    number_of_subtables = math.ceil(df.shape[0] / rows_per_image)
    batch_size = 10
    no_of_batches = math.ceil(number_of_subtables / batch_size)

    num_write_threads = 10
    write_threads = []

    for i in range(num_write_threads):
        w = threading.Thread(target=worker)
        w.start()
        write_threads.append(w)

    for i in range(0, no_of_batches):
        converted_images = [None] * batch_size
        threads = []
        for j in range(0, batch_size):
            subtable_number = batch_size * i + j + 2
            df = csv[subtable_number * rows_per_image: (subtable_number+1) * rows_per_image]
            t = threading.Thread(target=convert_subtable_html, args=(df, j, max_width, converted_images))
            threads.append(t)
            t.start()
        for t in threads:
            t.join()

        subtable_images = []
        for j, img2 in enumerate(converted_images):
            subtable_number = batch_size * i + j + 1
            if start_row == -1:
                if img2 is not None:
                    subtable_images.append(img2)
                break
            img, start_row = create_subtable_image(img1, img2, start_row)
            img1 = img2
            subtable_images.append(img)
            pil_img = Image.fromarray(img)
            subtable_path = "{0}/tiles/{1}/tile_{2}.jpg".format(settings.MEDIA_ROOT, doc.uid, str(subtable_number))
            write_q.put((pil_img, subtable_path))
            add_subtable_entries(doc, batch_size*i, subtable_images)
        write_q.join()

        for i in range(num_write_threads):
            write_q.put(None)
        for w in write_threads:
            w.join()

def worker():
    while True:
        item = write_q.get()
        if item is None:
            break
        write_subtable_image(item[0], item[1])
        write_q.task_done()

def write_subtable_image(pil_img, subtable_path):
    pil_img.save(subtable_path, 'jpeg', quality=60)

def convert_subtable_html(df, subtable_number, max_width, results=None):
    if df.shape[0] == 0:
        return None
    pd.set_option('display.max_colwidth', -1)
    html = df.to_html(index=False, border=1).replace('<td>', '<td style = "word-wrap: break-word;' + 
        ' text-align:center; font-family: Times New Roman; font-size: 18;">')
    html = html.replace('<th>', '<th style = "background-color: #9cd4e2; text-align: center;' + 
        ' font-family: Times New Roman; font-size: 18;">')
    html = html.replace('<table', '<div style="width:' + str(max_width) + 'px;">\n<table ' + 
        'style="border-collapse: collapse;"')
    html = html.replace('</table>', '</table>\n</div>')

    options = {
        'quality' : '60'
    }
    img = Image.open(io.BytesIO(imgkit.from_string(html, False, options=options)))
    img_arr = np.array(img)
    if results is not None:
        results[subtable_number] = img_arr
    else:
        return img_arr

def get_subtable_dimensions(df):
    chars_per_row = 0
    max_lines_per_row = 1
    for col in df.columns:
        max_len = df[col].map(len).max()
        if max_len > 50:
            lines_per_row = math.ceil(max_len / 200)
            max_lines_per_row = max(max_lines_per_row, lines_per_row)
            max_len = 50
        chars_per_row = chars_per_row + max_len
    max_width = chars_per_row * 5
    rows_per_image = math.ceil(400 / max_lines_per_row)
    return rows_per_image, max_width

def create_subtable_image(img1, img2, start_row):
    h1 = img1.shape[0]
    w1 = img1.shape[1]
    max_tile_size = 2 ** 12
    number_of_rows = int(math.ceil((h1 - start_row) / (max_tile_size * 1.0)))
    number_of_cols = int(math.ceil(w1 / (max_tile_size * 1.0)))
    diff = max_tile_size * number_of_rows - h1 + start_row
    if img2 is None:
        img = img1[start_row : h1, :]
        img = pad_img(img, max_tile_size * number_of_rows, max_tile_size * number_of_cols)
        return img, -1
    else:
        h2 = img2.shape[0]
        w2 = img2.shape[1]
        if h2 < diff:
            img = np.full((h1 - start_row + h2, max(w1, w2), 3), 255, dtype=np.uint8)
            img[:h1-start_row, :w1] = img1[start_row:, :]
            img[h1-start_row:,:w2] = img2[:, :]
            img = pad_img(img, max_tile_size * number_of_rows, max_tile_size * number_of_cols)
            return img, -1
        else:
            img = np.full((h1 - start_row + diff, max(w1, w2), 3), 255, dtype=np.uint8)
            img[:h1-start_row, :w1] = img1[start_row:, :]
            img[h1-start_row:,:w2] = img2[:diff, :]
            img = pad_img(img, max_tile_size * number_of_rows, max_tile_size * number_of_cols)
            return img, diff

def pad_img(img, h, w):
    height, width, channels = img.shape
    new_img = np.full((h, w, channels), 221, dtype=np.uint8)
    new_img[0:height, 0:width] = img
    return new_img

def add_subtable_entries(doc, start_st_no, images):
    entries = []
    for i, img in enumerate(images):
        tile_size = 2 ** 12
        nrows = int(math.ceil(img.shape[0]/tile_size)) * (2 ** 4) 
        ncols = int(math.ceil(img.shape[1]/tile_size)) * (2 ** 4)
        entries.append(TiledDocument(document=doc, subtable_number=start_st_no+i,
            tile_count_on_x=ncols, tile_count_on_y=nrows, total_tile_count=ncols*nrows))
    TiledDocument.objects.bulk_create(entries)
