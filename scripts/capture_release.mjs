#!/usr/bin/env node
// Captures de l'état courant uniquement : aucune mutation IAM, aucun storageState.
import { chromium, expect } from '@playwright/test';
import { readFile, mkdir, access } from 'node:fs/promises';

const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({ viewport: { width: 1440, height: 900 } });
const page = await context.newPage();
async function capture(file) {
  await expect.poll(async () => (await page.locator('body').innerText()).trim().length).toBeGreaterThan(5);
  const text = await page.locator('body').innerText();
  // Les écrans de login ne sont capturés qu'avant toute saisie.
  const populated = await page.locator('input').evaluateAll(inputs => inputs.some(
    input => ['text', 'email', 'password', 'tel', 'number'].includes(input.type) && input.value.length > 0,
  ));
  if (populated || /recovery code|QR code|client secret|access_token|refresh_token|otpauth:/i.test(text)) {
    throw new Error('Capture bloquée par le contrôle des données sensibles');
  }
  try { await access(file); console.log(`PRESERVED ${file}`); return; } catch {}
  await page.screenshot({ path: file, fullPage: false });
  console.log(`CAPTURE ${file}`);
}
try {
  await mkdir('captures/tp1', { recursive: true });
  await page.goto('http://localhost:3000/login');
  await page.getByRole('button', { name: 'Log in', exact: true }).waitFor();
  await capture('captures/tp1/03-grafana-login.png');
  await page.goto('http://localhost:9000/if/flow/default-authentication-flow/');
  await page.locator('input:not([type=hidden])').first().waitFor();
  await capture('captures/tp1/02-authentik-login.png');

  // Utilisation du compte local de secours existant, sans afficher son mot de passe.
  const env = Object.fromEntries((await readFile('.env', 'utf8')).split('\n')
    .filter(line => line.includes('=') && !line.startsWith('#'))
    .map(line => [line.slice(0, line.indexOf('=')), line.slice(line.indexOf('=') + 1)]));
  await page.goto('http://localhost:3000/login');
  await page.getByLabel('Email or username').fill('admin');
  await page.getByLabel('Password', { exact: true }).fill(env.GRAFANA_ADMIN_PASSWORD);
  await page.getByRole('button', { name: 'Log in', exact: true }).click();
  await page.waitForURL(url => !url.pathname.startsWith('/login'));
  await page.goto('http://localhost:3000/org/users');
  await page.getByRole('row').filter({ hasText: 'alice' }).waitFor({ timeout: 30000 });
  for (const login of ['bob', 'charlie']) {
    await page.getByRole('row').filter({ hasText: login }).waitFor();
  }
  await capture('captures/tp2/10-grafana-users.png');
  await page.getByText('Organization users', { exact: true }).click();
  await page.getByRole('row').filter({ hasText: 'alice' }).waitFor();
  await expect(page.getByRole('row').filter({ hasText: 'alice' })).toContainText('Viewer');
  await expect(page.getByRole('row').filter({ hasText: 'bob' })).toContainText('Editor');
  await expect(page.getByRole('row').filter({ hasText: 'charlie' })).toContainText('Admin');
  await capture('captures/tp2/10a-grafana-roles.png');
} finally {
  await context.close();
  await browser.close();
}
