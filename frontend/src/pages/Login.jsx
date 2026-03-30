import { useState } from "react";
import { useNavigate } from "react-router-dom";
import API from "../api/api";

function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleLogin = async () => {
  try {
    const formData = new URLSearchParams();
    formData.append("username", username); // ✅ FIXED
    formData.append("password", password);

    const res = await API.post("/auth/login", formData, {
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
    });

    console.log("SUCCESS:", res.data);
    localStorage.setItem("token", res.data.access_token);

    alert("Login success");
    navigate("/dashboard"); // optional
  } catch (err) {
    console.log("FULL ERROR:", err);
    console.log("DATA:", err.response?.data);
    console.log("STATUS:", err.response?.status);

    alert("Login failed");
  }
};
  return (
    <div>
      <h2>Login</h2>
      <input placeholder="Username" onChange={(e) => setUsername(e.target.value)} />
      <input placeholder="Password" type="password" onChange={(e) => setPassword(e.target.value)} />
      <button onClick={handleLogin}>Login</button>
    </div>
  );
}

export default Login;