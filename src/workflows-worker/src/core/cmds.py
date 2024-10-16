import logging
from typing import Awaitable, Dict, Any, List, Union
from dataclasses import asdict
from asyncio import gather
from tmpl_framework import (
    DaprConfigs,
    PartitionKeys,
    RootCmd,
    Proj,
    get_state,
    query_state,
    safely_publish_cmd,
)
from .mappers import map_upload_documents_workflow_cmds
from .cmd_factory import add_proc


async def process_cmd(cmd: RootCmd):
    proj_data: Dict[str, Any] = await get_state(
        store_name=DaprConfigs.DAPR_PROJS_STATE_STORE_NAME.value,
        key=cmd._project_id_(),
        partition_key=PartitionKeys.PROJS.value,
    )

    proj = Proj.from_dict(proj_data)
    cmds = map_upload_documents_workflow_cmds(proj=proj)

    await safely_publish_cmd(cmds=cmds)
