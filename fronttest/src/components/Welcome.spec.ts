import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import Welcome from './Welcome.vue'

describe('Welcome', () => {
  it('renders message prop', () => {
    const wrapper = mount(Welcome, {
      props: { msg: 'Pipeline Generic' },
    })
    expect(wrapper.find('h2').text()).toBe('Pipeline Generic')
  })

  it('has welcome section with testid', () => {
    const wrapper = mount(Welcome, {
      props: { msg: 'Test' },
    })
    expect(wrapper.find('[data-testid="welcome"]').exists()).toBe(true)
  })
})
