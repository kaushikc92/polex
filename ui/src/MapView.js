import { MapContainer, TileLayer } from 'react-leaflet';
import { useParams } from 'react-router-dom';

const MapView = () => {
  var url = new URL(process.env.PUBLIC_URL);
  let { uid } = useParams();
  return(
    <MapContainer center={[0.0, 0.0]} zoom={13} scrollWheelZoom={false}>
      <TileLayer
        url={url.href + "/api/map/tile/" + uid + "/{z}/{x}/{y}"}
      />
    </MapContainer>
  );
}



export default MapView;
