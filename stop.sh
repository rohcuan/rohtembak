#!/bin/bash

# RohTembak Web GUI - Stop Services
# Manual stop script for RohTembak services

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}Stopping RohTembak services...${NC}"
echo ""

# Stop frontend first
echo -e "${YELLOW}Stopping frontend...${NC}"
systemctl stop rohtembak-frontend.service
if ! systemctl is-active --quiet rohtembak-frontend.service; then
    echo -e "${GREEN}✓ Frontend stopped${NC}"
else
    echo -e "${RED}✗ Frontend still running${NC}"
fi

# Stop backend
echo -e "${YELLOW}Stopping backend...${NC}"
systemctl stop rohtembak-backend.service
if ! systemctl is-active --quiet rohtembak-backend.service; then
    echo -e "${GREEN}✓ Backend stopped${NC}"
else
    echo -e "${RED}✗ Backend still running${NC}"
fi

echo ""
echo -e "${GREEN}✓ All services stopped${NC}"
echo ""
