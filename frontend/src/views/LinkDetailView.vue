<script setup lang="ts">
defineProps<{ code: string }>();
</script>

<template>
  <section class="panel">
    <h2>短链详情</h2>
    <p>
      code: <code>{{ code }}</code>
    </p>
    <p class="muted">TODO: 调用 getLink(code)，展示点击数与过期信息。</p>
  </section>
</template>
