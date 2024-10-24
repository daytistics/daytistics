import { mount } from '@vue/test-utils';
import { describe, it, expect, beforeEach, vitest, vi } from 'vitest';
import DaytisticsList from '~/components/dashboard/DaytisticsList.vue';
import { mountSuspended } from '@nuxt/test-utils/runtime';
import { resolve } from 'chart.js/helpers';

describe('YourDaytistics Component', () => {
    let wrapper: any;

    beforeEach(async () => {
        wrapper = await mountSuspended(DaytisticsList, {
            props: {
                daytistics: [
                    {
                        id: 1,
                        date: '2024-10-19',
                        total_activities: 3,
                        total_duration: 120,
                    },
                ],
                totalPages: 1,
            },
        });
    });

    it('renders daytistics correctly', () => {
        const date = new Date('2024-10-19');
        expect(wrapper.text()).toContain('Your Daytistics');
        expect(wrapper.text()).toContain(date.toLocaleDateString());
        expect(wrapper.text()).toContain('3 Activities / 2h');
    });

    it('shows a message when no daytistics are found', async () => {
        await wrapper.setProps({ daytistics: [] });
        expect(wrapper.text()).toContain(
            "We couldn't find any daytistics for you."
        );
    });

    // it('calls the API when changing the page', async () => {
    //     const mockLoadPage = vitest.spyOn(wrapper.vm, 'loadPage');
    //     await wrapper.vm.currentPage = 2;
    //     wrapper.vm.$nextTick();
    //     expect(mockLoadPage).toHaveBeenCalledWith(2);
    // });
});
