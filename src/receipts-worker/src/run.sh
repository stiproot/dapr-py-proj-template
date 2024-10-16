#!/bin/sh

dapr run --app-id tmpl-receipts-worker \
    --placement-host-address localhost:50000 \
    --resources-path ../../../.dapr/components/ \
    --config ../../../dapr/configuration/config.yaml \
    --app-port 6007 \
    -- python3 -m uvicorn main:app --host 0.0.0.0 --port 6007