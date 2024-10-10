<template>
  <div class="min-h-screen bg-gray-50">

    <!-- Hero Section -->
    <section class="pt-32 pb-20 px-4" data-aos="fade-up">
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
    <section id="features" data-aos="fade-up" class="py-20 bg-white">
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
    <section id="pricing" data-aos="fade-up" class="py-20 bg-gray-50">
      <div class="container mx-auto px-4">
        <div class="flex flex-col md:flex-row items-center">
          <div class="md:w-1/2 mb-8 md:mb-0">
            <NuxtLink to="https://polar.sh/daytistics/donate">
              <div
                class="bg-gray-50 rounded-lg p-6 shadow-md hover:shadow-xl transition duration-300 ease-in-out flex flex-row items-center gap-4">
                <Heart class="h-64 w-64 text-red-500" />
                <div class="text-gray-900">
                  <h3 class="text-2xl font-semibold mb-2">Donate to Us</h3>
                  <p class="text-gray-900">
                  <div class="flex flex-col gap-3">
                    <span class="text-gray-900">Thanks to every donation, we can continue to improve Daytistics and
                      provide better services to our users. Our current goal is to...
                    </span>

                    <h4 class="text-xl font-semibold text-gray-900">Cover the Expenses</h4>
                    <div class="w-full text-gray-900 rounded-full dark:bg-gray-700">
                      <div
                        class="bg-red-600 text-xs font-medium text-blue-100 text-center p-0.5 leading-none rounded-full"
                        style="width: 45%"> 45%</div>
                    </div>
                  </div>
                  </p>
                </div>
              </div>
            </NuxtLink>
          </div>
          <div class="md:w-1/2 md:pl-12">
            <h2 class="text-3xl font-bold text-gray-900 mb-4">Pricing</h2>
            <p class="text-gray-600 mb-6">At Daytistics, we're dedicated to helping individuals gain better insights
              into their lives through self-reflection. By tracking daily activities and well-being, users can identify
              patterns that lead to more informed decisions and improved well-being.</p>
            <p class="text-gray-600 mb-6">Founded in 2024, we're still at the beginning of our journey. However, our
              commitment to transparency, privacy, and open-source development ensures that every user has full control
              over their data while we grow with the community.</p>

          </div>
        </div>
      </div>
    </section>

    <!-- Self-Hosting Section -->
    <section id="self-hosting" data-aos="fade-up" class="py-20 bg-white">
      <div class="container mx-auto px-4">
        <div class="flex flex-col md:flex-row items-center">
          <div class="md:w-1/2 mb-8 md:mb-0 p-4">
            <h2 class="text-3xl font-bold text-gray-900 mb-4">Self-Hosting Options</h2>
            <p class="text-gray-600 mb-6">Take control of your data and infrastructure with our flexible self-hosting
              solutions. Deploy Daytistics on your own servers or preferred cloud provider.</p>
            <ul class="mb-6">
              <li v-for="benefit in selfHostingBenefits" :key="benefit" class="flex items-center mb-2">
                <CheckIcon class="h-5 w-5 text-green-500 mr-2" />
                <span class="text-gray-600">{{ benefit }}</span>
              </li>
            </ul>
            <a href="#"
              class="inline-block bg-primary text-white px-6 py-2 rounded-full font-semibold hover:bg-primary-dark transition duration-300 ease-in-out">Start
              Now</a>
          </div>
          <div class="md:w-1/2">
            <NuxtImg src="/images/self_hosting.jpeg" alt="Self-hosting illustration" class="rounded-lg shadow-md" />
          </div>
        </div>
      </div>
    </section>

    <!-- About Section -->
    <section id="about" data-aos="fade-up" class="py-20 bg-gray-50">
      <div class="container mx-auto px-4">
        <div class="flex flex-col md:flex-row items-center">
          <div class="md:w-1/2 mb-8 md:mb-0">
            <ol class="relative border-s border-gray-200 dark:border-gray-700">
              <li class="mb-10 ms-4">
                <div
                  class="absolute w-3 h-3 bg-gray-200 rounded-full mt-1.5 -start-1.5 border border-white dark:border-gray-900 dark:bg-gray-700">
                </div>
                <time class="mb-1 text-sm font-normal leading-none text-gray-400 dark:text-gray-500">August
                  2024</time>
                <h3 class="text-lg font-semibold text-gray-900 dark:text-white">Daytistics Was Founded</h3>
                <p class="mb-4 text-base font-normal text-gray-500 dark:text-gray-400">On August 4th, 2024, Leo Gall
                  founded Daytistics after creating a prototype CLI tool for personal use, realizing it could benefit
                  others as well.</p>
              </li>
              <li class="ms-4">
                <div
                  class="absolute w-3 h-3 bg-gray-200 rounded-full mt-1.5 -start-1.5 border border-white dark:border-gray-900 dark:bg-gray-700">
                </div>
                <time class="mb-1 text-sm font-normal leading-none text-gray-400 dark:text-gray-500">Future</time>
                <h3 class="text-lg font-semibold text-gray-900 dark:text-white">What Will The Future Bring?</h3>
                <p class="text-base font-normal text-gray-500 dark:text-gray-400">We don't know what the future holds.
                  All we do know is that <strong>you</strong> can help shape how Daytistics evolves.</p>
              </li>
            </ol>
          </div>
          <div class="md:w-1/2 md:pl-12">
            <h2 class="text-3xl font-bold text-gray-900 mb-4">About</h2>
            <p class="text-gray-600 mb-6">At Daytistics, we're dedicated to helping individuals gain better insights
              into their lives through self-reflection. By tracking daily activities and well-being, users can identify
              patterns that lead to more informed decisions and improved well-being.</p>
            <p class="text-gray-600 mb-6">Founded in 2024, we're still at the beginning of our journey. However, our
              commitment to transparency, privacy, and open-source development ensures that every user has full control
              over their data while we grow with the community.</p>
            <NuxtLink to="https://docs.daytistics.com/contributers/overview/"
              class="inline-block bg-secondary text-white px-6 py-2 rounded-full font-semibold hover:bg-secondary-dark transition duration-300 ease-in-out">
              Contribute
              to Us</NuxtLink>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue';
