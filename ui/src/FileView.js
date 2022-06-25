import React from "react";
import axios from "axios";

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
  getFiles() {
    const request = axios({
      method: "GET",
      url: `${process.env.PUBLIC_URL}/api/get-files/`
    });
    request.then(
      response => {
        this.setState({
          items: response.data.files
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
      url: `${process.env.PUBLIC_URL}/api/upload-file/`,
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
  deleteFile() {
  }
  render() {
    return (
      <div>
        <form onSubmit={this.onUploadFileSubmit}>
          <input type="file" onChange={this.onUploadFileChange} />
          <button type="submit">{"Upload"}</button>
        </form>
      </div>
    );
  }
}

export default FileView;
