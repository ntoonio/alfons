#!/bin/bash
parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
cd "$parent_path"

# Install requirements, if not done automatically
pip3 install -r requirements.txt

# Make Alfons a service
sudo cp extra/alfons.service /etc/systemd/system/alfons.service
sudo systemctl daemon-reload
sudo systemctl enable alfons
sudo systemctl start alfons