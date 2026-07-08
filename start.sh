#!/bin/bash

# RohTembak Web GUI - Start Services
# Manual start script for RohTembak services

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}Starting RohTembak services...${NC}"
echo ""

# Start backend
echo -e "${YELLOW}Starting backend...${NC}"
systemctl start rohtembak-backend.service
if systemctl is-active --quiet rohtembak-backend.service; then
    echo -e "${GREEN}✓ Backend started successfully${NC}"
else
    echo -e "${RED}✗ Backend failed to start${NC}"
    exit 1
fi

# Start frontend
echo -e "${YELLOW}Starting frontend...${NC}"
systemctl start rohtembak-frontend.service
if systemctl is-active --quiet rohtembak-frontend.service; then
    echo -e "${GREEN}✓ Frontend started successfully${NC}"
else
    echo -e "${RED}✗ Frontend failed to start${NC}"
    exit 1
fi

# Wait for services to initialize
sleep 2

echo ""
echo -e "${GREEN}╔════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║           Services Started Successfully!              ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${BLUE}Access:${NC}"
echo -e "  Backend:  ${YELLOW}http://localhost:8000${NC}"
echo -e "  Frontend: ${YELLOW}http://localhost:3000${NC}"
echo -e "  API Docs: ${YELLOW}http://localhost:8000/docs${NC}"
echo ""
