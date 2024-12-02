import { it, describe, expect, vi, beforeEach } from 'vitest';
import { mockNuxtImport, mountSuspended } from '@nuxt/test-utils/runtime';
import { flushPromises } from '@vue/test-utils';
import CreateDaytisticContent from '~~/components/dashboard/CreateDaytisticContent.vue';
import DatePicker from '~~/components/global/DatePicker.vue';

// Create mocks
const mockError = vi.fn();
const mockSuccess = vi.fn();
const mockCreateDaytistic = vi.fn();
const mockNavigateTo = vi.fn();

// Mock vue-toastification
vi.mock('vue-toastification', () => ({
    useToast: () => ({
        error: mockError,
        success: mockSuccess,
    }),
}));

// Mock useEndpoints
vi.mock('~/composables/useEndpoints', () => ({
    default: vi.fn(() => ({
        createDaytistic: mockCreateDaytistic,
    })),
}));

const { navigateTo } = vi.hoisted(() => {
    return {
        navigateTo: vi.fn(),
    };
});

mockNuxtImport('navigateTo', () => navigateTo);

describe('CreateDaytisticContent', () => {
    beforeEach(() => {
        vi.clearAllMocks();
        // Setup successful API response
        mockCreateDaytistic.mockResolvedValue({
            status: 201,
            _data: { id: '123' },
        });
    });

    it('should render the dialog', async () => {
        const wrapper = await mountSuspended(CreateDaytisticContent);
        expect(wrapper.findComponent(DatePicker).exists()).toBe(true);
        expect(wrapper.text()).toContain('What day are we talking about here?');
        expect(wrapper.find('button').text()).toBe('Add');
    });

    it('matches snapshot', async () => {
        const wrapper = await mountSuspended(CreateDaytisticContent);
        await flushPromises();
        expect(wrapper.html()).toMatchSnapshot();
    });

    it('shows error toast when date is not selected', async () => {
        const wrapper = await mountSuspended(CreateDaytisticContent);

        // Trigger form submission
        await wrapper.find('form').trigger('submit.prevent');
        await flushPromises();

        // Verify toast was called
        expect(mockError).toHaveBeenCalledWith('Please select a date');
        expect(mockCreateDaytistic).not.toHaveBeenCalled();
    });

    it('submits form successfully when date is selected', async () => {
        const wrapper = await mountSuspended(CreateDaytisticContent);
        const testDate = new Date('2024-01-01');

        // First, set the modelValue prop
        await wrapper.findComponent(DatePicker).setValue(testDate);

        // Then emit the update event
        await wrapper.findComponent(DatePicker).vm.$emit('update', testDate);

        // Wait for Vue to process the updates
        await wrapper.vm.$nextTick();

        // Trigger form submission
        await wrapper.find('form').trigger('submit');

        // Wait for all promises to resolve
        await flushPromises();

        // Verify API call was made with correct date
        expect(mockCreateDaytistic).toHaveBeenCalledWith(testDate);

        // FOR AI: Failes with "expected "spy" to be called at least once"
        expect(navigateTo).toHaveBeenCalled();
        expect(mockSuccess).toHaveBeenCalled();
    });

    it('handles API error properly', async () => {
        const wrapper = await mountSuspended(CreateDaytisticContent);
        const testDate = new Date('2024-01-01');
        const errorMessage = 'API Error';

        // Setup error response
        mockCreateDaytistic.mockRejectedValueOnce({
            response: {
                _data: { detail: errorMessage },
            },
        });

        // Simulate date selection and submission
        await wrapper.findComponent(DatePicker).vm.$emit('update', testDate);
        await wrapper.vm.$nextTick();
        await wrapper.find('form').trigger('submit.prevent');
        await flushPromises();

        // Verify error handling
        expect(mockError).toHaveBeenCalled();
        expect(mockNavigateTo).not.toHaveBeenCalled();
    });
});
