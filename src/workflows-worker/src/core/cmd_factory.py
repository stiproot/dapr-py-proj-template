import logging
from typing import Dict, Any
from tmpl_framework import (
    DaprConfigs,
    RootCmd,
    CmdTypes,
    ProcStatuses,
    Proj,
    utc_now_timestamp_str,
)


def create_upload_cmd(proj: Proj) -> Dict[str, Any]:

    cmd = {
        "cmd": RootCmd(
            cmd_type=CmdTypes.UPLOAD_DOCUMENTS.value,
            cmd_data={},
            cmd_metadata={
                "cmd_post_op": {
                    "enrichment": {
                        "add_property_map": [
                            {"key": "__metadata__", "val": {"project_id": proj.id}}
                        ]
                    },
                },
                "project_id": proj.id,
                "user_id": proj.user_id,
            },
        ),
        "proc": {
            "target_topic_name": DaprConfigs.UPLOAD_TOPIC.value,
            "proc_status": ProcStatuses.PENDING.value,
            "proc_err": None,
            "utc_created_timestamp": utc_now_timestamp_str(),
        },
    }

    return cmd


def add_proc(cmd: RootCmd, topic_name: str) -> Dict[str, Any]:
    return {
        "cmd": cmd,
        "proc": {
            "target_topic_name": topic_name,
            "proc_status": ProcStatuses.PENDING.value,
            "proc_err": None,
            "utc_created_timestamp": utc_now_timestamp_str(),
        },
    }
