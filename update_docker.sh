#!/usr/bin/env bash
set -euo pipefail

echo "========================================"
echo " Docker Deployment Update Script"
echo "========================================"
echo

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if docker-compose is installed
if ! command -v docker-compose &> /dev/null && ! command -v docker &> /dev/null; then
    echo -e "${RED}ERROR: Docker or docker-compose is not installed!${NC}"
    echo "Please install Docker first."
    exit 1
fi

# Determine docker compose command
DOCKER_COMPOSE_CMD="docker-compose"
if ! command -v docker-compose &> /dev/null; then
    # Try docker compose (new syntax)
    if docker compose version &> /dev/null; then
        DOCKER_COMPOSE_CMD="docker compose"
    else
        echo -e "${RED}ERROR: Could not find docker-compose or docker compose command!${NC}"
        exit 1
    fi
fi

echo -e "${GREEN}[1/5] Backing up current .env file...${NC}"
if [[ -f ".env" ]]; then
    cp .env .env.backup
    echo ".env backed up to .env.backup"
else
    echo -e "${YELLOW}WARNING: No .env file found. Will create from .env.example after pull.${NC}"
fi
echo

echo -e "${GREEN}[2/5] Pulling latest code from git...${NC}"
if [[ -d ".git" ]]; then
    # Stash any local changes to prevent conflicts
    git stash push -m "Auto-stash before update $(date +%Y%m%d_%H%M%S)"
    
    # Pull latest changes
    git pull origin main
    
    echo -e "${GREEN}Latest code pulled successfully!${NC}"
else
    echo -e "${RED}ERROR: Not a git repository!${NC}"
    echo "Please run this script from the project root directory."
    exit 1
fi
echo

echo -e "${GREEN}[3/5] Checking .env configuration...${NC}"
# If .env doesn't exist, create from example
if [[ ! -f ".env" ]]; then
    echo "Creating .env from .env.example..."
    cp .env.example .env
    echo -e "${YELLOW}IMPORTANT: Please edit .env and set your API_KEY!${NC}"
    echo "After setting API_KEY, run this script again."
    exit 0
fi

# Restore API_KEY from backup if it exists
if [[ -f ".env.backup" ]]; then
    OLD_API_KEY=$(grep -E "^API_KEY=" .env.backup | cut -d '=' -f 2- || echo "")
    if [[ -n "${OLD_API_KEY}" ]]; then
        # Update API_KEY in new .env
        if grep -q "^API_KEY=" .env; then
            sed -i.tmp "s|^API_KEY=.*|API_KEY=${OLD_API_KEY}|" .env
            rm -f .env.tmp
            echo "API_KEY restored from backup"
        fi
    fi
fi

# Check if API_KEY is set
API_KEY=$(grep -E "^API_KEY=" .env | cut -d '=' -f 2- || echo "")
if [[ -z "${API_KEY}" ]] || [[ "${API_KEY}" == "your-secret-key-here" ]]; then
    echo -e "${YELLOW}WARNING: API_KEY is not set or using default value!${NC}"
    echo "Please edit .env and set a secure API_KEY."
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi
echo

echo -e "${GREEN}[4/5] Stopping current containers...${NC}"
${DOCKER_COMPOSE_CMD} down
echo "Containers stopped"
echo

echo -e "${GREEN}[5/5] Building and starting containers...${NC}"
${DOCKER_COMPOSE_CMD} build --no-cache
${DOCKER_COMPOSE_CMD} up -d

echo
echo "Waiting for service to start..."
sleep 3

# Check if container is running
if ${DOCKER_COMPOSE_CMD} ps | grep -q "Up"; then
    echo -e "${GREEN}========================================"
    echo " Update Complete!"
    echo "========================================${NC}"
    echo
    echo "Service is running:"
    ${DOCKER_COMPOSE_CMD} ps
    echo
    echo "To view logs:"
    echo "  ${DOCKER_COMPOSE_CMD} logs -f"
    echo
    echo "To stop the service:"
    echo "  ${DOCKER_COMPOSE_CMD} down"
else
    echo -e "${RED}========================================"
    echo " ERROR: Container failed to start!"
    echo "========================================${NC}"
    echo
    echo "Check logs with:"
    echo "  ${DOCKER_COMPOSE_CMD} logs"
    exit 1
fi




