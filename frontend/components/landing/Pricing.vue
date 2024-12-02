<script setup lang="ts">
import { Bird, Coins, Handshake, Server } from 'lucide-vue-next';
import { ref } from 'vue';

const pricingPlans = ref([
    {
        popular: true,
        type: 'Free',
        title: `It's totally free`,
        price: '0$',
        button: {
            text: 'Default Plan',
        },
        icon: Bird,
        features: [
            { isChecked: true, text: 'Up to 1 User' },
            { isChecked: true, text: '100k free tokens/month' },
            { isChecked: true, text: 'Visualizations' },
            { isChecked: true, text: 'Free Updates' },
            { isChecked: true, text: 'Data export' },
            { isChecked: false, text: 'Permanent Data Backup' },
            { isChecked: false, text: 'Early Access' },
        ],
    },
    {
        type: 'Premium',
        title: `Pay-As-You-Go`,
        price: '29$',
        discountPrice: '39$',
        button: {
            text: 'Get the plan',
        },
        icon: Handshake,
        features: [
            { isChecked: true, text: 'Up to 1 User' },
            { isChecked: true, text: '100k free tokens/month' },
            { isChecked: true, text: 'Visualizations' },
            { isChecked: true, text: 'Free Updates' },
            { isChecked: true, text: 'Data export' },
            { isChecked: true, text: 'Permanent Data Backup' },
            { isChecked: false, text: 'Early Access' },
        ],
    },
    {
        type: 'Donator',
        title: `Free with $50+ donation`,
        price: '59$',
        discountPrice: '99$',
        button: {
            text: 'Donate now',
        },
        icon: Coins,
        features: [
            { isChecked: true, text: 'Up to 1 User' },
            { isChecked: true, text: '100k free tokens/month' },
            { isChecked: true, text: 'Visualizations' },
            { isChecked: true, text: 'Free Updates' },
            { isChecked: true, text: 'Data export' },
            { isChecked: true, text: 'Permanent Data Backup' },
            { isChecked: true, text: 'Early Access' },
        ],
    },
    {
        type: 'Self-Hosting',
        title: `Do it yourself`,
        price: '59$',
        discountPrice: '99$',
        button: {
            text: 'Download now',
        },
        icon: Server,
        features: [
            { isChecked: true, text: 'Up to 1 User' },
            { isChecked: true, text: '100k free tokens/month' },
            { isChecked: true, text: 'Visualizations' },
            { isChecked: true, text: 'Free Updates' },
            { isChecked: true, text: 'Data export' },
            { isChecked: true, text: 'Permanent Data Backup' },
            { isChecked: true, text: 'Early Access' },
        ],
    },
]);
</script>

