#!/bin/sh

rm -r ./dist/
npm run build
cp .env ./dist/

docker build -f Dockerfile -t img-tmpl-ui-$1 .

docker run --name tmpl-ui-$1 \
    -p 8080:8081 \
    -it --detach \
    img-tmpl-ui-$1

# docker exec -it tmpl-ui-$1 sh
