from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dapr.ext.fastapi import DaprApp
from dapr.ext.fastapi import DaprActor
from dapr.actor.runtime.config import (
    ActorRuntimeConfig,
    ActorTypeConfig,
    ActorReentrancyConfig,
)
from dapr.actor.runtime.runtime import ActorRuntime
import logging
from core import route_cmd
from tmpl_framework import (
    RootCmd,
    CloudEvt,
    DaprConfigs,
    ProcActor,
)
from endpoints import healthz

logging.basicConfig(level=logging.DEBUG)

app = FastAPI()
dapr_app = DaprApp(app)

config = ActorRuntimeConfig()
config.update_actor_type_configs(
    [
        ActorTypeConfig(
            actor_type=ProcActor.__name__,
            reentrancy=ActorReentrancyConfig(enabled=True),
        )
    ]
)
ActorRuntime.set_actor_config(config)

actor = DaprActor(app)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(healthz.router)


@app.on_event("startup")
async def startup_event():
    logging.info("Registering actors...")
    await actor.register_actor(ProcActor)


@dapr_app.subscribe(
    pubsub=DaprConfigs.DAPR_CMD_WORKFLOW_PUBSUB_NAME.value,
    topic=DaprConfigs.WORKFLOW_TOPIC.value,
    route="/workflows/cmd",
)
async def process_evt(evt: CloudEvt):
    logging.info(f"Received evt.")
    cmd = RootCmd(**evt.data)
    await route_cmd(cmd)
    logging.info(f"Processed evt")