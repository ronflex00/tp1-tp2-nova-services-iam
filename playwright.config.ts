import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: './tests/e2e',
  timeout: 60 * 60 * 1000,
  expect: { timeout: 15_000 },
  fullyParallel: false,
  workers: 1,
  reporter: [['line'], ['html', { outputFolder: 'playwright-report', open: 'never' }]],
  use: {
    baseURL: process.env.TP2_GRAFANA_URL ?? 'http://localhost:3000',
    viewport: { width: 1440, height: 900 },
    locale: 'fr-FR',
    colorScheme: 'dark',
    screenshot: 'off',
    // Les traces peuvent contenir les requêtes OAuth et les saisies MFA.
    trace: 'off',
  },
});
