#!/bin/bash
docker pull $MECHANICAL_IMAGE
docker run --restart always --name mechanical -e ANSYSLMD_LICENSE_FILE=1055@$LICENSE_SERVER -p $PYMECHANICAL_PORT:10000 $MECHANICAL_IMAGE > log.txt &
grep -q 'Started the grpc server' <(timeout 60 tail -f log.txt)