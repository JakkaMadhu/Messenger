# 📢 Messenger — Real-Time Chat Application

[![Python Version](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Database](https://img.shields.io/badge/Database-MongoDB%20Atlas-green?logo=mongodb&logoColor=white)](https://www.mongodb.com/cloud/atlas)
[![Host](https://img.shields.io/badge/Hosting-Railway-black?logo=railway&logoColor=white)](https://railway.app/)
[![Email Service](https://img.shields.io/badge/Email-Resend%20SDK-purple)](https://resend.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A premium, modular full-stack client-server chat application featuring a Tkinter-based dark theme, MongoDB persistence, secure email OTP validation, timezone-aware dynamic chat separators, and background sliding notifications. 

This repository contains both the desktop client application and the backend socket server daemon.

---

## 🚀 Live Demo (Single-Click Executable)

Skip the local configuration! You can run and test the application immediately on Windows:

1. 📥 **[Download the Standalone Executable (messenger.exe)](https://github.com/JakkaMadhu/Messenger/releases/latest/download/messenger.exe)**
2. ⚡ Double-click **`messenger.exe`** to start chatting!

> [!NOTE]
> The executable is pre-configured to automatically default to our live socket server hosted 24/7 on Railway (`zephyr.proxy.rlwy.net:28364`). You can launch multiple instances of the executable to test real-time chat between different accounts. No local configuration or `.env` files are required!

---

## ✨ Key Features

* **Real-time Messaging**: Multi-threaded TCP socket communication enabling direct private chats and broadcast routing, handled in [client.py](file:///c:/Coding/projects/Messenger/client/client.py) and [server.py](file:///c:/Coding/projects/Messenger/server/server.py).
* **Modern Dark UI**: Elegant dark mode palette, Segoe UI typography, custom styled input fields, inline password visibility toggles, and customized focus layouts located in [ui_screens.py](file:///c:/Coding/projects/Messenger/client/ui_screens.py).
* **Resend API Integration**: Lightning-fast registration and password recovery validated by OTP codes dispatched over HTTPS using the official **Resend SDK** in [utils.py](file:///c:/Coding/projects/Messenger/server/utils.py). This bypasses traditional SMTP blocking issues on cloud platforms.
* **Database Caching**: MongoDB database with compound index query optimizations and TTL (Time-to-Live) indexes for automated OTP code expiration, configured in [database.py](file:///c:/Coding/projects/Messenger/server/database.py).
* **Unread Notification Badges**: Sidebar badge updates displaying the number of unread messages per contact.
* **Sliding Toast Alerts**: Smooth animation slide-downs notifying users of background incoming messages, implemented in [toast.py](file:///c:/Coding/projects/Messenger/client/toast.py).
* **Dynamic Timestamps**: Timezone-aware date separators (e.g. `Today`, `Yesterday`, `Month Day, Year`) inside scrollable bubbles, using helper functions in [utils.py](file:///c:/Coding/projects/Messenger/client/utils.py).
* **Professional Logging**: Replaced print statements with standard Python `logging` to stream structured logs directly to console output. This integrates perfectly with cloud dashboard monitoring (e.g., Railway logs).

---

## 🏗 System Architecture

The application is structured using an **MVC (Model-View-Controller)** pattern on the client side, communicating over raw TCP JSON sockets to a multithreaded daemon server:

```mermaid
graph TD
    subgraph Client App [Client MVC Architecture]
        M["messenger.py (Controller)"] --> V["ui_screens.py (Views)"]
        M --> C["client.py (Network Listener)"]
        M --> T["toast.py (Notifications)"]
        M --> U1["utils.py (Formatting)"]
    end
    
    subgraph Server Backend [Server daemon]
        S["server.py (Main Daemon)"] --> CM["client_manager.py (Registry)"]
        S --> H["handlers.py (Request Router)"]
        H --> DB["database.py (MongoDB Wrapper)"]
        H --> U2["utils.py (Resend SDK Dispatcher)"]
    end
    
    C <--> |TCP JSON Sockets| S
```

---

## 🛠 Directory Structure

```bash
Messenger/
├── client/
│   ├── .env.example       # Example client environment variables
│   ├── client.py          # Network socket listener thread class (Client)
│   ├── config.py          # Colors, fonts, and default server connection settings
│   ├── icon.ico           # Application window & binary file icon
│   ├── messenger.py       # Main App controller class (App)
│   ├── messenger.spec     # PyInstaller compilation specification file
│   ├── requirements.txt   # Client package dependencies (dotenv, pillow)
│   ├── toast.py           # Slide-in toast notification animation class (ToastNotification)
│   ├── ui_screens.py      # Tkinter views (LoginScreen, RegistrationScreen, etc.)
│   └── utils.py           # Datetime parsing and formatting utility functions
├── server/
│   ├── .env.example       # Example server environment variables
│   ├── client_manager.py  # Thread-safe socket registry manager class (ClientManager)
│   ├── config.py          # Port configs and MongoDB URI
│   ├── database.py        # MongoDB database connections and queries wrapper class (Database)
│   ├── handlers.py        # Client actions request router (handle_client)
│   ├── requirements.txt   # Server package dependencies (resend, pymongo, python-dotenv)
│   ├── server.py          # Main TCP socket port listener
│   └── utils.py           # Email verification and Resend SDK dispatcher
└── .gitignore             # Git exclusion rules
```

---

## 📥 Setup & Installation

If you prefer to run the codebase locally rather than using the pre-compiled `.exe` file:

### 1. Prerequisites
* **Python 3.8+** installed on your system.
* **MongoDB Server** installed and running locally or in the cloud.

### 2. Setting Up Virtual Environments & Dependencies

#### ⚙️ Server Setup:
```bash
# Navigate to server directory
cd server

# Create and activate virtual environment
python -m venv .venv
# On Windows (PowerShell):
.venv\Scripts\Activate.ps1
# On Windows (CMD):
.venv\Scripts\activate.bat
# On macOS/Linux:
source .venv/bin/activate

# Install server dependencies
pip install -r requirements.txt

# Return to root directory
cd ..
```

#### 🖥️ Client Setup:
```bash
# Navigate to client directory
cd client

# Create and activate virtual environment
python -m venv .venv
# On Windows (PowerShell):
.venv\Scripts\Activate.ps1
# On Windows (CMD):
.venv\Scripts\activate.bat
# On macOS/Linux:
source .venv/bin/activate

# Install client dependencies
pip install -r requirements.txt

# Return to root directory
cd ..
```

---

## 🔒 Environment Configuration

Create a `.env` file in both `client/` and `server/` directories based on the provided configuration outlines:

### Server Environment (`server/.env`)
```ini
# Transactional Email configuration (Resend API Key)
RESEND_API_KEY="re_your_resend_api_key"

# Port and address bindings
IP_ADDRESS="0.0.0.0"
PORT_NUMBER="45999"

# MongoDB Database Connection Configuration
# Option A (Recommended): Granular config variables (passwords URL-encoded automatically)
MONGODB_USER="username"
MONGODB_PASSWORD="your_raw_password"
MONGODB_HOST="cluster.mongodb.net"
MONGODB_DB_NAME="db_messenger"
MONGODB_APP_NAME="Messenger"

# Option B: Single MongoDB connection URI fallback
# MONGODB_URI="mongodb://username:password@127.0.0.1:27017/db_messenger?authSource=db_messenger"
```

> [!WARNING]
> Never commit actual `.env` files containing your API keys or database passwords to public repositories.

### Client Environment (`client/.env` - Optional)
```ini
# Address and port of the active chat server (defaults to production if omitted)
IP_ADDRESS=zephyr.proxy.rlwy.net
PORT_NUMBER=28364
```

---

## 🚦 Running the Application

### Option A: Standard Manual Running

1. **Start MongoDB**: Ensure your local or cloud MongoDB instance is active.
2. **Start the Server**:
   Navigate to the `server/` directory, activate the virtual environment, and run:
   ```bash
   python server.py
   ```
3. **Start the Client(s)**:
   Navigate to the `client/` directory, activate the virtual environment, and run:
   ```bash
   python messenger.py
   ```
   *(You can launch multiple client instances to test messaging between different accounts).*

---

### Option B: Docker Compose (Server & Database Stack)

You can launch the entire server infrastructure (MongoDB database and the TCP Chat Server) headlessly in isolated containers:

1. **Navigate to server directory**:
   ```bash
   cd server
   ```
2. **Configure Environment**: Ensure your `server/.env` is configured with your database and email credentials.
3. **Launch Stack**: From the `server/` directory, run:
   ```bash
   docker-compose up --build -d
   ```
   *This builds the server image, downloads MongoDB, maps port `45999`, and runs the services headlessly in the background.*
4. **Shutdown Stack**:
   To stop and remove the server infrastructure, run:
   ```bash
   docker-compose down
   ```

---

### Option C: Docker Compose (GUI Client Container)

To run the Tkinter GUI client inside a Docker container (separately from the server stack), you must configure display forwarding to your host display system:

#### 1. Install & Configure X-server on Host (Windows):
1. Download and install [VcXsrv (Windows X Server)](https://sourceforge.net/projects/vcxsrv/).
2. Run **XLaunch** from your Start menu and choose these options:
   * **Display settings**: Choose **Multiple windows** and set **Display number** to `0`.
   * **Client startup**: Choose **Start no client**.
   * **Extra settings**: Check **Disable access control** (crucial to allow connections from Docker).
3. Click Finish to start the server.

#### 2. Run the Client Container:
Make sure your server is running (either locally or via Option B above), then navigate to the `client/` directory and run:
```bash
# Navigate to client directory
cd client

# Build and run the client GUI container
docker-compose up --build
```
*The client GUI will automatically forward its screen and pop up on your host Windows desktop!*

#### 3. Run Additional Client Instances:
To open a second client container instance to test chatting, run:
```bash
docker-compose run client
```

#### 4. Shutdown Client Containers:
To stop client containers, run:
```bash
docker-compose down
```

---

## 🌐 Cloud Deployment (Railway.app)

The TCP Socket Server is designed to host on **Railway** (which supports raw TCP port exposure).

### 1. Deploy the Server
1. Sign up/log in to [Railway.app](https://railway.app/).
2. Create a **New Project** -> **Deploy from GitHub repo** -> Select your `Messenger` repository.
3. In the Railway service settings for the server:
   * **Build/Start Command**: Railway will use the `Dockerfile` inside the `server` directory to build and run the daemon automatically.
   * **TCP Port**: Under your service's settings page, add a new **TCP Port** mapping. Railway will expose a public host (e.g. `zephyr.proxy.rlwy.net`) and a public port (e.g. `28364`).
   * **Environment Variables**: Add your production credentials:
     * `MONGODB_USER`
     * `MONGODB_PASSWORD`
     * `MONGODB_HOST`
     * `MONGODB_DB_NAME`
     * `MONGODB_APP_NAME`
     * `RESEND_API_KEY` (For OTP verification emails)

### 2. Live Logs
Because the server utilizes standard console logging (`StreamHandler`), you can view structured real-time activity and errors by going to the **Logs** tab of your service in the Railway dashboard.

---

## 📦 Packaging the Client (PyInstaller)

If you modify the client code and want to recompile the standalone single-file executable:

1. **Activate the client virtual environment & install packaging dependencies:**
   ```bash
   cd client
   # Activate your virtual environment (.venv)
   pip install pyinstaller pillow python-dotenv
   ```

2. **Rebuild the executable using the spec file:**
   ```bash
   pyinstaller --clean messenger.spec
   ```
   *PyInstaller will read the `messenger.spec` configuration to compile all Python modules, resource files (like the custom `icon.ico` layout), and compile everything into a single standalone executable at `client/dist/messenger.exe`.*

---

## 📄 License
Distributed under the **MIT License**. See `LICENSE` for details.
