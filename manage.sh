#!/bin/bash

set -e

SCRIPT_HOME="$( cd "$( dirname "$0" )" && pwd )"
DOCKER_DIRECTORY="docker"

cd "$SCRIPT_HOME/$DOCKER_DIRECTORY"

case "$1" in
  start_nodes)
      docker-compose up node1 node2 node3 node4
    ;;
  start_client)
      docker-compose run client
    ;;
  stop)
      docker-compose stop
    ;;
  build)
      docker-compose build
    ;;
  rebuild)
      docker-compose build --no-cache
    ;;
  *)
    echo $"Usage: $0 {start_nodes|start_client|stop|build|rebuild}"
    RETVAL=1
esac

cd - > /dev/null