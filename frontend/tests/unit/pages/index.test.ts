import { describe, it, expect, vi, afterEach, beforeEach } from 'vitest';
import { mountSuspended } from '@nuxt/test-utils/runtime';
import index from '~/pages/index.vue';
import number from '~/pages/number.vue';
import { config } from '@vue/test-utils';

// ! Testing if component can mount
describe('index', () => {
    it('can mount', async () => {
        const component = await mountSuspended(index);
        expect(component).toBeTruthy();
    });
});

describe('number', () => {
    it('can mount', async () => {
        vi.mock('vue', async () => {
            const actual = await vi.importActual('vue');
            return {
                ...actual,
                onMounted: vi.fn((fn) => fn()),
            };
        });

        const randomSpy = vi.spyOn(Math, 'random').mockReturnValue(0.5);

        const wrapper = await mountSuspended(number);

        expect(wrapper.text()).toBe('Number: 0.5');
        expect(randomSpy).toHaveBeenCalled();

        randomSpy.mockRestore();
    });
});
