# RohTembak Web GUI

Web-based GUI untuk XL Axiata CLI Client.

## 🚀 Quick Start

Satu command, langsung jalan:

```bash
git clone https://github.com/rohcuan/rohtembak.git && cd rohtembak && chmod +x setup.sh start.sh stop.sh && ./setup.sh
```

Setup script akan otomatis:
- ✅ Install Python 3, Node.js 20, dan semua dependencies
- ✅ Setup backend (FastAPI) dan frontend (React)
- ✅ Install systemd services (auto-start on boot & after crash)
- ✅ Start services langsung

Setelah selesai, akses:
- **Frontend**: http://localhost:3000
- **Backend**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## 🔧 Service Management

```bash
# Cek status
systemctl status rohtembak-backend rohtembak-frontend

# Start/Stop/Restart
./start.sh
./stop.sh
systemctl restart rohtembak-backend rohtembak-frontend

# View logs
tail -f /var/log/rohtembak/backend.log
tail -f /var/log/rohtembak/frontend.log
```

## 📁 Struktur Project

```
rohtembak/
├── backend/           # FastAPI backend
├── frontend/          # React frontend
├── cli/              # Original CLI code
├── setup.sh          # Setup script
├── start.sh          # Start services
├── stop.sh           # Stop services
└── .env              # Environment variables
```

## 🔐 Authentication Flow

1. **Subscription Login**: Login dengan username/password dari subscription list
2. **JWT Token**: Backend generate JWT token untuk session
3. **XL Login**: Login ke XL dengan OTP
4. **API Access**: Semua API calls menggunakan JWT token

## 📝 Environment Variables

File `.env` sudah include semua API keys XL Axiata. Variables yang bisa di-configure:
- `SECRET_KEY` - JWT secret key
- `ENVIRONMENT` - development/production

## 🛠️ Tech Stack

- **Base**: Debian Bookworm
- **Backend**: FastAPI, Python 3
- **Frontend**: React 18, TypeScript, Vite
- **Database**: File-based (JSON)

## 📄 License

Same as original RohTembak project.
