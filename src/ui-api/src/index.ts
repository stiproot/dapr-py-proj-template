import express from "express";
import cors from "cors";
import { processProcsQry, processProjsQry, processProjQry } from "./controllers/qrys";
import { processWorkflowCmd } from "./controllers/cmds/cmds";
import { processPersistProjCmd, processUpdateProjCmd } from "./controllers/cmds/projs.cmds";
import { processExchangeCodeForTokenCmd, processRefreshTokenCmd } from "./controllers/cmds/auth.cmds";
import { validateToken } from "./controllers/cmds/auth.token";
import { Request, Response } from 'express';
require("dotenv").config();

const BASE_URL = "/ui-api";
const PORT = process.env.PORT || 3001;

const app = express();
app.use(cors());

// AUTH...
app.post(`${BASE_URL}/cmd/auth/token/exchange`, express.json(), processExchangeCodeForTokenCmd);
app.post(`${BASE_URL}/cmd/auth/token/refresh`, express.json(), processRefreshTokenCmd);

// CMDS...
app.post(`${BASE_URL}/cmd/data/workflows`, express.json(), validateToken, processWorkflowCmd);
app.post(`${BASE_URL}/cmd/data/persist/proj`, express.json(), validateToken, processPersistProjCmd);
app.patch(`${BASE_URL}/cmd/data/update/proj`, express.json(), validateToken, processUpdateProjCmd);

// QRYS...
app.post(`${BASE_URL}/qry/data/procs`, express.json(), validateToken, processProcsQry);
app.post(`${BASE_URL}/qry/data/projs`, express.json(), validateToken, processProjsQry);
app.post(`${BASE_URL}/qry/data/proj`, express.json(), validateToken, processProjQry);

// HEALTH...
app.get('/healthz', (req: Request, res: Response) => {
  res.status(200).send('OK');
});

app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
