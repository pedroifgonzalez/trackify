#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}Setting up Trackify...${NC}"

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo -e "${YELLOW}Creating virtual environment...${NC}"
    python -m venv .venv
fi

# Activate virtual environment
echo -e "${YELLOW}Activating virtual environment...${NC}"
source .venv/bin/activate

# Install dependencies
echo -e "${YELLOW}Installing dependencies...${NC}"
pip install -e .

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}Creating .env file from example...${NC}"
    cp .env.example .env
    echo -e "${GREEN}Please edit the .env file with your API keys and configuration.${NC}"
fi

echo -e "${GREEN}Setup complete!${NC}"
echo -e "${GREEN}To get started, run:${NC}"
echo -e "${YELLOW}source .venv/bin/activate${NC}"
echo -e "${YELLOW}python main.py get-pr-summary <pr_id>${NC}"
