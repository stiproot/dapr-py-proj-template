#!/bin/sh

# USED TO RUN THIS SERVICE LOCALLY, USING THE DAPR CLI

dapr run --app-id tmpl-test-harness \
    --placement-host-address localhost:50000 \
    --resources-path ../../src/..dapr/components.local/ \
    --config ../../src/.dapr/configuration/config.yaml \
    --app-port 6010 \
    -- python3 -m uvicorn main:app --host 0.0.0.0 --port 6010