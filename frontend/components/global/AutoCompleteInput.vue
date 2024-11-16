<template>
    <Combobox v-model="selected">
        <div class="relative mt-1">
            <div
                class="relative w-full cursor-default overflow-hidden rounded-lg bg-white text-left focus:outline-none focus-visible:ring-2 focus-visible:ring-white/75 focus-visible:ring-offset-2 focus-visible:ring-offset-teal-300 sm:text-sm"
            >
                <ComboboxInput
                    class="w-full input"
                    :displayValue="(item: any) => item"
                    @change="query = $event.target.value"
                />
                <ComboboxButton class="absolute inset-y-0 right-0 flex items-center pr-2">
                    <ChevronsUpDown
                        class="h-5 w-5 text-gray-400"
                        aria-hidden="true"
                    />
                </ComboboxButton>
            </div>
            <TransitionRoot
                leave="transition ease-in duration-100"
                leaveFrom="opacity-100"
                leaveTo="opacity-0"
                @after-leave="query = ''"
            >
                <ComboboxOptions
                    class="absolute mt-1 max-h-60 w-full overflow-auto rounded-md bg-white py-1 text-base shadow-lg ring-1 ring-black/5 focus:outline-none sm:text-sm"
                >
                    <div
                        v-if="filteredItems.length === 0 && query !== ''"
                        class="relative cursor-default select-none px-4 py-2 text-gray-700 z-50 bg-white"
                    >
                        Nothing found.
                    </div>

                    <ComboboxOption
                        v-for="(item, index) in filteredItems"
                        as="template"
                        :key="index"
                        :value="item"
                        v-slot="{ selected, active }"
                    >
                        <li
                            class="relative cursor-default select-none py-2 pl-10 pr-4 z-50 bg-white"
                            :class="{
                                'bg-teal-600 text-white': active,
                                'text-gray-900': !active,
                            }"
                        >
                            <span
                                class="block truncate"
                                :class="{
                                    'font-medium': selected,
                                    'font-normal': !selected,
                                }"
                            >
                                {{ item }}
                            </span>
                            <span
                                v-if="selected"
                                class="absolute inset-y-0 left-0 flex items-center pl-3"
                                :class="{
                                    'text-white': active,
                                    'text-teal-600': !active,
                                }"
                            >
                                <CheckIcon
                                    class="h-5 w-5"
                                    aria-hidden="true"
                                />
                            </span>
                        </li>
                    </ComboboxOption>
                </ComboboxOptions>
            </TransitionRoot>
        </div>
    </Combobox>
</template>

<script lang="ts" setup>
import { CheckIcon, ChevronsUpDown } from 'lucide-vue-next';
import {
    Combobox,
    ComboboxInput,
    ComboboxButton,
    ComboboxOptions,
    ComboboxOption,
    TransitionRoot,
} from '@headlessui/vue';

const props = defineProps<{
    items: string[];
}>();

let selected = ref(props.items[0]);
let query = ref('');

let filteredItems = computed(() =>
    query.value === ''
        ? props.items
        : props.items.filter((item) =>
              item
                  .toLowerCase()
                  .replace(/\s+/g, '')
                  .includes(query.value.toLowerCase().replace(/\s+/g, ''))
          )
);
</script>
