import logging
from typing import Awaitable
from tmpl_framework import RootCmd, handle_next_cmd


async def process_cmd(cmd: RootCmd) -> Awaitable:
    await handle_next_cmd(cmd=cmd)
