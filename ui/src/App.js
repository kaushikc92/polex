import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import "./App.css";
import MapView from "./MapView";
import FileView from "./FileView";

class App extends React.Component {
  render() {
    var url = new URL(process.env.PUBLIC_URL);
    let router;
    router = (
      <Router basename={url.pathname} >
        <Routes>
          <Route 
            path="/map/:uid"
            element={<MapView />}
          />
          <Route
            path="/"
            element={<FileView />}
          />
        </Routes>
      </Router>
    );
    return router
  }
}


export default App;
