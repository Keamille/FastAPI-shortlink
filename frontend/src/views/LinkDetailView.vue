<script setup lang="ts">
import { onMounted, ref, watch } from "vue";
import { RouterLink, useRouter } from "vue-router";

import { deleteLink, getLink } from "@/api/links";
import type { LinkItem } from "@/types/link";
import { getErrorMessage } from "@/utils/error";

const props = defineProps<{ code: string }>();
const router = useRouter();

const item = ref<LinkItem | null>(null);
const loading = ref(false);
const error = ref("");
const copied = ref(false);

function formatTime(ts: number): string {
  return new Date(ts * 1000).toLocaleString();
}

async function load() {
  loading.value = true;
  error.value = "";
  item.value = null;
  copied.value = false;
  try {
    const res = await getLink(props.code);
    item.value = res.data;
  } catch (err) {
    error.value = getErrorMessage(err, "加载详情失败");
  } finally {
    loading.value = false;
  }
}

async function copyShortUrl() {
  if (!item.value?.short_url) return;
  try {
    await navigator.clipboard.writeText(item.value.short_url);
    copied.value = true;
  } catch {
    error.value = "复制失败，请手动选择短链";
  }
}

async function onDelete() {
  if (!confirm(`确定删除短链 ${props.code}？`)) return;
  try {
    await deleteLink(props.code);
    await router.push("/links");
  } catch (err) {
    error.value = getErrorMessage(err, "删除失败");
  }
}

onMounted(() => {
  void load();
});

watch(
  () => props.code,
  () => {
    void load();
  },
);
</script>

<template>
  <section class="panel">
    <div class="row-between">
      <h2>短链详情</h2>
      <RouterLink to="/links">返回列表</RouterLink>
    </div>

    <p v-if="loading" class="muted">加载中…</p>
    <p v-if="error" class="error">{{ error }}</p>

    <template v-if="item">
      <dl class="detail">
        <div>
          <dt>短码</dt>
          <dd><code>{{ item.code }}</code></dd>
        </div>
        <div>
          <dt>短链</dt>
          <dd>
            <a :href="item.short_url" target="_blank" rel="noopener">{{ item.short_url }}</a>
          </dd>
        </div>
        <div>
          <dt>原链</dt>
          <dd>
            <a :href="item.original_url" target="_blank" rel="noopener">{{ item.original_url }}</a>
          </dd>
        </div>
        <div>
          <dt>点击次数</dt>
          <dd>{{ item.clicks }}</dd>
        </div>
        <div>
          <dt>创建时间</dt>
          <dd>{{ formatTime(item.created_at) }}</dd>
        </div>
        <div>
          <dt>TTL 剩余（秒）</dt>
          <dd>{{ item.ttl_seconds ?? "—" }}</dd>
        </div>
      </dl>

      <div class="actions">
        <button type="button" class="secondary" @click="copyShortUrl">
          {{ copied ? "已复制" : "复制短链" }}
        </button>
        <button type="button" class="secondary" @click="load">刷新</button>
        <button type="button" class="danger" @click="onDelete">删除</button>
      </div>
    </template>
  </section>
</template>
