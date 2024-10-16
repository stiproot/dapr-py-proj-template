#!/bin/sh

# docker build -f Dockerfile -t img-tmpl-ui-api-$1 .
docker run --name tmpl-ui-api-$1 -p 3001:3002 -it --detach img-tmpl-ui-api-$1
# docker exec -it tmpl-ui-api-$1 sh
