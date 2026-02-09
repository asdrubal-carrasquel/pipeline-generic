<script setup lang="ts">
import { ref } from 'vue'
import Counter from './components/Counter.vue'
import Welcome from './components/Welcome.vue'

const title = ref('CI/CD Vue App')
</script>

<template>
  <div class="app">
    <header class="header">
      <h1 data-testid="app-title">{{ title }}</h1>
    </header>
    <main class="main">
      <Welcome msg="Pipeline Generic" />
      <Counter />
    </main>
  </div>
</template>

<style scoped>
.app {
  max-width: 800px;
  margin: 0 auto;
  padding: 1rem;
}
.header {
  margin-bottom: 2rem;
}
.header h1 {
  font-size: 1.5rem;
  color: var(--color-heading);
}
.main {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}
</style>
