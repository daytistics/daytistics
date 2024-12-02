<template>
    <header class="relative isolate z-50 bg-transparent">
        <nav
            class="mx-auto flex max-w-7xl items-center justify-between p-6 lg:px-8"
            aria-label="Global"
        >
            <div class="flex lg:flex-1">
                <a
                    href="#"
                    class="-m-1.5 p-1.5"
                >
                    <span class="sr-only">Your Contribute</span>
                    <NuxtImg
                        class="h-10 w-auto"
                        src="/images/logo.png"
                        alt=""
                    />
                </a>
            </div>
            <div class="flex lg:hidden">
                <button
                    type="button"
                    class="-m-2.5 inline-flex items-center justify-center rounded-md p-2.5 text-gray-700"
                    @click="mobileMenuOpen = true"
                >
                    <span class="sr-only">Open main menu</span>
                    <MenuIcon
                        class="size-6"
                        aria-hidden="true"
                    />
                </button>
            </div>
            <PopoverGroup class="hidden lg:flex lg:gap-x-12">
                <Popover>
                    <PopoverButton
                        class="flex items-center gap-x-1 text-sm/6 font-semibold text-gray-900"
                    >
                        Daytistics
                        <ChevronDownIcon
                            class="size-5 flex-none text-gray-400"
                            aria-hidden="true"
                        />
                    </PopoverButton>

                    <transition
                        enter-active-class="transition ease-out duration-200"
                        enter-from-class="opacity-0 -translate-y-1"
                        enter-to-class="opacity-100 translate-y-0"
                        leave-active-class="transition ease-in duration-150"
                        leave-from-class="opacity-100 translate-y-0"
                        leave-to-class="opacity-0 -translate-y-1"
                    >
                        <PopoverPanel
                            class="absolute inset-x-0 top-0 -z-10 bg-white pt-14 shadow-lg ring-1 ring-gray-900/5"
                        >
                            <div
                                class="mx-auto grid max-w-7xl grid-cols-4 gap-x-4 px-6 py-10 lg:px-8 xl:gap-x-8"
                            >
                                <div
                                    v-for="item in Daytisticss"
                                    :key="item.name"
                                    class="group relative rounded-lg p-6 text-sm/6 hover:bg-gray-50"
                                >
                                    <div
                                        class="flex size-11 items-center justify-center rounded-lg bg-gray-50 group-hover:bg-white"
                                    >
                                        <component
                                            :is="item.icon"
                                            class="size-6 text-gray-600 group-hover:text-primary"
                                            aria-hidden="true"
                                        />
                                    </div>
                                    <a
                                        :href="item.href"
                                        class="mt-6 block font-semibold text-gray-900"
                                    >
                                        {{ item.name }}
                                        <span class="absolute inset-0" />
                                    </a>
                                    <p class="mt-1 text-gray-600">
                                        {{ item.description }}
                                    </p>
                                </div>
                            </div>
                            <div class="bg-gray-50">
                                <div class="mx-auto max-w-7xl px-6 lg:px-8">
                                    <div
                                        class="grid grid-cols-3 divide-x divide-gray-900/5 border-x border-gray-900/5"
                                    >
                                        <a
                                            v-for="item in callsToAction"
                                            :key="item.name"
                                            :href="item.href"
                                            class="flex items-center justify-center gap-x-2.5 p-3 text-sm/6 font-semibold text-gray-900 hover:bg-gray-100"
                                        >
                                            <component
                                                :is="item.icon"
                                                class="size-5 flex-none text-gray-400"
                                                aria-hidden="true"
                                            />
                                            {{ item.name }}
                                        </a>
                                    </div>
                                </div>
                            </div>
                        </PopoverPanel>
                    </transition>
                </Popover>

                <NuxtLink
                    to="#features"
                    class="text-sm/6 font-semibold text-gray-900"
                    >Features</NuxtLink
                >
                <a
                    href="#"
                    class="text-sm/6 font-semibold text-gray-900"
                    >Pricing</a
                >
                <a
                    href="#"
                    class="text-sm/6 font-semibold text-gray-900"
                    >Contribute</a
                >
            </PopoverGroup>
            <div class="hidden lg:flex lg:flex-1 lg:justify-end">
                <a
                    href="#"
                    class="text-sm/6 font-semibold text-gray-900"
                    >Log in <span aria-hidden="true">&rarr;</span></a
                >
            </div>
        </nav>
        <Dialog
            class="lg:hidden"
            @close="mobileMenuOpen = false"
            :open="mobileMenuOpen"
        >
            <div class="fixed inset-0 z-10" />
            <DialogPanel
                class="fixed inset-y-0 right-0 z-10 w-full overflow-y-auto bg-white px-6 py-6 sm:max-w-sm sm:ring-1 sm:ring-gray-900/10"
            >
                <div class="flex items-center justify-between">
                    <a
                        href="#"
                        class="-m-1.5 p-1.5"
                    >
                        <span class="sr-only">Your Contribute</span>
                        <img
                            class="h-8 w-auto"
                            src="https://tailwindui.com/plus/img/logos/mark.svg?color=indigo&shade=600"
                            alt=""
                        />
                    </a>
                    <button
                        type="button"
                        class="-m-2.5 rounded-md p-2.5 text-gray-700"
                        @click="mobileMenuOpen = false"
                    >
                        <span class="sr-only">Close menu</span>
                        <X
                            class="size-6"
                            aria-hidden="true"
                        />
                    </button>
                </div>
                <div class="mt-6 flow-root">
                    <div class="-my-6 divide-y divide-gray-500/10">
                        <div class="space-y-2 py-6">
                            <Disclosure
                                as="div"
                                class="-mx-3"
                                v-slot="{ open }"
                            >
                                <DisclosureButton
                                    class="flex w-full items-center justify-between rounded-lg py-2 pl-3 pr-3.5 text-base/7 font-semibold text-gray-900 hover:bg-gray-50"
                                >
                                    Daytistics
                                    <ChevronDownIcon
                                        :class="[open ? 'rotate-180' : '', 'size-5 flex-none']"
                                        aria-hidden="true"
                                    />
                                </DisclosureButton>
                                <DisclosurePanel class="mt-2 space-y-2">
                                    <DisclosureButton
                                        v-for="item in [...Daytisticss, ...callsToAction]"
                                        :key="item.name"
                                        as="a"
                                        :href="item.href"
                                        class="block rounded-lg py-2 pl-6 pr-3 text-sm/7 font-semibold text-gray-900 hover:bg-gray-50"
                                        >{{ item.name }}</DisclosureButton
                                    >
                                </DisclosurePanel>
                            </Disclosure>
                            <a
                                href="#"
                                class="-mx-3 block rounded-lg px-3 py-2 text-base/7 font-semibold text-gray-900 hover:bg-gray-50"
                                >Features</a
                            >
                            <NuxtLink
                                to="#pricing"
                                class="-mx-3 block rounded-lg px-3 py-2 text-base/7 font-semibold text-gray-900 hover:bg-gray-50"
                                >Pricing</NuxtLink
                            >
                            <a
                                href="#"
                                class="-mx-3 block rounded-lg px-3 py-2 text-base/7 font-semibold text-gray-900 hover:bg-gray-50"
                                >Contribute</a
                            >
                        </div>
                        <div class="py-6">
                            <a
                                href="#"
                                class="-mx-3 block rounded-lg px-3 py-2.5 text-base/7 font-semibold text-gray-900 hover:bg-gray-50"
                                >Log in</a
                            >
                        </div>
                    </div>
                </div>
            </DialogPanel>
        </Dialog>
    </header>
