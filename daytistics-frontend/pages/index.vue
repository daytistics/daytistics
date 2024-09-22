<template>
  <div class="min-h-screen bg-gray-50">

    <!-- Hero Section -->
    <section class="pt-32 pb-20 px-4">
      <div class="container mx-auto text-center">
        <h1 class="text-5xl md:text-6xl font-bold text-gray-900 mb-6">Welcome to Daytistics</h1>
        <p class="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">Discover the power of our innovative platform designed
          to simplify your life and increase your productivity.</p>
        <a href="#"
          class="bg-secondary text-white px-8 py-3 rounded-full text-lg font-semibold hover:bg-secondary-dark transition duration-300 ease-in-out">Get
          Started</a>
      </div>
    </section>

    <!-- Features Section -->
    <section id="features" class="py-20 bg-white">
      <div class="container mx-auto px-4">
        <h2 class="text-3xl font-bold text-center text-gray-900 mb-12">Key Features</h2>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div v-for="feature in features" :key="feature.title"
            class="bg-gray-50 rounded-lg p-6 shadow-md hover:shadow-lg transition duration-300 ease-in-out">
            <component :is="feature.icon" class="h-12 w-12 text-primary mb-4" />
            <h3 class="text-xl font-semibold text-gray-900 mb-2">{{ feature.title }}</h3>
            <p class="text-gray-600">{{ feature.description }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Pricing Section -->
    <section id="pricing" class="py-20 bg-gray-50">
      <div class="container mx-auto px-4">
        <h2 class="text-3xl font-bold text-center text-gray-900 mb-12">Pricing Plans</h2>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div v-for="[index, plan] in pricingPlans.entries()" :key="plan.title"
            class="bg-white rounded-lg shadow-md overflow-hidden">
            <div class="p-6">
              <h3 class="text-2xl font-semibold text-gray-900 mb-4">{{ plan.title }}</h3>
              <p class="text-4xl font-bold text-gray-900 mb-6">${{ plan.price }}<span
                  class="text-lg font-normal text-gray-600">/mo</span></p>
              <ul class="mb-6">
                <li v-for="feature in plan.features" :key="feature" class="flex items-center mb-2">
                  <CheckIcon v-if="feature.available" class="h-5 w-5 text-green-500 mr-2" />
                  <X v-else class="h-5 w-5 text-red-500 mr-2" />
                  <span class="text-gray-600">{{ feature.name }}</span>
                </li>
              </ul>
            </div>
            <div class="bg-gray-50 p-6">
              <button type="button" @click="openPlanModal(index)" :disabled="!plan.available"
                :class="{ 'cursor-not-allowed bg-secondary/60 hover:bg-secondary/60': !plan.available }"
                class="block w-full text-center bg-secondary text-white px-4 py-2 rounded-full font-semibold hover:bg-secondary-dark transition duration-300 ease-in-out">
                Choose
                Plan</button>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Self-Hosting Section -->
    <section id="self-hosting" class="py-20 bg-white">
      <div class="container mx-auto px-4">
        <div class="flex flex-col md:flex-row items-center">
          <div class="md:w-1/2 mb-8 md:mb-0 p-4">
            <h2 class="text-3xl font-bold text-gray-900 mb-4">Self-Hosting Options</h2>
            <p class="text-gray-600 mb-6">Take control of your data and infrastructure with our flexible self-hosting
              solutions. Deploy ModernApp on your own servers or preferred cloud provider.</p>
            <ul class="mb-6">
              <li v-for="benefit in selfHostingBenefits" :key="benefit" class="flex items-center mb-2">
                <CheckIcon class="h-5 w-5 text-green-500 mr-2" />
                <span class="text-gray-600">{{ benefit }}</span>
              </li>
            </ul>
            <a href="#"
              class="inline-block bg-primary text-white px-6 py-2 rounded-full font-semibold hover:bg-primary-dark transition duration-300 ease-in-out">Learn
              More</a>
          </div>
          <div class="md:w-1/2">
            <img src="https://via.assets.so/game.png?id=1&q=95&w=600&h=400&fit=fill" alt="Self-hosting illustration"
              class="rounded-lg shadow-md" />
          </div>
        </div>
      </div>
    </section>

    <!-- About Section -->
    <section id="about" class="py-20 bg-gray-50">
      <div class="container mx-auto px-4">
        <div class="flex flex-col md:flex-row items-center">
          <div class="md:w-1/2 mb-8 md:mb-0">
            <NuxtImg src="/images/about-us.jpg" width="650" alt="About us image" class="rounded-lg shadow-md" />
          </div>
          <div class="md:w-1/2 md:pl-12">
            <h2 class="text-3xl font-bold text-gray-900 mb-4">About</h2>
            <p class="text-gray-600 mb-6">At ModernApp, we're passionate about creating innovative solutions that
              empower businesses and individuals to achieve their goals. Our team of dedicated professionals works
              tirelessly to deliver cutting-edge technology and exceptional user experiences.</p>
            <p class="text-gray-600 mb-6">Founded in 2023, we've quickly grown to become a leader in our industry,
              serving clients across the globe. Our commitment to excellence and customer satisfaction drives everything
              we do.</p>
            <a href="#"
              class="inline-block bg-secondary text-white px-6 py-2 rounded-full font-semibold hover:bg-secondary-dark transition duration-300 ease-in-out">Meet
              the Team</a>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue';
import { MenuIcon, XIcon, CheckIcon, Brain, ShieldIcon, UsersIcon, ActivitySquareIcon, Book, ChartColumnIcon, Server, X } from 'lucide-vue-next';

const mobileMenuOpen = ref(false);
const newsletterEmail = ref('');

const router = useRouter();

function openPlanModal(index: number) {
  alert(`Plan ${index + 1} selected`);
}

const features = [
  { icon: ActivitySquareIcon, title: 'Activities & Well-being Tracker', description: 'Experience blazing-fast performance with our optimized platform.' },
  { icon: Book, title: 'Digital Diary', description: 'Your data is protected with state-of-the-art security measures.' },
  { icon: ChartColumnIcon, title: 'Stunning Visualization', description: 'Work seamlessly with your team in real-time.' },
  { icon: Brain, title: 'Predictor & Suggestor', description: 'Work seamlessly with your team in real-time.' },
  { icon: UsersIcon, title: 'Family Integration', description: 'Work seamlessly with your team in real-time.' },
  { icon: Server, title: 'Self-Hosting', description: 'Work seamlessly with your team in real-time.' },
];

const pricingPlans = [
  {
    title: 'Free',
    price: 0,
    features: [
      { name: '5 Users', available: true },
      { name: 'Self-Hosting', available: true },
      { name: 'Activity-Wellbeing Visualizations', available: true },
      { name: 'No advertising', available: true },
      { name: 'Permanent data storage', available: false },
      { name: 'No AI training limits', available: false },
      { name: 'Data export', available: false },
      { name: 'Family features', available: false },
    ],
    available: true,
  },
  {
    title: 'Premium',
    price: 4.99,
    features: [
      { name: '1 User', available: true },
      { name: 'Self-Hosting', available: true },
      { name: 'Activity-Wellbeing Visualizations', available: true },
      { name: 'No advertising', available: true },
      { name: 'Permanent data storage', available: true },
      { name: 'No AI training limits', available: true },
      { name: 'Data export', available: true },
      { name: 'Family features', available: false },
    ],
    available: false,
  },
  {
    title: 'Family',
    price: 9.99,
    features: [
      { name: '5 Users', available: true },
      { name: 'Self-Hosting', available: true },
      { name: 'Activity-Wellbeing Visualizations', available: true },
      { name: 'No advertising', available: true },
      { name: 'Permanent data storage', available: true },
      { name: 'No AI training limits', available: true },
      { name: 'Data export', available: true },
      { name: 'Family features', available: true },
    ],
    available: false,
  },
];

const selfHostingBenefits = [
  'Full control over your data',
  'Customizable infrastructure',
  'Enhanced security and compliance',
  'Flexible deployment options',
];
</script>
