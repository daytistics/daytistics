import { mountSuspended } from '@nuxt/test-utils/runtime';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import SideBar from '~/components/dashboard/SideBar.vue';
import { findByAttribute } from '~/test/test-utils/selectors';

const mockGetTotalTokens = vi.fn();

vi.mock('~/composables/useEndpoints', () => ({
    default: vi.fn(() => ({
        payments: {
            getTotalTokens: mockGetTotalTokens,
        },
    })),
}));

describe('SideBar', () => {
    beforeEach(() => {
        vi.clearAllMocks();
        mockGetTotalTokens.mockResolvedValue(10000);
    });

    it('should render the sidebar', async () => {
        const wrapper = await mountSuspended(SideBar);
        expect(wrapper.html()).toContain('Home');
        expect(wrapper.html()).toContain('Suggestions');
        expect(wrapper.html()).toContain('Settings');
        expect(wrapper.html()).toContain('10.0k Tokens');
    });

    it('matches snapshot', async () => {});

    it('should navigate to / when clicking on the logo', async () => {});

    it("should navigate to /dashboard when clicking on the 'Home' link", async () => {});

    it("should navigate to /dashboard/suggestions when clicking on the 'Suggestions' link", async () => {});

    it("should navigate to /account/settings when clicking on the 'Settings' link", async () => {});

    it("should navigate to /account/tokens when clicking on the 'Tokens' link", async () => {});

    it('can be collapsed', async () => {
        const wrapper = await mountSuspended(SideBar);

        // Check if the sidebar is expanded
        expect(wrapper.html()).toContain('Home');
        expect(wrapper.html()).toContain('Suggestions');
        expect(wrapper.html()).toContain('Settings');
        expect(wrapper.html()).toContain('10.0k Tokens');

        const toggleButton = findByAttribute(wrapper, 'button', 'aria-label', 'Toggle Sidebar')[0];
        await toggleButton.trigger('click');

        wrapper.vm.$nextTick();

        // We check if 10.0k Tokens is not visible because that's the
        // only thing that fully disappears when the sidebar is collapsed
        expect(wrapper.html()).not.toContain('10.0k Tokens');
    });

    it('can be expanded', async () => {
        const wrapper = await mountSuspended(SideBar);

        // Collapse the sidebar
        const toggleButton = findByAttribute(wrapper, 'button', 'aria-label', 'Toggle Sidebar')[0];
        await toggleButton.trigger('click');

        wrapper.vm.$nextTick();

        // Check if the sidebar is collapsed
        expect(wrapper.html()).not.toContain('10.0k Tokens');

        // Expand the sidebar
        await toggleButton.trigger('click');

        wrapper.vm.$nextTick();

        // Check if the sidebar is expanded
        expect(wrapper.html()).toContain('Home');
        expect(wrapper.html()).toContain('Suggestions');
        expect(wrapper.html()).toContain('Settings');
        expect(wrapper.html()).toContain('10.0k Tokens');
    });

    it('should match snapshot when collapsed', async () => {});

    it('switches into a bottom bar when smaller than 768px', async () => {});

    it('switches back to a sidebar when larger than 768px', async () => {});

    it('should match snapshot when in bottom bar mode', async () => {});
});
