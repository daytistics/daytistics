<template>
    <div class="w-full max-w-4xl bg-white rounded-lg shadow-md p-6 mb-8">
        <h2 class="text-xl font-semibold mb-4">Suggestions</h2>
        <div class="grid grid-rows-3 border-t border-gray-200 pt-4">
            <div class="row-span-2 flex flex-col gap-1 mb-4">
                <p>
                    Lorem ipsum dolor sit amet consectetur adipisicing elit. Ipsam, repellat! Qui nihil commodi saepe
                    quo
                    magnam totam culpa! Ratione mollitia nobis ad quam a voluptatum corporis eius numquam, ipsa iusto!
                    Lorem
                    ipsum dolor sit, amet consectetur adipisicing elit.
                    <br>
                    Magnam, tenetur, totam, eveniet deleniti non a
                    blanditiis quam laudantium corrupti enim rerum saepe quaerat omnis fuga aspernatur necessitatibus
                    eius
                    ea rem.
                </p>
                <span class="underline text-secondary hover:cursor-pointer">See More</span>
            </div>
            <div class="row-span-1 flex flex-col justify-end items-end gap-4">
                <div
                    class="bg-green-100 rounded-lg p-3 max-w-xs hover:cursor-pointer hover:-translate-y-1 transition-transform">
                    <p>
                        <Crown class="w-6 h-6 mr-2 inline text-yellow-300" />
                        <span>Receive a professional analysis</span>
                    </p>
                </div>
                <div
                    class="bg-green-100 rounded-lg p-3 max-w-xs hover:cursor-pointer hover:-translate-y-1 transition-transform">
                    <p>
                        <Settings class="w-6 h-6 mr-2 inline" />
                        <span>Regenerate Analysis</span>
                    </p>
                </div>
            </div>
        </div>
    </div>
</template>

<script lang="ts" setup>
import { Crown, Settings } from 'lucide-vue-next';


</script>