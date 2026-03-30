import { useState, useEffect } from "react";
import API from "../api/api";
import Navbar from "../components/Navbar";

function Tasks() {
  const [title, setTitle] = useState("");
  const [desc, setDesc] = useState("");
  const [tasks, setTasks] = useState([]);

  // 🔄 fetch tasks
  const getTasks = async () => {
    try {
      const res = await API.get("/tasks/assigned");
      setTasks(res.data);
    } catch (err) {
      console.log(err);
    }
  };

  useEffect(() => {
    getTasks();
  }, []);

  // ➕ create task
  const createTask = async () => {
    try {
      const payload = {
        title,
        description: desc,
        status: "pending",
        project_id: 1, // ⚠️ make sure project exists
      };

      const res = await API.post("/tasks", payload);

      alert("Task Created ✅");

      setTitle("");
      setDesc("");

      getTasks(); // refresh
    } catch (err) {
      console.log(err.response?.data);
      alert("Create Failed ❌");
    }
  };

  // 👤 assign task
  const assignTask = async (taskId) => {
    try {
      await API.post(`/tasks/${taskId}/assign`, {
        user_id: 1,
      });

      alert("Assigned ✅");
      getTasks();
    } catch (err) {
      console.log(err.response?.data);
    }
  };

  return (
    <div>
      <Navbar />

      <h2>Create Task</h2>

      <input
        placeholder="Title"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
      />

      <input
        placeholder="Description"
        value={desc}
        onChange={(e) => setDesc(e.target.value)}
      />

      <button onClick={createTask}>Create Task</button>

      <h3>Tasks List</h3>

      {tasks.map((task) => (
        <div key={task.id}>
          <p>{task.title} - {task.status}</p>
          <button onClick={() => assignTask(task.id)}>
            Assign
          </button>
        </div>
      ))}
    </div>
  );
}

export default Tasks;