# Pricing API with Blue-Green Deployment

This project provides a **FastAPI-based Pricing API** that supports **blue-green deployment strategy**.  
Requests are routed to different backend versions (Blue or Green) based on headers or IP rules.  

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
