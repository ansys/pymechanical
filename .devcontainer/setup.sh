#!/usr/bin/env bash
set -e

# Install Python from deadsnakes PPA
apt update
apt install --reinstall ca-certificates
apt install lsb-release xvfb software-properties-common -y
add-apt-repository ppa:deadsnakes/ppa -y
apt install -y python3.11 python3.11-venv
python3.11 -m venv /env

# Create venv
python3.11 -m venv .env
. /env/bin/activate

# Upgrade pip and install your repo in editable mode
pip install --upgrade pip
pip install uv
pip install -e .
