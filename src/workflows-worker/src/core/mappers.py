import logging
from typing import Awaitable, Dict, Any, List, Tuple
from dataclasses import asdict
from tmpl_framework import Proj
from .cmd_factory import create_upload_cmd


def map_upload_documents_workflow_cmds(proj: Proj) -> List[Dict[str, Any]]:
    return []
