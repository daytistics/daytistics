import { it, describe, expect, vi, beforeEach } from 'vitest';
import { mockNuxtImport, mountSuspended } from '@nuxt/test-utils/runtime';
import { flushPromises } from '@vue/test-utils';
import DaytisticsList from '~/components/dashboard/DaytisticsList.vue';
import type { Daytistic } from '~/types/daytistics';
import { findByAttribute, findByText } from '~/test/test-utils/selectors';
import { generateDaytistics } from '~/test/test-utils/mocks';

const DAYTISTICS_COUNT = 9;
const mockListDaytistics = vi.fn();

let daytistics: undefined | Daytistic[] = undefined;

vi.mock('~/composables/useEndpoints', () => ({
    default: vi.fn(() => ({
        listDaytistics: mockListDaytistics,
    })),
}));

describe('DaytisticsList', () => {
    beforeEach(() => {
        vi.clearAllMocks();
        daytistics = generateDaytistics(DAYTISTICS_COUNT);

        mockListDaytistics.mockResolvedValue({
            count: DAYTISTICS_COUNT,
            items: daytistics,
        });
    });

    it('should render the list', async () => {
        const wrapper = await mountSuspended(DaytisticsList);
        await flushPromises();

        expect(mockListDaytistics).toHaveBeenCalledTimes(1);
        expect(wrapper.text()).toContain('Your Daytistics');
        expect(wrapper.text()).toContain(`1 of 2`);
        expect(wrapper.text()).toContain('Add New');
        expect(wrapper.text()).toContain('Next');
        expect(wrapper.text()).toContain('Previous');

        for (const daytistic of daytistics?.slice(0, 5)!) {
            const date = new Date(daytistic.date).toLocaleDateString();
            expect(wrapper.text()).toContain(date);
        }
    });

    it('matches snapshot', async () => {
        const wrapper = await mountSuspended(DaytisticsList);
        await flushPromises();
        expect(wrapper.html()).toMatchSnapshot();
    });

    it("switches to the next page when the 'next' button is clicked", async () => {
        const wrapper = await mountSuspended(DaytisticsList);
        await flushPromises();

        const nextButton = findByText(wrapper, 'button', /Next/).at(0);
        await nextButton!.trigger('click');

        await flushPromises();

        expect(mockListDaytistics).toHaveBeenCalledTimes(2);
        expect(wrapper.text()).toContain('2 of 2');

        for (const daytistic of daytistics?.slice(5, 10)!) {
            const date = new Date(daytistic.date).toLocaleDateString();
            expect(wrapper.text()).toContain(date);
        }
    });

    it("switches to the previous page when the 'previous' button is clicked", async () => {
        const wrapper = await mountSuspended(DaytisticsList);

        await flushPromises();

        const nextButton = findByText(wrapper, 'button', /Next/).at(0);
        await nextButton!.trigger('click');

        await flushPromises();

        const previousButton = findByText(wrapper, 'button', /Previous/).at(0);
        await previousButton!.trigger('click');

        await flushPromises();

        expect(mockListDaytistics).toHaveBeenCalledTimes(3);
        expect(wrapper.text()).toContain('1 of 2');

        for (const daytistic of daytistics?.slice(0, 5)!) {
            const date = new Date(daytistic.date).toLocaleDateString();
            expect(wrapper.text()).toContain(date);
        }
    });

    it("opens the 'CreateDaytisticDialog' when the 'Add Daytistic' button is clicked", async () => {
        const wrapper = await mountSuspended(DaytisticsList);
        await flushPromises();

        const addButton = findByText(wrapper, 'button', /Add New/).at(0);
        await addButton!.trigger('click');

        wrapper.vm.$nextTick();

        expect(findByAttribute(wrapper, 'span', 'data-dialog-open-test', 'true').length).toBe(1);
    });
});
