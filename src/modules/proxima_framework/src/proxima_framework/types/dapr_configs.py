from enum import Enum


class DaprConfigs(Enum):
    DAPR_PROJS_STATE_STORE_NAME = "statestore-projs"
    DAPR_PROCS_STATE_STORE_NAME = "statestore-procs"
    DAPR_USRS_STATE_STORE_NAME = "statestore-usrs"
    DAPR_PUBSUB_NAME = "pubsub"
    DAPR_CMD_UPLOAD_PUBSUB_NAME = "pubsub-cmd-upload"
    DAPR_CMD_WORKFLOW_PUBSUB_NAME = "pubsub-cmd-workflow"
    DAPR_CMD_RECEIPT_PUBSUB_NAME = "pubsub-cmd-receipt"
    WORKFLOW_TOPIC = "PROXIMA_CMD_WORKFLOW"
    UPLOAD_TOPIC = "PROXIMA_CMD_UPLOAD"
    UPLOAD_RECEIPT_TOPIC = "PROXIMA_CMD_UPLOAD_RECEIPT"


class PartitionKeys(Enum):
    PROCS = "procs"
    PROJS = "projs"
    USRS = "usrs"
