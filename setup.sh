#!/bin/bash

# RohTembak Web GUI - Setup Script
# Run this inside a Debian Bookworm Docker container

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║     RohTembak Web GUI - Setup Script                  ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════╝${NC}"
echo ""

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo -e "${RED}✗ This script must be run as root${NC}"
    exit 1
fi

# Get script directory (resolve symlinks)
SCRIPT_DIR="$( cd -P "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

print_status() { echo -e "${GREEN}✓${NC} $1"; }
print_error()  { echo -e "${RED}✗${NC} $1"; }
print_info()   { echo -e "${BLUE}ℹ${NC} $1"; }
print_warning(){ echo -e "${YELLOW}⚠${NC} $1"; }

echo -e "${BLUE}Project path: ${SCRIPT_DIR}${NC}"
echo ""

# ============================================
# Install System Dependencies
# ============================================
print_info "Installing system dependencies..."

apt-get update -qq
apt-get install -y -qq \
    python3 \
    python3-pip \
    python3-venv \
    curl \
    wget \
    build-essential \
    systemd \
    systemd-sysv \
    > /dev/null 2>&1

print_status "Python 3 installed: $(python3 --version)"

# Install Node.js 20
if ! command -v node &> /dev/null; then
    print_info "Installing Node.js 20..."
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash - > /dev/null 2>&1
    apt-get install -y -qq nodejs > /dev/null 2>&1
fi

print_status "Node.js installed: $(node --version)"
print_status "npm installed: $(npm --version)"

# ============================================
# Backend Setup
# ============================================
print_info "Setting up backend..."

cd "${SCRIPT_DIR}/backend"

# Create virtual environment
if [ ! -d "venv" ]; then
    python3 -m venv venv
    print_status "Virtual environment created"
else
    print_status "Virtual environment already exists"
fi

# Activate and install dependencies
source venv/bin/activate
pip install --upgrade pip -q
pip install -r requirements.txt -q
print_status "Backend dependencies installed"

cd "${SCRIPT_DIR}"

# ============================================
# Frontend Setup
# ============================================
print_info "Setting up frontend..."

cd "${SCRIPT_DIR}/frontend"

# Install dependencies
if [ ! -d "node_modules" ]; then
    npm install --silent
    print_status "Frontend dependencies installed"
else
    print_status "Frontend dependencies already exist"
fi

cd "${SCRIPT_DIR}"

# ============================================
# Environment Setup
# ============================================
print_info "Setting up environment..."

if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        cp .env.example .env
        print_status ".env file created"
    else
        print_warning ".env.example not found, creating default .env"
        cat > .env << 'EOF'
# RohTembak Web GUI - Environment Configuration
SECRET_KEY=rohtembak-secret-key-change-in-production
ENVIRONMENT=development
BASE_API_URL=https://api.myxl.xlaxiata.co.id
BASE_CIAM_URL=https://gede.ciam.xlaxiata.co.id
BASIC_AUTH=OWZjOTdlZDEtNmEzMC00OGQ1LTk1MTYtNjBjNTNjZTNhMTM1OllEV21GNExKajlYSUt3UW56eTJlMmxiMHRKUWIyOW8z
AX_FP_KEY=18b4d589826af50241177961590e6693
UA=myXL / 8.9.0(1202); com.android.vending; (samsung; SM-N935F; SDK 33; Android 13)
API_KEY=vT8tINqHaOxXbGE7eOWAhA==
ENCRYPTED_FIELD_KEY=5dccbf08920a5527
XDATA_KEY=5dccbf08920a5527b99e222789c34bb7
AX_API_SIG_KEY=18b4d589826af50241177961590e6693
X_API_BASE_SECRET=mU1Y4n1vBjf3M7tMnRkFU08mVyUJHed8B5En3EAniu1mXLixeuASmBmKnkyzVziOye7rG5nIekMdthensbQMcOJ6SLnrkGyfXALD7mrBC6vuWv6G01pmD3XlU5rT7Tzx
CIRCLE_MSISDN_KEY=5dccbf08920a5527
EOF
        print_status ".env file created with default values"
    fi
