import { defineStore } from "pinia";
import { ref } from "vue";

import type { LinkItem } from "@/types/link";

/** Optional Pinia store — fill when wiring list/create flows. */
export const useLinksStore = defineStore("links", () => {
  const items = ref<LinkItem[]>([]);
  const loading = ref(false);

  return { items, loading };
});
