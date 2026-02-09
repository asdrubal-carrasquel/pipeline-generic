import { test, expect } from '@playwright/test'

test.describe('Vue App', () => {
  test('shows app title and welcome section', async ({ page }) => {
    await page.goto('/')
    await expect(page.getByTestId('app-title')).toHaveText('CI/CD Vue App')
    await expect(page.getByTestId('welcome')).toBeVisible()
    await expect(page.getByRole('heading', { name: 'Pipeline Generic' })).toBeVisible()
  })

  test('counter starts at 0', async ({ page }) => {
    await page.goto('/')
    await expect(page.getByTestId('count')).toHaveText('0')
  })

  test('counter increments and decrements', async ({ page }) => {
    await page.goto('/')
    await page.getByTestId('increment').click()
    await expect(page.getByTestId('count')).toHaveText('1')
    await page.getByTestId('increment').click()
    await expect(page.getByTestId('count')).toHaveText('2')
    await page.getByTestId('decrement').click()
    await expect(page.getByTestId('count')).toHaveText('1')
  })
})
