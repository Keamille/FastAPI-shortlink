<script setup lang="ts">
import { ref } from "vue";
import { RouterLink } from "vue-router";

import { createLink } from "@/api/links";
import type { LinkItem } from "@/types/link";
import { getErrorMessage } from "@/utils/error";

const url = ref("");
const customCode = ref("");
const ttlSeconds = ref<number | null>(null);
const loading = ref(false);
const error = ref("");
const result = ref<LinkItem | null>(null);
const copied = ref(false);

async function onSubmit() {
  error.value = "";
  result.value = null;
  copied.value = false;

  const trimmed = url.value.trim();
  if (!trimmed) {
    error.value = "请填写长链接";
    return;
  }

  loading.value = true;
  try {
    const body = {
      url: trimmed,
      custom_code: customCode.value.trim() || null,
      ttl_seconds: ttlSeconds.value || null,
    };
    const res = await createLink(body);
    result.value = res.data;
  } catch (err) {
    error.value = getErrorMessage(err, "创建失败");
  } finally {
    loading.value = false;
  }
}

async function copyShortUrl() {
  if (!result.value?.short_url) return;
  try {
    await navigator.clipboard.writeText(result.value.short_url);
    copied.value = true;
  } catch {
    error.value = "复制失败，请手动选择短链";
  }
}
</script>

<template>
  <section class="panel">
    <h2>创建短链</h2>
    <p class="muted">填写长链接；自定义短码与 TTL 可选。</p>

    <label class="field">
      <span>长链接</span>
      <input v-model="url" type="url" placeholder="https://example.com/..." />
    </label>

    <label class="field">
      <span>自定义短码（可选）</span>
      <input
        v-model="customCode"
        type="text"
        maxlength="32"
        placeholder="留空则自动生成；仅 0-9a-zA-Z，3～32 位"
      />
    </label>

    <label class="field">
      <span>TTL（秒，可选）</span>
      <input v-model.number="ttlSeconds" type="number" min="1" placeholder="留空则默认 7 天" />
    </label>

    <button type="button" :disabled="loading" @click="onSubmit">
      {{ loading ? "创建中…" : "创建" }}
    </button>

    <p v-if="error" class="error">{{ error }}</p>

    <div v-if="result" class="result">
      <p><strong>短码：</strong>{{ result.code }}</p>
      <p>
        <strong>短链：</strong>
        <a :href="result.short_url" target="_blank" rel="noopener">{{ result.short_url }}</a>
      </p>
      <div class="actions">
        <button type="button" class="secondary" @click="copyShortUrl">
          {{ copied ? "已复制" : "复制短链" }}
        </button>
        <RouterLink class="link-btn" :to="`/links/${result.code}`">查看详情</RouterLink>
      </div>
    </div>
  </section>
</template>
