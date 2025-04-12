# LoadMonitor

**LoadMonitor** is a lightweight web-based application designed to monitor and visualize system load in real-time. It leverages Python for backend logic and HTML for the frontend interface, making it simple yet effective for basic performance monitoring needs.

## Features

- 🔁 Real-time system load monitoring
- 🌐 Web-based interface using HTML
- ⚙️ Backend powered by Python
- 📂 Clear separation between client and server components

## Project Structure

```
LoadMonitor/
├── server/
│   ├── app.py             # Main server application
│   ├── database.py        # Database models
│   ├── config.py          # Server configuration
│   └── templates/
│       └── dashboard.html # Dashboard interface
└── client/
    ├── monitor.py         # Resource monitoring script
    ├── config.py          # Client configuration
```


## Getting Started

### Prerequisites

- Python 3.x installed on your system
- Web browser to access the frontend

### How to Run

## Setup Instructions

Follow these steps to set up both the server and client components of LoadMonitor.

---

## 🔧 Server Setup

1. **Install dependencies:**

   Open a terminal and run the following command to install the necessary Python dependencies:

   ```bash
   pip install -r server/requirements.txt
   ```

2. **Initialize the database:**

   Set up the database by running the following commands:

   ```bash
   flask db init
   flask db migrate
   flask db upgrade
   ```

3. **Run the server:**

   Start the server with the following command:

   ```bash
   flask run --host=0.0.0.0 --port=5000
   ```

   The server will now be accessible at `http://localhost:5000`.

---

## 💻 Client Setup

1. **Install dependencies:**

   Install the required dependencies for the client by running:

   ```bash
   pip install -r client/requirements.txt
   ```

2. **Configure the client:**

   Edit the configuration file located at `client/config.py` and make any necessary changes.

3. **Run the monitor:**

   Start the monitor by running the following command:

   ```bash
   python monitor.py
   ```

---

Now your LoadMonitor system should be up and running! 🎉
```

This is the **proper Markdown** for your setup instructions. You can copy and paste this into your `README.md` file directly.

1. **Clone the Repository**

   ```bash
   git clone https://github.com/0marWaleed/LoadMonitor.git
   cd LoadMonitor
