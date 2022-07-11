import { MapContainer, TileLayer, useMap } from 'react-leaflet';
import { useParams } from 'react-router-dom';

const SetCenter = () => {
  const map = useMap();
  var center = map.unproject([400, 250], 13);
  map.setView(center, 13);
  return null
}


const MapView = () => {
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



export default MapView;
