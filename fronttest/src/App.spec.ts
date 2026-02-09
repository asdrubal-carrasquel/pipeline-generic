import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import App from './App.vue'

describe('App', () => {
  it('renders app title', () => {
    const wrapper = mount(App)
    expect(wrapper.find('[data-testid="app-title"]').text()).toBe('CI/CD Vue App')
  })

  it('renders Welcome and Counter', () => {
    const wrapper = mount(App)
    expect(wrapper.find('[data-testid="welcome"]').exists()).toBe(true)
    expect(wrapper.find('[data-testid="counter"]').exists()).toBe(true)
  })
})
