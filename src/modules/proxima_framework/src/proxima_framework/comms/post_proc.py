from typing import Awaitable, List, Any, Dict
import logging
from dapr.clients import DaprClient
from dapr.clients.grpc._state import StateItem
from json import dumps as json_dumps
from .dapr_wrapper import get_state, save_state, publish_event
from ..types import (
    RootCmd,
    CmdTypes,
    DaprConfigs,
    ProcStatuses,
    PartitionKeys,
)
from ..actors import create_proc_proxy
from ..utils import hours_between_timestamps, first


def build_uid(id: str, cmd: RootCmd) -> str:
    return f"{cmd._project_id_()}-{id}"


def enrich_payload(payload: dict, cmd: RootCmd) -> None:
    add_map = cmd._cmd_post_op_enrichment_map_()
    for m in add_map:
        payload[m["key"]] = m["val"]

    id = payload["id"]
    project_id = cmd._project_id_()
    new_id = project_id if id == project_id else build_uid(id, cmd)

    payload["id"] = str(id)
    payload["uid"] = new_id


async def publish_cmd(cmd: Dict[str, Any]) -> Awaitable:
    topic_name = cmd["proc"]["target_topic_name"]
    await publish_event(
        pubsub_name=DaprConfigs.DAPR_PUBSUB_NAME.value,
        topic_name=topic_name,
        data=cmd["cmd"]._serialize_(),
    )


def any_still_running(cmds: List[Dict[str, Any]]) -> bool:
    return any(
        cmd.get("proc", {}).get("proc_status", None) == ProcStatuses.RUNNING.value
        for cmd in cmds
    )


async def safely_publish_cmd(cmds: List[Dict[str, Any]]) -> Awaitable:

    first_cmd = first(cmds)["cmd"]
    first_proc = first(cmds)["proc"]
    user_id = first_cmd._user_id_()
    project_id = first_cmd._project_id_()

    proxy = create_proc_proxy(actor_id=user_id)
    state = await proxy.get_state()
    steps = state.get(project_id, {}).get("steps", [])

    if steps:
        if any_still_running(steps):
            logging.warn(f"Cmd(s) still running.")
            return

        this_batch_timestamp = first_proc.get("utc_created_timestamp", None)
        last_batch_timestamp = (
            steps[-1].get("proc", {}).get("utc_created_timestamp", None)
        )

        if hours_between_timestamps(last_batch_timestamp, this_batch_timestamp) < 4:
            logging.warn(f"Cmd(s) were run less than 4 hours ago.")

    steps_state = list(
        map(lambda cmd: {"cmd": cmd["cmd"]._to_dict_(), "proc": cmd["proc"]}, cmds)
    )
    state[project_id] = {"steps": steps_state}

    await proxy.set_state(state)
    await publish_cmd(cmd=first(cmds))


async def update_proc_status(
    cmd: RootCmd, status: str = ProcStatuses.RUNNING.value, err: str = None
) -> Awaitable[Dict[str, Any]]:

    proxy = create_proc_proxy(actor_id=cmd._user_id_())
    state = await proxy.get_state()
    if not state:
        logging.warn(f"No state found for {cmd._project_id_()}")
        return {}

    steps = state.get(cmd._project_id_(), {}).get("steps", [])
    if not steps:
        logging.warn(f"No steps found for {cmd._project_id_()}")
        return {}

    for step in steps:
        if step["cmd"]["cmd_type"] == cmd.cmd_type.value:
            step["proc"]["proc_status"] = status

    await proxy.set_state(state)

    return state


async def handle_next_cmd(
    cmd: RootCmd, status: str = ProcStatuses.COMPLETE.value
) -> Awaitable:

    state = await update_proc_status(cmd=cmd, status=status)

    steps = state.get(cmd._project_id_(), {}).get("steps", [])
    if not steps:
        logging.warn(f"No steps found for {cmd._project_id_()}")
        return

    next_step = first(
        list(
            filter(
                lambda step: step["proc"]["proc_status"] == ProcStatuses.PENDING.value,
                steps,
            )
        )
    )
    if not next_step:
        logging.warn(f"No more steps found for {cmd._project_id_()}")
        return

    await publish_event(
        pubsub_name=DaprConfigs.DAPR_PUBSUB_NAME.value,
        topic_name=next_step["proc"]["target_topic_name"],
        data=next_step["cmd"],
    )
