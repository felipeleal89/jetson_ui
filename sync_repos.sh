#!/bin/bash
set -e  # Exit immediately if any command fails

# ANSI color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
NC='\033[0m' # No color

# Check if a commit message was provided
if [ -z "$1" ]; then
    echo -e "${RED}✘ Error: No commit message provided.${NC}"
    echo -e "${CYAN}Usage:${NC} $0 \"your commit message\""
    exit 1
fi

COMMIT_MSG="$1"

# Step 1: Stage all changes
echo -e "${CYAN}▶ Step 1: Running 'git add .'${NC}"
git add .

# Step 2: Commit with provided message
echo -e "${CYAN}▶ Step 2: Running 'git commit -m \"$COMMIT_MSG\"'${NC}"
git commit -m "$COMMIT_MSG"

# Step 3: Push to remote repository
echo -e "${CYAN}▶ Step 3: Running 'git push'${NC}"
git push

# Step 4: Confirm and run Ansible playbook
echo -e "${CYAN}▶ Step 4: Preparing to run Ansible playbook 'deploy_ui.yml'${NC}"
read -p "Do you want to proceed with deployment via Ansible? (y/N): " confirm
if [[ "$confirm" =~ ^[Yy]$ ]]; then
    echo -e "${CYAN}▶ Running Ansible playbook...${NC}"
    ansible-playbook -i inventory.yml deploy_ui.yml
    echo -e "${GREEN}✔ Deployment completed.${NC}"
else
    echo -e "${RED}✘ Deployment skipped by user.${NC}"
fi

# Final message
echo -e "${GREEN}✔ Git operations completed successfully.${NC}"
