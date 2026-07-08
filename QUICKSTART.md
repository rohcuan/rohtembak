# 🚀 Quick Start - RohTembak Web GUI

## Setup di Dalam Docker Container

### 1. Buat Debian Bookworm Container

```bash
docker run -it --name rohtembak -p 8000:8000 -p 3000:3000 debian:bookworm /bin/bash
```

**Penting:** Container harus dijalankan dengan systemd support:
```bash
docker run -it --name rohtembak \
  -p 8000:8000 -p 3000:3000 \
  --tmpfs /run \
  --tmpfs /run/lock \
  --cgroupns=host \
  -v /sys/fs/cgroup:/sys/fs/cgroup:rw \
  debian:bookworm /sbin/init
```

### 2. Clone Repository

Di dalam container:

```bash
apt-get update && apt-get install -y git
git clone https://github.com/rohcuan/rohtembak.git
cd rohtembak
```

### 3. Jalankan Setup Script

```bash
chmod +x setup.sh
./setup.sh
```

**Script akan otomatis:**
- ✅ Install Python 3, Node.js 20, dan semua dependencies
- ✅ Setup backend dan frontend
- ✅ Install systemd services
- ✅ Enable auto-start pada boot
- ✅ Start services langsung

### 4. Akses Aplikasi

Setelah setup selesai, services langsung berjalan:

- **Backend**: http://localhost:8000
- **Frontend**: http://localhost:3000
- **API Docs**: http://localhost:8000/docs

## 🔄 Auto-Start Behavior

Services akan **otomatis start** pada kondisi berikut:

1. **Setelah setup.sh dijalankan** - Services langsung start
2. **Container restart** - Systemd akan start services otomatis
3. **Power outage** - Saat container restore, services akan start sendiri
4. **Service crash** - Systemd akan restart service dalam 10 detik

## 🛠️ Service Management

### Cek Status
```bash
systemctl status rohtembak-backend
systemctl status rohtembak-frontend
```

### Manual Start/Stop
```bash
# Start
./start.sh

# Stop
./stop.sh

# Restart
systemctl restart rohtembak-backend rohtembak-frontend
```

### View Logs
```bash
# Backend logs
tail -f /var/log/rohtembak/backend.log

# Frontend logs
tail -f /var/log/rohtembak/frontend.log
```

## 📝 Notes

- **Systemd required**: Container harus support systemd untuk auto-start
- **Services auto-restart**: Jika service crash, akan restart dalam 10 detik
- **Logs**: Semua logs tersimpan di `/var/log/rohtembak/`
- **Environment**: API keys sudah di-configure di `.env`