</template>

<script setup>
import { ref } from 'vue';
import {
    Dialog,
    DialogPanel,
    Disclosure,
    DisclosureButton,
    DisclosurePanel,
    Popover,
    PopoverButton,
    PopoverGroup,
    PopoverPanel,
} from '@headlessui/vue';
import {
    X,
    ChartPieIcon,
    TextCursorIcon,
    Fingerprint,
    SquareIcon,
    CircleIcon,
    PhoneIcon,
    RectangleVerticalIcon,
    ChevronDownIcon,
    MenuIcon,
    Book,
    HelpCircle,
    Speech,
    Star,
} from 'lucide-vue-next';
import DiscordIcon from '../icons/DiscordIcon.vue';

const Daytisticss = [
    {
        name: 'Dashboard',
        description: 'Get to know your well-being better and improve it',
        href: '#',
        icon: ChartPieIcon,
    },
    {
        name: 'Documentation',
        description: 'Learn how to use Daytistics and get the most out of it',
        href: '#',
        icon: Book,
    },
    {
        name: 'Testimonials',
        description: 'See what our users say about Daytistics',
        href: '#',
        icon: Star,
    },
    {
        name: 'Discord',
        description: 'Join our Discord community and get help from others',
        href: '#',
        icon: DiscordIcon,
    },
];
const callsToAction = [
    { name: 'Watch demo', href: '#', icon: CircleIcon },
    { name: 'Contact us', href: '#', icon: PhoneIcon },
    { name: 'Give us feedback', href: '#', icon: RectangleVerticalIcon },
];

const mobileMenuOpen = ref(false);
</script>
