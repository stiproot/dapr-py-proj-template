import logging
from typing import Awaitable
from tmpl_framework import (
    RootCmd,
    CmdTypes,
)
from .cmds import process_cmd


async def route_cmd(cmd: RootCmd) -> Awaitable:

    if cmd.cmd_type.value == CmdTypes.BUILD_WORKFLOW.value:
        await process_cmd(cmd)
        return

    raise ValueError(f"Unsupported cmd_type: {cmd.cmd_type.value}")
