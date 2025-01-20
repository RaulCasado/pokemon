
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import Header from "./components/Header";
import Home from "./pages/Home";
import SoloMode from "./pages/SoloMode";
import MultiplayerMode from "./pages/MultiplayerMode";

const App = () => {
  return (
    <Router>
      <Header />
      <div className="container mx-auto mt-4">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/solo" element={<SoloMode />} />
          <Route path="/multiplayer" element={<MultiplayerMode />} />
        </Routes>
      </div>
    </Router>
  );
};

export default App;
