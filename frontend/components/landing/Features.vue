<template>
    <div class="container mx-auto px-6 py-16">
        <div class="flex flex-col md:flex-row items-center justify-between gap-8">
            <div class="w-full md:w-1/4 space-y-4">
                <Card
                    v-for="(feature, index) in features.slice(0, 3)"
                    :key="index"
                    :clickable="true"
                    :class="{
                        shadow: activeFeature === index,
                    }"
                    @click="activeFeature = index"
                    class="flex flex-col justify-center items-center gap-2"
                >
                    <h3 class="font-bold text-lg">{{ feature.title }}</h3>
                    <component
                        :is="feature.icon"
                        class="w-14 h-auto text-day-primary"
                    />
                </Card>
            </div>

            <LandingFeaturesScreen>
                <NuxtImg
                    :key="activeFeature"
                    src="/images/app-placeholder.jpg"
                    :alt="features[activeFeature].title"
                    class="w-full h-auto rounded"
                />
            </LandingFeaturesScreen>
            <div class="w-full md:w-1/4 space-y-4">
                <Card
                    v-for="(feature, index) in features.slice(3)"
                    :key="index"
                    :clickable="true"
                    :class="{
                        shadow: activeFeature === index,
                    }"
                    @click="activeFeature = index"
                    class="flex flex-col justify-center items-center gap-2"
                >
                    <h3 class="font-bold text-lg">{{ feature.title }}</h3>
                    <component
                        :is="feature.icon"
                        class="w-14 h-auto text-day-primary"
                    />
                </Card>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';

import { Bot, ChartBar, DollarSign, RollerCoaster, Server, Trophy } from 'lucide-vue-next';

const features = [
    {
        title: 'Activity-Tracking',
        icon: RollerCoaster,
    },
    {
        title: 'Wellbeing-Tracking',
        icon: Trophy,
    },
    {
        title: 'Recommendations',
        icon: Bot,
    },
    {
        title: 'Visualizations',
        icon: ChartBar,
    },
    {
        title: 'Fair Pricing',
        icon: DollarSign,
    },
    {
        title: 'Self-Hosting',
        icon: Server,
    },
];

const activeFeature = ref(0);

const featureCutIndex = features.length; // 2;
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
    transition: opacity 0.5s ease;
}

.fade-enter-from,
.fade-leave-to {
    opacity: 0;
}
</style>
