#!/bin/sh

dapr run --app-id tmpl-workflows-worker \
    --placement-host-address localhost:50000 \
    --resources-path ../../../.dapr/components.local/ \
    --config ../../../dapr/configuration/config.yaml \
    --app-port 6006 \
    -- python3 -m uvicorn main:app --host 0.0.0.0 --port 6006