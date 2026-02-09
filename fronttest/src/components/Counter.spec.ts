import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import Counter from './Counter.vue'

describe('Counter', () => {
  it('renders initial count of 0', () => {
    const wrapper = mount(Counter)
    expect(wrapper.find('[data-testid="count"]').text()).toBe('0')
  })

  it('increments count when + is clicked', async () => {
    const wrapper = mount(Counter)
    await wrapper.find('[data-testid="increment"]').trigger('click')
    expect(wrapper.find('[data-testid="count"]').text()).toBe('1')
    await wrapper.find('[data-testid="increment"]').trigger('click')
    expect(wrapper.find('[data-testid="count"]').text()).toBe('2')
  })

  it('decrements count when − is clicked', async () => {
    const wrapper = mount(Counter)
    await wrapper.find('[data-testid="increment"]').trigger('click')
    await wrapper.find('[data-testid="increment"]').trigger('click')
    await wrapper.find('[data-testid="decrement"]').trigger('click')
    expect(wrapper.find('[data-testid="count"]').text()).toBe('1')
  })

  it('shows doubled value', async () => {
    const wrapper = mount(Counter)
    expect(wrapper.text()).toContain('Doble: 0')
    await wrapper.find('[data-testid="increment"]').trigger('click')
    expect(wrapper.text()).toContain('Doble: 2')
  })
})
