# 📢 Messenger — Real-Time Chat Application

A premium, modular full-stack client-server chat application featuring a Tkinter-based dark theme, MongoDB persistence, secure email OTP validation, timezone-aware dynamic chat separators, and background sliding notifications.

This repository contains both the client application and the backend socket server.

---

## 🚀 Key Features

* **Real-time Messaging**: Socket connection enabling direct private chats and broadcast routing.
* **Modern Dark UI**: Segoe UI typography, sleek visual containers, inline password toggles, and customized focus layouts.
* **OTP Verification**: Secure registration and password recovery validated by SMTP-dispatched OTP codes.
* **Database Caching**: MongoDB database with compound index query optimizations and TTL (Time-to-Live) indexes for automated OTP code expiration.
* **Unread Notification Badges**: Sidebar badge updates displaying the number of unread messages per contact.
* **Sliding Toast Alerts**: Smooth animation slide-downs notifying users of background incoming messages.
* **Dynamic Timestamps**: Timezone-aware date separators (e.g. `Today`, `Yesterday`, `Month Day, Year`) inside scrollable bubbles.
* **Highly Modular Design**: Code base cleanly partitioned using MVC (Model-View-Controller) structure.

---

## 🏗 System Architecture

The application is structured using an **MVC (Model-View-Controller)** pattern on the client side, communicating over raw TCP JSON sockets to a multithreaded daemon server:

```mermaid
graph TD
    subgraph Client App [Client MVC Architecture]
        M[messenger.py Controller] --> V[ui_screens.py Views]
        M --> C[client.py Network Listener]
        V --> F[Widget Factories]
        M --> T[toast.py Notifications]
        M --> U1[utils.py Formatting]
    end
    
    subgraph Server Backend [Server daemon]
        S[server.py Main Daemon] --> CM[client_manager.py Registry]
        S --> H[handlers.py Request Router]
        H --> DB[database.py MongoDB Connector]
        H --> U2[utils.py SMTP Sender]
    end
    
    C <--> |TCP JSON Sockets| S
```

---

## 🛠 Directory Structure

```bash
Messenger/
├── client/
│   ├── .env.example       # Client environment settings
│   ├── client.py          # Network socket listener thread
│   ├── config.py          # Colors, fonts, and theme configs
│   ├── messenger.py       # Main App controller (MVC Coordinator)
│   ├── requirements.txt   # Client package dependencies
│   ├── toast.py           # Slide-in toast notification animation
│   ├── ui_screens.py      # Login, Register, Forgot, and Dashboard UI
│   └── utils.py           # Datetime parsing and formatting
├── server/
│   ├── .env.example       # Server environment settings
│   ├── client_manager.py  # Thread-safe socket registry manager
│   ├── config.py          # Port configs and MongoDB URI
│   ├── database.py        # MongoDB connection and queries wrapper
│   ├── handlers.py        # Client actions request controller
│   ├── requirements.txt   # Server package dependencies
│   ├── server.py          # Main TCP socket port listener
│   └── utils.py           # Email verification and SMTP dispatcher
└── .gitignore             # Git exclusion rules
```

---

## 📥 Setup & Installation

### 1. Prerequisites
* **Python 3.8+** installed on your machine.
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
# SMTP configuration (Gmail App Password)
EMAIL_NAME="your_smtp_gmail@gmail.com"
EMAIL_PASSWORD="your_four_word_app_password"

# Port and address bindings
IP_ADDRESS="127.0.0.1"
PORT_NUMBER="45999"

# MongoDB connection string
MONGODB_URI="mongodb://username:password@127.0.0.1:27017/db_messenger?authSource=db_messenger"
```

### Client Environment (`client/.env`)
```ini
# Address and port of the active chat server
IP_ADDRESS=127.0.0.1
PORT_NUMBER=45999
```

---

## 🚦 Running the Application

### Option A: Standard Manual Running

1. **Start MongoDB**: Ensure that your MongoDB instance is active.
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
   *(You can launch multiple client terminals to test messaging).*

---

### Option B: Docker Compose (Server & Database Stack)

You can launch the entire server infrastructure (MongoDB and the TCP Chat Server) headlessly in isolated containers:

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

To run the Tkinter GUI client inside a Docker container (separately from the server stack), you must configure display forwarding to your host:

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

## 📦 Packaging the Client (Optional)
If you want to package the client into a standalone executable (e.g. `.exe` on Windows):

1. Activate your client virtual environment and install PyInstaller:
   ```bash
   pip install pyinstaller
   ```
2. Build the executable:
   ```bash
   pyinstaller --onefile --noconsole --name "Messenger" messenger.py
   ```
3. Find your standalone executable in the newly created `dist/` directory.

---

## 📄 License
Distributed under the **MIT License**. See `LICENSE` for details.
