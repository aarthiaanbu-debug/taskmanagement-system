# 🚀 Task Management System

A full-stack **Task Management and Collaboration System** built using **FastAPI (Backend)** and **React (Frontend)**.

---

## 📌 Features

### 🔐 Authentication

* User Registration
* User Login (JWT Token)

### 📁 Project Management

* Create Projects
* View Projects

### ✅ Task Management

* Create Tasks
* Assign Tasks to Users
* Track Task Status (Pending / Completed)

### 🔔 Notifications

* Get notifications when a task is assigned

### 📊 Analytics

* View task statistics (Completed vs Pending)

---

## 🛠️ Tech Stack

### Backend

* FastAPI
* SQLAlchemy
* SQLite
* JWT Authentication

### Frontend

* React (Vite)
* Axios
* React Router
* Recharts

---

## 📂 Project Structure

```
taskmanagement/
├── backend/
│   ├── app/
│   └── main.py
├── frontend/
│   ├── src/
│   └── package.json
└── README.md
```

---

## ⚙️ Setup Instructions

### 🔧 Backend Setup

```bash
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --port 8001
```

👉 Backend runs on: http://127.0.0.1:8001

---

### 💻 Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

👉 Frontend runs on: http://localhost:5173

---

## 🔑 Demo Login Credentials

Use the following credentials to test the application:

```
Email: aarthia@gmail.com
Password: Aar12
```

---

## 🔗 API Documentation

Swagger UI available at:

👉 http://127.0.0.1:8001/docs

---

## 📸 Screens Included

* Login Page
* Dashboard
* Projects Page
* Tasks Page
* Notifications
* Analytics Charts

---

If you like this project, give it a ⭐ on GitHub!
