#!/usr/bin/env bash

set -o nounset
set -o errexit
set -o pipefail

while read -r _line; do
  _no_repo=${_line#'docker.io/'}
  _image=$(echo $_no_repo | cut -d ":" -f 1)
  _tag=$(echo $_no_repo | cut -d ":" -f 2)

  _time=$(
    curl -s "https://hub.docker.com/v2/repositories/$_image/tags/$_tag" | jq '.tag_last_pushed'
  )
  echo "$_image:$_tag ==> $_time"
done
