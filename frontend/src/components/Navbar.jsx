import { Link } from "react-router-dom";

function Navbar() {
  return (
    <div style={{ padding: "10px", background: "#eee" }}>
      <Link to="/dashboard">Dashboard</Link> |{" "}
      <Link to="/projects">Projects</Link> |{" "}
      <Link to="/tasks">Tasks</Link> |{" "}
      <Link to="/notifications">Notifications</Link> |{" "}
      <Link to="/analytics">Analytics</Link>
    </div>
  );
}

export default Navbar;