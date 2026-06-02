# 📢 Messenger — Real-Time Chat Application

A premium, modular full-stack client-server chat application featuring a Tkinter-based dark theme, MongoDB persistence, secure email OTP validation, timezone-aware dynamic chat separators, and background sliding notifications.

This repository contains both the desktop client application and the backend socket server daemon.

---

## 🚀 Live Demo (Run instantly in 1-Click)

Skip the local configuration! You can run and test the application immediately on Windows:

1. 📥 **[Download the pre-packaged Live Demo (.zip)](https://github.com/JakkaMadhu/Messenger/releases/latest/download/Messenger-Demo.zip)**
2. 📂 **Extract** the downloaded `.zip` archive.
3. ⚡ Double-click **`messenger.exe`** to start chatting!

> [!NOTE]
> The executable is pre-configured via the included `.env` file to connect to our live socket server hosted 24/7 on Railway (`zephyr.proxy.rlwy.net:28364`). You can launch multiple instances of the app to test real-time chat between accounts.


---

## 🚀 Key Features

* **Real-time Messaging**: Multi-threaded socket communication enabling direct private chats and broadcast routing, handled in [client.py](file:///c:/Coding/projects/Messenger/client/client.py) and [server.py](file:///c:/Coding/projects/Messenger/server/server.py).
* **Modern Dark UI**: Segoe UI typography, sleek visual containers, inline password toggles, and customized focus layouts located in [ui_screens.py](file:///c:/Coding/projects/Messenger/client/ui_screens.py).
* **OTP Verification**: Secure registration and password recovery validated by SMTP-dispatched OTP codes, processed by [utils.py](file:///c:/Coding/projects/Messenger/server/utils.py) and [handlers.py](file:///c:/Coding/projects/Messenger/server/handlers.py).
* **Database Caching**: MongoDB database with compound index query optimizations and TTL (Time-to-Live) indexes for automated OTP code expiration, configured in [database.py](file:///c:/Coding/projects/Messenger/server/database.py).
* **Unread Notification Badges**: Sidebar badge updates displaying the number of unread messages per contact.
* **Sliding Toast Alerts**: Smooth animation slide-downs notifying users of background incoming messages, implemented in [toast.py](file:///c:/Coding/projects/Messenger/client/toast.py).
* **Dynamic Timestamps**: Timezone-aware date separators (e.g. `Today`, `Yesterday`, `Month Day, Year`) inside scrollable bubbles, using helper functions in [utils.py](file:///c:/Coding/projects/Messenger/client/utils.py).
* **Highly Modular Design**: Clean architecture separating configuration, networking, views, and controllers.

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
        H --> U2["utils.py (SMTP Dispatcher)"]
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
│   ├── config.py          # Colors, fonts, and dynamic path load configurations
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
│   ├── requirements.txt   # Server package dependencies
│   ├── server.py          # Main TCP socket port listener
│   └── utils.py           # Email verification and SMTP dispatcher
└── .gitignore             # Git exclusion rules
```

---

## 📥 Setup & Installation

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
IP_ADDRESS="127.0.0.1"
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
> Never commit actual `.env` files containing your SMTP credentials or database passwords to public repositories.

### Client Environment (`client/.env`)
```ini
# Address and port of the active chat server
IP_ADDRESS=127.0.0.1
PORT_NUMBER=45999
```

---

## 🚦 Running the Application

### Option A: Standard Manual Running

1. **Start MongoDB**: Ensure your local MongoDB instance is active.
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
2. **Configure Environment**: Ensure your `server/.env` is configured with your SMTP email and password credentials.
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

To share this app as a live working model with interviewers, you can host the TCP Socket Server in the cloud using **Railway** (which supports raw TCP port exposure).

### 1. Deploy the Server
1. Sign up/log in to [Railway.app](https://railway.app/).
2. Create a **New Project** -> **Deploy from GitHub repo** -> Select your `Messenger` repository.
3. In the Railway service settings for the server:
   * **Build/Start Command**: Ensure it starts `server/server.py` (since it contains the `Dockerfile` under the `server` folder, Railway will build and run it automatically).
   * **TCP Port**: Under your service's settings page, add a new **TCP Port** mapping. Railway will expose a public host (e.g. `xxx.railway.app`) and a random public port (e.g. `12345`).
   * **Environment Variables**: Add your production credentials (do not hardcode these in code):
     * `MONGODB_USER`
     * `MONGODB_PASSWORD`
     * `MONGODB_HOST`
     * `MONGODB_DB_NAME`
     * `MONGODB_APP_NAME`
     * `RESEND_API_KEY` (For OTP verification emails via Resend API)

### 2. Connect the Client to the Cloud Server
Once your server is running on Railway:
1. Copy the public TCP host and port assigned by Railway (e.g., Host: `xxxx.railway.app`, Port: `12345`).
2. Update your client's `.env` file (`client/.env` and `client/dist/.env`):
   ```ini
   IP_ADDRESS=xxxx.railway.app
   PORT_NUMBER=12345
   ```
3. Run the compiled client executable. It will connect to your hosted server over the internet!

---

## 📦 Packaging the Client

If you want to package the client into a standalone executable (e.g. `.exe` on Windows):

1. **Activate the client virtual environment & install packaging dependencies:**
   ```bash
   cd client
   # Activate your virtual environment (.venv)
   pip install pyinstaller pillow
   ```
   > [!TIP]
   > Installing `pillow` allows PyInstaller to automatically convert custom PNG or JPEG images to the correct Windows icon format during compile time.

2. **Add an Icon:**
   Place your custom icon file named `icon.ico` directly inside the `client/` folder.

3. **Build the executable:**
   Run the build command using PyInstaller:
   ```bash
   pyinstaller --onefile --noconsole --icon="icon.ico" --name "Messenger" messenger.py
   ```

4. **Dynamic Configuration (`.env` file):**
   * PyInstaller outputs the final executable inside the `client/dist/` directory.
   * > [!IMPORTANT]
     > Copy your `.env` configuration file from the `client/` folder and paste it **directly next to `Messenger.exe`** inside the `dist/` directory.
     > The executable dynamically loads settings (like `IP_ADDRESS` and `PORT_NUMBER`) from the `.env` file in its current runtime folder.

5. **Future Rebuilds:**
   Once generated, you can rebuild the executable with the exact same configuration using the spec file:
   ```bash
   pyinstaller messenger.spec
   ```

---

## 📄 License
Distributed under the **MIT License**. See `LICENSE` for details.
