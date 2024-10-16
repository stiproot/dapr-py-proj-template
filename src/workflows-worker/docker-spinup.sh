#!/bin/sh

# USED TO BUILD, RUN AND EXEC AND INTERACTIVE TERMAINAL IN THE CONTAINER OF THIS SERVICE.

docker build -f Dockerfile -t img-tmpl-workflows-worker-$1 .

docker run --name tmpl-workflows-worker-$1 \
    -p 8005:8001 \
    -e ENVIRONMENT=aks \
    -e KEY_VAULT_URL=https://kvprojectmetricsdevtest.vault.azure.net/ \
    -e COSMOS_DATABASE_NAME=cossqldb-tmpl-devtest \
    -e COSMOS_URL=https://cosmos.documents.azure.com:443/ \
    -e STORE_QUERY_URL= \
    -it --detach \
    img-tmpl-workflows-worker-$1

docker exec -it tmpl-workflows-worker-$1 sh