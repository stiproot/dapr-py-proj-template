#!/bin/sh

docker build -f Dockerfile -t img-tmpl-receipts-worker-$1 .

docker run --name tmpl-receipts-worker-$1 \
    -p 8005:8001 \
    -e ENVIRONMENT=aks \
    -e KEY_VAULT_URL=https://kvprojectmetricsdevtest.vault.azure.net/ \
    -e COSMOS_DATABASE_NAME=cossqldb-tmpl-devtest \
    -e COSMOS_URL=https://cosmos.documents.azure.com:443/ \
    -e STORE_QUERY_URL= \
    -it --detach \
    img-tmpl-receipts-worker-$1

docker exec -it tmpl-receipts-worker-$1 sh