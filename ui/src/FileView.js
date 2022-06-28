import React from "react";
import axios from "axios";
import { FaTrash } from 'react-icons/fa';

class FileView extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      items: [],
      selectedFile: null
    };
    this.getFiles = this.getFiles.bind(this);
    this.onUploadFileSubmit = this.onUploadFileSubmit.bind(this);
    this.onUploadFileChange = this.onUploadFileChange.bind(this);
    this.deleteFile = this.deleteFile.bind(this);
  }
  componentDidMount() {
    this.getFiles();
  }
  getFiles() {
    const request = axios({
      method: "GET",
      url: `${process.env.PUBLIC_URL}/api/files/list/`
    });
    request.then(
      response => {
        this.setState({
          items: response.data
        });
      }, err => {
      }
    );
  }
  onUploadFileSubmit(e) {
    e.preventDefault();
    const formData = new FormData();
    formData.append("file", this.state.selectedFile);
    formData.append("fileName", this.state.selectedFile.name);
    const request = axios({
      method: "POST",
      url: `${process.env.PUBLIC_URL}/api/files/upload/`,
      data: formData,
      headers: {"content-type": "multipart/form-data"}
    });
    request.then(
      response => {
        this.getFiles();
      }, err => {
      }
    );
  }
  onUploadFileChange(e) {
    this.setState({
      selectedFile: e.target.files[0]
    });
  }
  deleteFile(uid) {
    const formData = new FormData();
    formData.append("uid", uid);
    const request = axios({
      method: "POST",
      url: `${process.env.PUBLIC_URL}/api/files/delete/`,
      data: formData,
    });
    request.then(
      response => {
        this.getFiles();
      }, err => {
      }
    );
  }
  render() {
    let rows;
    rows = this.state.items.map((item, i) => {
      return (
        <tr key={i}>
          <td>
            {item.name}
          </td>
          <td onClick={() => this.deleteFile(item.uid)} >
            <FaTrash size={25} color="#9c9c9c" />
          </td>
        </tr>
      );
    });
    let table;
    table = (
      <table>
        <thead>
          <tr>
            <th>Name</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {rows}
        </tbody>
      </table>
    );
    return (
      <div>
        <form onSubmit={this.onUploadFileSubmit}>
          <input type="file" onChange={this.onUploadFileChange} />
          <button type="submit">{"Upload"}</button>
        </form>
        <div>
          {table}
        </div>
      </div>
    );
  }
}

export default FileView;
