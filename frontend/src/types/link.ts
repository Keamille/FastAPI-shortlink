/** Align with backend Pydantic schemas (docs/DEVELOPMENT.md). */

export interface LinkItem {
  code: string;
  original_url: string;
  short_url: string;
  created_at: number;
  ttl_seconds: number | null;
  clicks: number;
}

export interface ApiResponse<T> {
  code: number;
  message: string;
  data: T;
}

export interface LinkListData {
  items: LinkItem[];
  total: number;
  page: number;
  page_size: number;
}

export interface CreateLinkBody {
  url: string;
  ttl_seconds?: number | null;
}
