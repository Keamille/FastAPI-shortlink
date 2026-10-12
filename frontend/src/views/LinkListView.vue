<script setup lang="ts">
import { onMounted, ref } from "vue";
import { RouterLink } from "vue-router";

import { deleteLink, listLinks } from "@/api/links";
import type { LinkItem } from "@/types/link";
import { getErrorMessage } from "@/utils/error";

const items = ref<LinkItem[]>([]);
const total = ref(0);
const page = ref(1);
const pageSize = ref(20);
const loading = ref(false);
const error = ref("");

function formatTime(ts: number): string {
  return new Date(ts * 1000).toLocaleString();
}

async function load() {
  loading.value = true;
  error.value = "";
  try {
    const res = await listLinks(page.value, pageSize.value);
    items.value = res.data.items;
    total.value = res.data.total;
  } catch (err) {
    error.value = getErrorMessage(err, "加载列表失败");
  } finally {
    loading.value = false;
  }
}

async function onDelete(code: string) {
  if (!confirm(`确定删除短链 ${code}？`)) return;
  try {
    await deleteLink(code);
    await load();
  } catch (err) {
    error.value = getErrorMessage(err, "删除失败");
  }
}

function prevPage() {
  if (page.value <= 1) return;
  page.value -= 1;
  void load();
}

function nextPage() {
  if (page.value * pageSize.value >= total.value) return;
  page.value += 1;
  void load();
}

onMounted(() => {
  void load();
});
</script>

<template>
  <section class="panel">
    <div class="row-between">
      <h2>短链列表</h2>
      <button type="button" class="secondary" :disabled="loading" @click="load">刷新</button>
    </div>

    <p v-if="error" class="error">{{ error }}</p>
    <p v-if="loading" class="muted">加载中…</p>
    <p v-else-if="!items.length" class="muted">暂无短链，先去创建一条吧。</p>

    <div v-else class="table-wrap">
      <table>
        <thead>
          <tr>
            <th>短码</th>
            <th>原链</th>
            <th>点击</th>
            <th>创建时间</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in items" :key="item.code">
            <td>
              <RouterLink :to="`/links/${item.code}`">{{ item.code }}</RouterLink>
            </td>
            <td class="url-cell" :title="item.original_url">{{ item.original_url }}</td>
            <td>{{ item.clicks }}</td>
            <td>{{ formatTime(item.created_at) }}</td>
            <td class="ops">
              <a :href="item.short_url" target="_blank" rel="noopener">打开</a>
              <button type="button" class="danger" @click="onDelete(item.code)">删除</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-if="total > 0" class="pager">
      <button type="button" class="secondary" :disabled="page <= 1 || loading" @click="prevPage">
        上一页
      </button>
      <span class="muted">第 {{ page }} 页 · 共 {{ total }} 条</span>
      <button
        type="button"
        class="secondary"
        :disabled="page * pageSize >= total || loading"
        @click="nextPage"
      >
        下一页
      </button>
    </div>
  </section>
</template>
