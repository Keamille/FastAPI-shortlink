import type { ApiResponse, CreateLinkBody, LinkItem, LinkListData } from "@/types/link";

import { http } from "./http";

/** Call backends after you implement the APIs. */

export async function createLink(body: CreateLinkBody): Promise<ApiResponse<LinkItem>> {
  const { data } = await http.post<ApiResponse<LinkItem>>("/api/v1/links", body);
  return data;
}

export async function listLinks(
  page = 1,
  pageSize = 20,
): Promise<ApiResponse<LinkListData>> {
  const { data } = await http.get<ApiResponse<LinkListData>>("/api/v1/links", {
    params: { page, page_size: pageSize },
  });
  return data;
}

export async function getLink(code: string): Promise<ApiResponse<LinkItem>> {
  const { data } = await http.get<ApiResponse<LinkItem>>(`/api/v1/links/${code}`);
  return data;
}

export async function deleteLink(code: string): Promise<ApiResponse<null>> {
  const { data } = await http.delete<ApiResponse<null>>(`/api/v1/links/${code}`);
  return data;
}
