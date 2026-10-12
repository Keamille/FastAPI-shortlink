import { defineStore } from "pinia";
import { ref } from "vue";

import { listLinks } from "@/api/links";
import type { LinkItem } from "@/types/link";
import { getErrorMessage } from "@/utils/error";

/** Shared list cache; views may also fetch directly. */
export const useLinksStore = defineStore("links", () => {
  const items = ref<LinkItem[]>([]);
  const total = ref(0);
  const loading = ref(false);
  const error = ref("");

  async function fetchPage(page = 1, pageSize = 20) {
    loading.value = true;
    error.value = "";
    try {
      const res = await listLinks(page, pageSize);
      items.value = res.data.items;
      total.value = res.data.total;
    } catch (err) {
      error.value = getErrorMessage(err, "加载列表失败");
      throw err;
    } finally {
      loading.value = false;
    }
  }

  return { items, total, loading, error, fetchPage };
});
