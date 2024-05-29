#!/usr/bin/env bash

set -Eeuo pipefail

export LDFLAGS="-L/usr/local/opt/libomp/lib"
export CPPFLAGS="-I/usr/local/opt/libomp/include"
