import Home from "../features/home/components/Home";
import Results from "../features/results/components/Results";
import "./App.css";
import { Routes, Route } from "react-router-dom";

const App = () => {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/search" element={<Results />} />
    </Routes>
  );
};

export default App;
