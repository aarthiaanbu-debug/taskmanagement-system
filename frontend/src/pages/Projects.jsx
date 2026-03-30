import { useEffect, useState } from "react";
import API from "../api/api";
import Navbar from "../components/Navbar";

function Projects() {
  const [projects, setProjects] = useState([]);
  const [name, setName] = useState("");

  const fetchProjects = () => {
    API.get("/projects")
      .then((res) => setProjects(res.data))
      .catch((err) => console.log(err));
  };

  useEffect(() => {
    fetchProjects();
  }, []);

  const createProject = async () => {
    try {
      await API.post("/projects", { name });
      setName("");
      fetchProjects(); // refresh list
    } catch (err) {
      console.log(err);
    }
  };

  return (
    <div>
      <Navbar />
      <h2>Projects</h2>

      <input
        placeholder="Project Name"
        value={name}
        onChange={(e) => setName(e.target.value)}
      />
      <button onClick={createProject}>Create</button>

      {projects.map((p) => (
        <div key={p.id}>{p.name}</div>
      ))}
    </div>
  );
}

export default Projects;