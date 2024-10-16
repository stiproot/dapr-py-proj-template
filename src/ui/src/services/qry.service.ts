import { HttpClient } from "./http.client";
import { dataEnricher } from "./enricher.service";

export class QryService {
  private readonly _client = new HttpClient();

  private async post(endpoint: string, qryData: any = {}): Promise<any> {
    try {
      return await this._client.post(endpoint, { qryData });
    } catch (error) {
      console.error(`POST request to ${endpoint} failed:`, error);
      return [];
    }
  }

  public getProjQry(projId: string): Promise<any> {
    return this.post("/qry/data/proj", { projId });
  }

  public getProjsQry(qryData: any): Promise<any> {
    return this.post("/qry/data/projs", qryData);
  }

  public async getProcsQry(data: any): Promise<any> {
    dataEnricher.enrichWithUsr(data);
    return this.post("/qry/data/procs", { userId: data.userId });
  }
}