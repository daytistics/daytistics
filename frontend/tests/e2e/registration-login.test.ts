import { expect, test } from '@nuxt/test-utils/playwright';
import type { plugins } from 'chart.js';

test('test', async ({ page, goto }) => {
    await goto('/', { waitUntil: 'hydration' });
    await expect(
        page.getByRole('heading', { name: 'Key Features' })
    ).toHaveText('Key Features');
});
