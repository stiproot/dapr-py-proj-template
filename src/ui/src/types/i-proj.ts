
export interface IProjSummary {
  utc_updated_timestamp: string | null;
}

export interface IProj {
  id: string | null;
  name: string | null;
  tag: string | null;
  utc_created_timestamp: string;
  color: string | null;
  is_pinned: string;
  description: string | null;
  user_id: string;
  utc_updated_timestamp: string | null;
  summary: IProjSummary | null;
}