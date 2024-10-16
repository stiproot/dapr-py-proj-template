from json import dumps as json_dumps
from pydantic import BaseModel
from typing import List, Dict, Any
from ..types.cmd_types import CmdTypes
from ..utils.enum_fns import string_to_enum


class RootCmd(BaseModel):
    cmd_type: CmdTypes
    cmd_data: Dict[str, Any]
    cmd_metadata: Dict[str, Any]

    def _user_id_(self) -> str:
        return self.cmd_metadata.get("user_id", "sys")

    def _project_id_(self) -> str:
        return self.cmd_metadata.get("project_id", "default")

    def _cmd_key_(self) -> str:
        return self.cmd_type.value

    def _cmd_post_op_(self) -> Dict[str, Any]:
        return self.cmd_metadata.get("cmd_post_op", {})

    def _cmd_post_op_enrichment_(self) -> Dict[str, Any]:
        return self._cmd_post_op_().get("enrichment", {})

    def _cmd_post_op_proc_(self) -> Dict[str, Any]:
        return self._cmd_post_op_().get("proc", {})

    def _cmd_post_op_enrichment_map_(self) -> List[Dict[str, Any]]:
        return self._cmd_post_op_enrichment_().get("add_property_map", [])

    def _build_post_op_enrichment_obj_(self) -> Dict[str, Any]:
        obj = {}
        add_map = self._cmd_post_op_enrichment_map_()
        for m in add_map:
            obj[m["key"]] = m["val"]
        return obj

    def _to_dict_(self) -> Dict[str, Any]:
        return {
            "cmd_type": self.cmd_type.value,
            "cmd_data": self.cmd_data,
            "cmd_metadata": self.cmd_metadata,
        }

    def _serialize_(self) -> str:
        return json_dumps(self._to_dict_())
