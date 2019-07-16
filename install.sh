#!/bin/bash
parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
cd "$parent_path"

# Make Alfons a service
sudo cp extra/alfons.service /lib/systemd/system/alfons.service
sudo systemctl daemon-reload
sudo systemctl enable alfons
sudo systemctl start alfons

# Install requirements, if not done automatically
pip3 install -r requirements.txt