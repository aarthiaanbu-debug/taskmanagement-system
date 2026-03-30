import { useEffect, useState } from "react";
import API from "../api/api";
import Navbar from "../components/Navbar";
import { BarChart, Bar, XAxis, YAxis, Tooltip } from "recharts";

function Analytics() {
  const [data, setData] = useState([]);

  const getAnalytics = async () => {
    try {
      const res = await API.get("/analytics");

      // example transform
      const chartData = [
        { name: "Completed", value: res.data.completed },
        { name: "Pending", value: res.data.pending },
      ];

      setData(chartData);
    } catch (err) {
      console.log(err.response?.data);
    }
  };

  useEffect(() => {
    getAnalytics();
  }, []);

  return (
    <div>
      <Navbar />
      <h2>Analytics</h2>

      <BarChart width={400} height={300} data={data}>
        <XAxis dataKey="name" />
        <YAxis />
        <Tooltip />
        <Bar dataKey="value" />
      </BarChart>
    </div>
  );
}

export default Analytics;