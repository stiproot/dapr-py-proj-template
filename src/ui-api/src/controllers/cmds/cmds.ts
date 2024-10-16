import { publishPubSubMsg } from "../pubsub-manager";
import { CmdTypes, Configs } from "../consts";
import { IReq, ICmd, ICmdMetadata, IPubSubCmd, IAzdoReq } from '../types';
import { Response } from 'express';

export const processWorkflowCmd = async (req: IReq<ICmd>, res: Response) => {

  const { userId, projectId } = req.body.cmdData;

  const cmd = {
    cmd_type: CmdTypes.BUILD_WORKFLOW,
    cmd_data: {},
    cmd_metadata: {
      user_id: userId,
      project_id: projectId,
    } as ICmdMetadata
  };

  await publishPubSubMsg(Configs.WORKFLOW_TOPIC, cmd);

  console.info("Processed workflow cmd.");
  res.status(200).send('OK');
};

export const processAzdoProxyCmds = async (req: IReq<ICmd>, res: Response) => {

  const { userId, reqs }: { userId: string, reqs: IAzdoReq[] } = req.body.cmdData;

  await Promise.all(reqs.map(r => publishPubSubMsg(Configs.WORKFLOW_TOPIC, createAzdoCmd(r, userId))));

  console.info("Processed azdo proxy cmds.");
  res.status(200).send('OK');
};

const createAzdoCmd = (req: IAzdoReq, userId: string, projectId: string = "default"): IPubSubCmd => {
  const cmd = {
    cmd_type: req.cmdType,
    cmd_data: req.cmdData,
    cmd_metadata: {
      user_id: userId,
      project_id: projectId,
    } as ICmdMetadata,
  } as IPubSubCmd;

  return cmd;
}