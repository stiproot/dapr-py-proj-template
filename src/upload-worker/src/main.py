from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dapr.ext.fastapi import DaprApp
import logging
from core import upload_documents_workflow
from tmpl_framework import CmdTypes, RootCmd, CloudEvt, DaprConfigs
from endpoints import healthz

logging.basicConfig(level=logging.INFO)

app = FastAPI()
dapr_app = DaprApp(app)


app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


workflow_hash = {
    CmdTypes.UPLOAD_DOCUMENTS: upload_documents_workflow,
}

app.include_router(healthz.router)


@dapr_app.subscribe(
    pubsub=DaprConfigs.DAPR_CMD_UPLOAD_PUBSUB_NAME.value,
    topic=DaprConfigs.UPLOAD_TOPIC.value,
    route="/insights/worker/cmd",
)
async def process_evt(evt: CloudEvt):
    logging.info(f"Received evt: {evt}")
    cmd = RootCmd(**evt.data)
    await workflow_hash[cmd.cmd_type](cmd)
    logging.info(f"Processed evt: {evt}")
