import {describe, it, expect} from 'vitest';
import {mountSuspended} from '@nuxt/test-utils/runtime';
import Card from '~/components/global/Card.vue';


describe("GlobalCard", () => {
    it("should render the card", async () => {
        const wrapper = await mountSuspended(Card, {
            slots: {
                default: () => `
            <template>
                <h1>Card Title</h1>
                <p>Card Description</p>
            </template>
            `,
            }
        });

        expect(wrapper.html()).toContain("Card Title");
        expect(wrapper.html()).toContain("Card Description");
    });

    it("clicking on the element emits a click event if clickable prop is true", async () => {
        const wrapper = await mountSuspended(Card, {
            props: {
                clickable: true,
            },
        });

        await wrapper.trigger("click");
        expect(wrapper.emitted("click")).toBeTruthy();
    });
})