<template>
    <!-- ====== Pricing Section Start -->
    <section class="relative z-20 overflow-hidden bg-white pt-20 pb-12 lg:pt-[120px] lg:pb-[90px]">
        <div class="container mx-auto">
            <div class="flex flex-wrap -mx-4">
                <div class="w-full px-4">
                    <div class="mx-auto mb-[60px] max-w-[600px] text-center">
                        <span class="block mb-2 text-lg font-semibold text-primary">
                            Our Pricing Plans
                        </span>
                        <h2
                            class="mb-4 text-3xl leading-[1.208] font-bold text-dark sm:text-4xl md:text-[40px]"
                        >
                            Ready to feel better?
                        </h2>
                        <p class="mx-auto max-w-[510px] text-base text-body-color">
                            Choose the plan that fits your needs best, or take full control by
                            hosting it yourself with our open-source version.
                        </p>
                    </div>
                </div>
            </div>

            <div class="flex flex-wrap justify-center -mx-4">
                <template
                    v-for="(plan, index) in pricingPlans"
                    :key="index"
                >
                    <div class="w-full px-4 md:w-1/2 xl:w-1/4">
                        <div class="p-8 bg-white border shadow-pricing-4 rounded-xl border-stroke">
                            <div class="pb-8 border-b border-stroke">
                                <div class="mb-[22px] flex justify-between">
                                    <div>
                                        <h3
                                            class="text-[22px] leading-7 mb-1 font-semibold text-dark"
                                        >
                                            {{ plan.type }}
                                        </h3>
                                        <p class="text-base text-body-color">
                                            {{ plan.title }}
                                        </p>
                                    </div>
                                    <component
                                        :is="plan.icon"
                                        class="h-[34px] w-auto text-primary"
                                    />
                                </div>

                                <button
                                    :class="{
                                        'flex w-full items-center justify-center rounded-md bg-dark py-[10px] text-base font-medium text-white hover:bg-body-color':
                                            plan.popular,
                                        'flex w-full items-center justify-center rounded-md bg-primary py-[10px] text-base font-medium text-white hover:bg-blue-dark':
                                            !plan.popular,
                                    }"
                                >
                                    {{ plan.button.text }}
                                </button>
                            </div>

                            <div class="pt-8">
                                <div class="space-y-[14px]">
                                    <template
                                        v-for="(item, index) in plan.features"
                                        :key="index"
                                    >
                                        <p class="flex items-center text-base text-dark">
                                            <span
                                                class="pr-[10px]"
                                                v-if="item.isChecked"
                                            >
                                                <svg
                                                    width="20"
                                                    height="20"
                                                    viewBox="0 0 20 20"
                                                    fill="none"
                                                    xmlns="http://www.w3.org/2000/svg"
                                                >
                                                    <g clip-path="url(#clip0_1676_331)">
                                                        <path
                                                            d="M10 0.5625C4.78125 0.5625 0.5625 4.78125 0.5625 10C0.5625 15.2188 4.78125 19.4688 10 19.4688C15.2188 19.4688 19.4688 15.2188 19.4688 10C19.4688 4.78125 15.2188 0.5625 10 0.5625ZM10 18.0625C5.5625 18.0625 1.96875 14.4375 1.96875 10C1.96875 5.5625 5.5625 1.96875 10 1.96875C14.4375 1.96875 18.0625 5.59375 18.0625 10.0312C18.0625 14.4375 14.4375 18.0625 10 18.0625Z"
                                                            fill="#22AD5C"
                                                        />
                                                        <path
                                                            d="M12.6874 7.09374L8.96868 10.7187L7.28118 9.06249C6.99993 8.78124 6.56243 8.81249 6.28118 9.06249C5.99993 9.34374 6.03118 9.78124 6.28118 10.0625L8.28118 12C8.46868 12.1875 8.71868 12.2812 8.96868 12.2812C9.21868 12.2812 9.46868 12.1875 9.65618 12L13.6874 8.12499C13.9687 7.84374 13.9687 7.40624 13.6874 7.12499C13.4062 6.84374 12.9687 6.84374 12.6874 7.09374Z"
                                                            fill="#22AD5C"
                                                        />
                                                    </g>
                                                    <defs>
                                                        <clipPath id="clip0_1676_331">
                                                            <rect
                                                                width="20"
                                                                height="20"
                                                                fill="white"
                                                            />
                                                        </clipPath>
                                                    </defs>
                                                </svg>
                                            </span>

                                            <span
                                                class="pr-[10px]"
                                                v-if="!item.isChecked"
                                            >
                                                <svg
                                                    width="20"
                                                    height="20"
                                                    viewBox="0 0 20 20"
                                                    fill="none"
                                                    xmlns="http://www.w3.org/2000/svg"
                                                >
                                                    <g clip-path="url(#clip0_1676_359)">
                                                        <path
                                                            d="M10 0.5625C4.78125 0.5625 0.5625 4.78125 0.5625 10C0.5625 15.2188 4.78125 19.4688 10 19.4688C15.2188 19.4688 19.4688 15.2188 19.4688 10C19.4688 4.78125 15.2188 0.5625 10 0.5625ZM10 18.0625C5.5625 18.0625 1.96875 14.4375 1.96875 10C1.96875 5.5625 5.5625 1.96875 10 1.96875C14.4375 1.96875 18.0625 5.59375 18.0625 10.0312C18.0625 14.4375 14.4375 18.0625 10 18.0625Z"
                                                            fill="#F56060"
                                                        />
                                                        <path
                                                            d="M12.875 7.09375C12.5938 6.8125 12.1563 6.8125 11.875 7.09375L10 9L8.09375 7.09375C7.8125 6.8125 7.375 6.8125 7.09375 7.09375C6.8125 7.375 6.8125 7.8125 7.09375 8.09375L9 10L7.09375 11.9062C6.8125 12.1875 6.8125 12.625 7.09375 12.9062C7.21875 13.0312 7.40625 13.125 7.59375 13.125C7.78125 13.125 7.96875 13.0625 8.09375 12.9062L10 11L11.9062 12.9062C12.0312 13.0312 12.2188 13.125 12.4063 13.125C12.5938 13.125 12.7812 13.0625 12.9062 12.9062C13.1875 12.625 13.1875 12.1875 12.9062 11.9062L11 10L12.9062 8.09375C13.1562 7.8125 13.1563 7.375 12.875 7.09375Z"
                                                            fill="#F56060"
                                                        />
                                                    </g>
                                                    <defs>
                                                        <clipPath id="clip0_1676_359">
                                                            <rect
                                                                width="20"
                                                                height="20"
                                                                fill="white"
                                                            />
                                                        </clipPath>
                                                    </defs>
                                                </svg>
                                            </span>
                                            {{ item.text }}
                                        </p>
                                    </template>
                                </div>
                            </div>
                        </div>
                    </div>
                </template>
            </div>
        </div>
    </section>
    <!-- ====== Pricing Section End -->
</template>