else
    print_status ".env file already exists"
fi

# ============================================
# Setup Systemd Services (with dynamic paths)
# ============================================
print_info "Setting up systemd services..."

mkdir -p /var/log/rohtembak

# Resolve actual paths
BACKEND_DIR="${SCRIPT_DIR}/backend"
FRONTEND_DIR="${SCRIPT_DIR}/frontend"
UVICORN_BIN="${BACKEND_DIR}/venv/bin/uvicorn"
NODE_BIN="$(which node)"
NPM_BIN="$(which npm)"
ENV_FILE="${SCRIPT_DIR}/.env"

# Install backend service
cat > /etc/systemd/system/rohtembak-backend.service << EOF
[Unit]
Description=RohTembak Backend API
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=${BACKEND_DIR}
EnvironmentFile=${ENV_FILE}
ExecStart=${UVICORN_BIN} main:app --host 0.0.0.0 --port 8000 --reload
Restart=always
RestartSec=10
StandardOutput=append:/var/log/rohtembak/backend.log
StandardError=append:/var/log/rohtembak/backend.log

[Install]
WantedBy=multi-user.target
EOF

print_status "Backend service installed (path: ${BACKEND_DIR})"

# Install frontend service
cat > /etc/systemd/system/rohtembak-frontend.service << EOF
[Unit]
Description=RohTembak Frontend
After=network.target rohtembak-backend.service
Wants=rohtembak-backend.service

[Service]
Type=simple
User=root
WorkingDirectory=${FRONTEND_DIR}
EnvironmentFile=${ENV_FILE}
Environment=PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
ExecStart=${NPM_BIN} run dev -- --host 0.0.0.0 --port 3000
Restart=always
RestartSec=10
StandardOutput=append:/var/log/rohtembak/frontend.log
StandardError=append:/var/log/rohtembak/frontend.log

[Install]
WantedBy=multi-user.target
EOF

print_status "Frontend service installed (path: ${FRONTEND_DIR})"

# Enable and start services
systemctl daemon-reload
systemctl enable rohtembak-backend.service
systemctl enable rohtembak-frontend.service
print_status "Services enabled for auto-start"

systemctl start rohtembak-backend.service
systemctl start rohtembak-frontend.service
print_status "Services started"

# Wait for services to initialize
sleep 3

# Check service status
if systemctl is-active --quiet rohtembak-backend.service; then
    print_status "Backend is running"
else
    print_warning "Backend may not be running properly"
    echo -e "  Check: ${YELLOW}journalctl -xeu rohtembak-backend.service${NC}"
fi

if systemctl is-active --quiet rohtembak-frontend.service; then
    print_status "Frontend is running"
else
    print_warning "Frontend may not be running properly"
    echo -e "  Check: ${YELLOW}journalctl -xeu rohtembak-frontend.service${NC}"
fi

# ============================================
# Summary
# ============================================
echo ""
echo -e "${GREEN}╔════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║              Setup Complete!                          ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${BLUE}Services are running and will auto-start on boot:${NC}"
echo ""
echo -e "  Backend:  ${YELLOW}http://localhost:8000${NC}"
echo -e "  Frontend: ${YELLOW}http://localhost:3000${NC}"
echo -e "  API Docs: ${YELLOW}http://localhost:8000/docs${NC}"
echo ""
echo -e "${BLUE}Service Management:${NC}"
echo -e "  Status:   ${YELLOW}systemctl status rohtembak-backend rohtembak-frontend${NC}"
echo -e "  Restart:  ${YELLOW}systemctl restart rohtembak-backend rohtembak-frontend${NC}"
echo -e "  Stop:     ${YELLOW}systemctl stop rohtembak-backend rohtembak-frontend${NC}"
echo ""
echo -e "${BLUE}Logs:${NC}"
echo -e "  Backend:  ${YELLOW}tail -f /var/log/rohtembak/backend.log${NC}"
echo -e "  Frontend: ${YELLOW}tail -f /var/log/rohtembak/frontend.log${NC}"
echo ""
echo -e "${GREEN}✓ Services will automatically restart after power outage or container restart${NC}"
echo ""
