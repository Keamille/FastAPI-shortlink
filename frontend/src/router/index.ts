import { createRouter, createWebHistory } from "vue-router";

import CreateLinkView from "@/views/CreateLinkView.vue";
import LinkDetailView from "@/views/LinkDetailView.vue";
import LinkListView from "@/views/LinkListView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: "/", name: "create", component: CreateLinkView },
    { path: "/links", name: "links", component: LinkListView },
    { path: "/links/:code", name: "link-detail", component: LinkDetailView, props: true },
  ],
});

export default router;
