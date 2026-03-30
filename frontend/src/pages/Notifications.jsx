import { useEffect, useState } from "react";
import API from "../api/api";
import Navbar from "../components/Navbar";

function Notifications() {
  const [notes, setNotes] = useState([]);

  const getNotifications = async () => {
    try {
      const res = await API.get("/notifications");
      setNotes(res.data);
    } catch (err) {
      console.log(err);
    }
  };

  useEffect(() => {
    getNotifications();
  }, []);

  return (
    <div>
      <Navbar />
      <h2>Notifications</h2>

      {notes.map((n) => (
        <p key={n.id}>{n.message}</p>
      ))}
    </div>
  );
}

export default Notifications;