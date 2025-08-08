#!/bin/bash
set -euo pipefail

# Resolve project root and log file path robustly
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
LOG_DIR="$PROJECT_ROOT/logs"
LOG_FILE="$LOG_DIR/provisioning.log"

# Ensure logs dir exists
mkdir -p "$LOG_DIR"

log() {
  # usage: log "INFO" "message"
  local level="$1"; shift
  echo "$(date '+%Y-%m-%d %H:%M:%S') - $level - $*" | tee -a "$LOG_FILE" >/dev/null
}

log INFO "Starting Nginx installation..."

# Detect package manager
PM=""
if command -v dnf >/dev/null 2>&1; then
  PM="dnf"
elif command -v yum >/dev/null 2>&1; then
  PM="yum"
elif command -v apt-get >/dev/null 2>&1; then
  PM="apt-get"
else
  log ERROR "No supported package manager found (dnf/yum/apt-get)."
  exit 1
fi
log INFO "Detected package manager: $PM"

# Already installed?
if command -v nginx >/dev/null 2>&1; then
  log INFO "Nginx already installed. Skipping."
  exit 0
fi

# Install nginx
log INFO "Installing Nginx..."
if [ "$PM" = "apt-get" ]; then
  sudo apt-get update >>"$LOG_FILE" 2>&1
  sudo apt-get install -y nginx >>"$LOG_FILE" 2>&1
else
  sudo "$PM" -y install nginx >>"$LOG_FILE" 2>&1
fi

# Enable & start service if systemd is present
if command -v systemctl >/dev/null 2>&1; then
  sudo systemctl enable nginx >>"$LOG_FILE" 2>&1 || true
  sudo systemctl start nginx >>"$LOG_FILE" 2>&1 || true
fi

log INFO "Nginx installation completed successfully."