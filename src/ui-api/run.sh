#!/bin/sh

dapr run --app-id tmpl-ui-api \
  --placement-host-address localhost:50000 \
  --config ../../dapr/configuration/config.yaml \
  --resources-path ../../.dapr/components.local/ \
  --dapr-http-port 3500 \
  --app-port 3001 \
  -- npm run start

# -- npx ts-node src/index.ts
