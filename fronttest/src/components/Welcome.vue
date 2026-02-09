<script setup lang="ts">
defineProps<{
  msg: string
}>()
</script>

<template>
  <section class="welcome" data-testid="welcome">
    <h2>{{ msg }}</h2>
    <p>App de prueba para el flujo CI/CD con tests unitarios y funcionales.</p>
  </section>
</template>

<style scoped>
.welcome h2 {
  color: var(--color-accent);
  margin-bottom: 0.5rem;
}
.welcome p {
  color: var(--color-text);
}
</style>
