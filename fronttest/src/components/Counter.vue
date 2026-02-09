<script setup lang="ts">
import { ref, computed } from 'vue'

const count = ref(0)
const doubled = computed(() => count.value * 2)

function increment() {
  count.value += 1
}

function decrement() {
  count.value -= 1
}
</script>

<template>
  <section class="counter" data-testid="counter">
    <h2>Contador</h2>
    <p class="count" data-testid="count">{{ count }}</p>
    <p class="doubled">Doble: {{ doubled }}</p>
    <div class="actions">
      <button type="button" data-testid="decrement" @click="decrement">−</button>
      <button type="button" data-testid="increment" @click="increment">+</button>
    </div>
  </section>
</template>

<style scoped>
.counter h2 {
  color: var(--color-heading);
  margin-bottom: 0.5rem;
}
.count {
  font-size: 2rem;
  font-weight: 700;
  color: var(--color-accent);
}
.doubled {
  margin-bottom: 1rem;
  color: var(--color-text);
}
.actions {
  display: flex;
  gap: 0.5rem;
}
.actions button {
  padding: 0.5rem 1rem;
  font-size: 1.25rem;
  cursor: pointer;
  border: 1px solid var(--color-accent);
  border-radius: 4px;
  background: #fff;
  color: var(--color-accent);
}
.actions button:hover {
  background: var(--color-accent);
  color: #fff;
}
</style>
