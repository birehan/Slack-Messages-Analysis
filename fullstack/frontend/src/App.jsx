import "./App.css";
import CreateUser from "./pages/CreateUser";
import Home from "./pages/Home";
import { Route, Routes, useLocation } from "react-router-dom";
import UpdateUser from "./pages/UpdateUser"; // Import the UpdateUser component

function App() {
  return (
    <>
      <div>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/create-user" element={<CreateUser />} />
          <Route path="/update-user/:userId" element={<UpdateUser />} />{" "}
          {/* Add the UpdateUser route with a dynamic parameter */}
        </Routes>
      </div>
    </>
  );
}

export default App;
