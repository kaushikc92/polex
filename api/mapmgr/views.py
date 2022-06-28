import math, io, os

import pandas as pd
from PIL import Image

from pymongo import MongoClient

def convert_html(uid):
    df = pd.read_csv("{0}/files/{1}.csv".format(settings.MEDIA_ROOT, uid))
    df = df.astype(str).apply(lambda x: x.str[:settings.MAX_CHARS_PER_COLUMN])
    rows_per_image, max_width = get_subtable_dimensions(df)
    os.mkdir("{0}/tiles/{1}".format(settings.MEDIA_ROOT, uid))
    df1 = df[0 : rows_per_image]
    img1 = convert_subtable_html(df1, uid, 0, max_width)
    img2 = None
    if df.shape[0] > rows_per_image:
        df2 = df[rows_per_image : 2 * rows_per_image]
        img2 = convert_subtable_html(df2, uid, 1, max_width)
    img, start_row = create_subtable_image(img1, img2, 0)
    pil_img = Image.fromarray(img)
    subtable_path = "{0}/tiles/{1}/tile_0.jpg".format(settings.MEDIA_ROOT, uid)
    pil_img.save(subtable_path, 'jpeg', quality=60)
    
    mongo_client = MongoClient("mongodb://localhost:27017/")
    db = mongo_client["polex"]
    tiles_collection = db["tiles"]




def convert_subtable_html(df, uid, subtable_number, max_width, results=None):
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


