<script setup lang="ts">
import { RouterLink, RouterView } from "vue-router";
</script>

<template>
  <div class="layout">
    <header class="header">
      <h1 class="brand">Shortlink</h1>
      <nav class="nav">
        <RouterLink to="/">创建</RouterLink>
        <RouterLink to="/links">列表</RouterLink>
      </nav>
    </header>
    <main class="main">
      <RouterView />
    </main>
  </div>
</template>
