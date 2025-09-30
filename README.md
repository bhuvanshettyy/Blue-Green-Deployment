# Pricing API with Blue-Green Deployment

This project provides a **FastAPI-based Pricing API** that supports a **blue-green deployment strategy**.  
Requests are routed to different backend versions (**Blue** or **Green**) based on headers or IP rules.  

---

## 🚀 Features
- FastAPI backend  
- Header-based and IP-based routing  
- Configurable using `.env` file  
- Supports hot reload with `watchfiles`  
- WebSocket support  

---

## 📦 Requirements
Dependencies are listed in `requirements.txt`.  
To install them:

```bash
pip install -r requirements.txt
```

##
▶️ Running the Server

Start the API with hot reload enabled:

uvicorn backend.main:app --reload

Here:

backend.main:app → Looks for app inside backend/main.py

--reload → Restarts the server automatically on code changes

##
🌐 Endpoints

GET /pricing → Returns pricing from Blue or Green version based on routing logic

WS /ws → WebSocket demo endpoin