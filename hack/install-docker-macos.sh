#!/usr/bin/env bash

set -Eeuo pipefail

# Install Docker
# From https://github.com/actions/runner-images/issues/17#issuecomment-1537238473
# From https://github.com/abiosoft/colima/discussions/273#discussioncomment-4959736
brew install docker docker-buildx
mkdir -p $HOME/.docker/cli-plugins
ln -sfn $(which docker-buildx) $HOME/.docker/cli-plugins/docker-buildx

# Install Lima
brew install lima
# Don't explicitly start Lima here (e.g. with `limactl start`).
# Let Colina do that, otherwise, # Colima seems to hang
# waiting for the SSH requirement to be met.

# Install Colima
sudo mkdir -p /usr/local/bin
sudo curl -L -o /usr/local/bin/colima https://github.com/abiosoft/colima/releases/download/v0.6.9/colima-Darwin-x86_64 && sudo chmod +x /usr/local/bin/colima
colima start --memory 5 --runtime docker

# Link Colima and Docker
sudo ln -sf $HOME/.colima/default/docker.sock /var/run/docker.sock
