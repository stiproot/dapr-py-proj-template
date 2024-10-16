from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dapr.ext.fastapi import DaprApp
import logging
from core import process_cmd
from tmpl_framework import RootCmd, CloudEvt, DaprConfigs
from endpoints import healthz

logging.basicConfig(level=logging.DEBUG)

app = FastAPI()
dapr_app = DaprApp(app)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(healthz.router)


@dapr_app.subscribe(
    pubsub=DaprConfigs.DAPR_CMD_RECEIPT_PUBSUB_NAME.value,
    topic=DaprConfigs.UPLOAD_RECEIPT_TOPIC.value,
    route="/receipts/cmd/structure",
)
async def process_upload_evt(evt: CloudEvt):
    logging.info(f"Received evt (upload): {evt}")
    cmd = RootCmd(**evt.data)
    await process_cmd(cmd)
    logging.info(f"Processed evt: {evt}")