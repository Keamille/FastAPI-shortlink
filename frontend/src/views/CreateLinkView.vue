<script setup lang="ts">
import { ref } from "vue";

const url = ref("");
const customCode = ref("");
const ttlSeconds = ref<number | null>(null);
const hint = ref("实现 createLink 后，在此提交并展示 short_url。");

function onSubmit() {
  hint.value = "TODO: 调用 src/api/links.ts 的 createLink（可带 custom_code）";
}
</script>

<template>
  <section class="panel">
    <h2>创建短链</h2>
    <p class="muted">{{ hint }}</p>
    <label>
      长链接
      <input v-model="url" type="url" placeholder="https://example.com/..." style="width: 100%" />
    </label>
    <label>
      自定义短码（可选）
      <input
        v-model="customCode"
        type="text"
        maxlength="32"
        placeholder="留空则自动生成；仅 0-9a-zA-Z，3～32 位"
        style="width: 100%"
      />
    </label>
    <label>
      TTL（秒，可选）
      <input v-model.number="ttlSeconds" type="number" min="1" placeholder="留空表示不过期" />
    </label>
    <button type="button" @click="onSubmit">创建</button>
  </section>
</template>