import { MenuIcon, Heart, CheckIcon, Brain, ShieldIcon, UsersIcon, ActivitySquareIcon, Book, ChartColumnIcon, Server, X } from 'lucide-vue-next';

const mobileMenuOpen = ref(false);
const newsletterEmail = ref('');

const router = useRouter();

function openPlanModal(index: number) {
  alert(`Plan ${index + 1} selected`);
}

const features = [
  {
    icon: ActivitySquareIcon,
    title: 'Activities & Well-being Tracker',
    description: 'Track your daily activities and well-being metrics, powered by a highly optimized platform for fast performance.'
  },
  {
    icon: Book,
    title: 'Digital Diary',
    description: 'Keep a private, secure digital diary with advanced data protection ensuring your privacy.'
  },
  {
    icon: ChartColumnIcon,
    title: 'Stunning Visualization',
    description: 'Get beautiful, real-time visualizations of your activity and well-being data, perfect for analysis.'
  },
  {
    icon: Brain,
    title: 'Predictor & Suggestor',
    description: 'Use AI-powered tools to predict patterns and suggest improvements based on your tracked data.'
  },
  {
    icon: UsersIcon,
    title: 'Family Integration',
    description: 'Seamlessly connect with family members and share your activity or well-being progress.'
  },
  {
    icon: Server,
    title: 'Self-Hosting',
    description: 'Self-host Daytistics for full control over your data, ensuring privacy and customization.'
  },
];

const pricingPlans = [
  {
    title: 'Free',
    price: 0,
    features: [
      { name: '1 User', available: true },
      { name: 'Self-Hosting', available: true },
      { name: 'Activity-Wellbeing Visualizations', available: true },
      { name: 'No advertising', available: false },
      { name: 'Pay-As-You-Go for AIs (max 1 AI-training/mo)', available: false },
      { name: 'Permanent data storage', available: false },
      { name: 'Data export', available: false },
      { name: 'Family features', available: false },
    ],
    available: false,
  },
  {
    title: 'Premium',
    price: 2.99,
    features: [
      { name: '1 User', available: true },
      { name: 'Self-Hosting', available: true },
      { name: 'Activity-Wellbeing Visualizations', available: true },
      { name: 'No advertising', available: true },
      { name: 'Pay-As-You-Go for AIs', available: true },
      { name: 'Permanent data storage', available: true },
      { name: 'Data export', available: true },
      { name: 'Family features', available: false },
    ],
    available: false,
  },
  {
    title: 'Family',
    price: 9.99,
    features: [
      { name: '1 User', available: true },
      { name: 'Self-Hosting', available: true },
      { name: 'Activity-Wellbeing Visualizations', available: true },
      { name: 'No advertising', available: true },
      { name: 'Pay-As-You-Go for AIs', available: true },
      { name: 'Permanent data storage', available: true },
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
  'Easy deployment using Docker or Kubernetes',
];

</script>
