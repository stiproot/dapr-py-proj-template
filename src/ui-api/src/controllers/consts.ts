
export const Configs = {
  DAPR_PROJS_STATE_STORE_NAME: "statestore-projs",
  DAPR_USRS_STATE_STORE_NAME: "statestore-usrs",
  DAPR_PROCS_STATE_STORE_NAME: "statestore-procs",
  DAPR_PUBSUB_NAME: "pubsub",
  DAPR_CMD_WORKFLOW_PUBSUB_NAME: "pubsub-cmd-workflow",
  DAPR_CMD_RECEIPT_PUBSUB_NAME: "pubsub-cmd-receipt",
  WORKFLOW_TOPIC: "PROXIMA_CMD_WORKFLOW",
  UPLOAD_TOPIC: "PROXIMA_CMD_UPLOAD",
  UPLOAD_RECEIPT_TOPIC: "PROXIMA_CMD_UPLOAD_RECEIPT",
}

export enum CmdTypes {
  UPLOAD_DOCUMENTS = "UPLOAD_DOCUMENTS",
  PERSIST_TO_STORE = "PERSIST_TO_STORE",
  BUILD_WORKFLOW = "BUILD_WORKFLOW",
}

export const PartitionKeys = {
  PROJS: "projs",
}