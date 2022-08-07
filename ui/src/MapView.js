import React from "react";
import { MapContainer, TileLayer, useMap } from 'react-leaflet';
import { useParams } from 'react-router-dom';
import axios from 'axios';

const SetCenter = () => {
  const map = useMap();
  var center = map.unproject([400, 250], 13);
  map.setView(center, 13);
  return null
}

const MapInterface = () => {
  var url = new URL(process.env.PUBLIC_URL);
  let { uid } = useParams();
  return(
    <MapContainer zoom={13} scrollWheelZoom={false}>
      <TileLayer
        url={url.href + "/api/map/tile/" + uid + "/{z}/{x}/{y}"}
      />
      <SetCenter />
    </MapContainer>
  );
}

class MapView extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      query: "",
    }
    this.handleSubmit = this.handleSubmit.bind(this);
  }
  handleSubmit(e) {
    var url = window.location.pathname;
    var ind = url.lastIndexOf("/");
    var uid = url.substring(ind + 1);

    const request = axios({
      method: 'POST',
      url: `${process.env.PUBLIC_URL}/api/query/execute/`,
      data: {
        query: this.state.query,
        uid: uid
      }
    });
    request.then(
      response => {
        window.location.href = process.env.PUBLIC_URL;
      }, err => {
      }
    );
  }
  render() {
    return (
      <div>
        <textarea rows="10" placeholder="Enter Query" value={this.state.query} onChange={e => this.setState({query: e.target.value})}/>
        <button onClick={this.handleSubmit} >
          Execute Query
        </button>
        <MapInterface />
      </div>
    );
  }
}

export default MapView;
