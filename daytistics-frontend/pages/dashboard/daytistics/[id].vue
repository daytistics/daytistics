<template>
  <div class="min-h-screen bg-gray-100 py-8 px-4 sm:px-6 lg:px-8">
    <div class="max-w-3xl mx-auto bg-white shadow-lg rounded-lg overflow-hidden">
      <div class="px-6 py-8 bg-secondary">
        <h1 class="text-3xl font-bold text-white">Daytistic Detail</h1>
        <p class="mt-2 text-lg text-indigo-100">{{ formatDate(daytistic.date) }}</p>
      </div>

      <div class="px-6 py-8">
        <section aria-labelledby="wellbeing-ratings-title" class="mb-12">
          <h2 id="wellbeing-ratings-title" class="text-2xl font-semibold text-gray-900 mb-6">Well-being Ratings</h2>
          <div class="grid grid-cols-1 gap-6 sm:grid-cols-3">
            <div v-for="(rating, category) in daytistic.wellbeingRatings" :key="category"
              class="bg-gray-50 p-4 rounded-lg shadow-sm">
              <h3 class="text-sm font-medium text-gray-500 mb-2">{{ category }}</h3>
              <div class="flex items-center">
                <div class="flex">
                  <Star v-for="star in 5" :key="star" @click="daytistic.wellbeingRatings[category] = star" :class="[
                    'w-5 h-5 hover:cursor-pointer',
                    star <= rating ? 'text-yellow-400 fill-current' : 'text-gray-300'
                  ]" />
                </div>
                <span class="ml-2 text-sm text-gray-700">{{ rating }}/5</span>
              </div>
            </div>
          </div>
        </section>

        <section aria-labelledby="diary-entry-title" class="mb-12">
          <div class="flex items-center mb-6">
            <h2 id="diary-entry-title" class="text-2xl font-semibold text-gray-900 mr-4">Diary Entry</h2>
            <button @click="toggleDiaryEdit"
              class="text-indigo-600 hover:text-indigo-800 flex items-center transition duration-150 ease-in-out"
              :aria-label="isEditingDiary ? 'Cancel editing' : 'Edit diary entry'">
              <component :is="isEditingDiary ? X : Edit2" class="w-5 h-5 mr-1" />
              <span class="text-sm font-medium">{{ isEditingDiary ? 'Cancel' : 'Edit' }}</span>
            </button>
          </div>
          <div class="bg-gray-50 p-6 rounded-lg shadow-sm">
            <div v-if="!isEditingDiary" class="prose max-w-none">
              <p class="text-gray-700">{{ daytistic.diaryEntry }}</p>
              <div class="mt-6">
                <h3 class="text-lg font-medium text-gray-900 mb-3">Moment of Happiness</h3>
                <p class="text-gray-700">{{ daytistic.momentOfHappiness }}</p>
              </div>
            </div>
            <div v-else>
              <label for="diary-entry" class="block text-sm font-medium text-gray-700 mb-2">Diary Entry</label>
              <textarea id="diary-entry" v-model="editedDiaryEntry"
                class="w-full p-3 border rounded-md focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 mb-4"
                rows="4"></textarea>
              <label for="moment-of-happiness" class="block text-sm font-medium text-gray-700 mb-2">Moment of
                Happiness</label>
              <textarea id="moment-of-happiness" v-model="editedMomentOfHappiness"
                class="w-full p-3 border rounded-md focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 mb-4"
                rows="2"></textarea>
              <button @click="saveDiaryChanges"
                class="w-full bg-indigo-600 text-white px-4 py-2 rounded-md hover:bg-indigo-700 transition duration-150 ease-in-out focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2">
                Save Changes
              </button>
            </div>
          </div>
        </section>

        <section aria-labelledby="activities-title">
          <div class="flex items-center mb-6">
            <h2 id="diary-entry-title" class="text-2xl font-semibold text-gray-900 mr-4">Activities</h2>
            <button class="text-indigo-600 hover:text-indigo-800 flex items-center transition duration-150 ease-in-out">
              <Plus class="w-5 h-5 mr-1" />
              <span class="text-sm font-medium">Add New</span>
            </button>
          </div>
          <ul class="bg-gray-50 rounded-lg shadow-sm overflow-hidden">
            <li v-for="(activity, index) in daytistic.activities" :key="activity.id" class="group"
              @click="viewActivityDetails(activity)">
              <div
                class="px-6 py-4 flex items-center justify-between hover:bg-gray-100 transition duration-150 ease-in-out cursor-pointer"
                :class="{ 'border-t border-gray-200': index !== 0 }">
                <div>
                  <p
                    class="text-lg font-medium text-gray-900 group-hover:text-indigo-600 transition duration-150 ease-in-out">
                    {{ activity.name }}</p>
                  <p class="text-sm text-gray-500">{{ formatTimeWindow(activity.startTime, activity.endTime) }}</p>
                </div>
                <div class="flex items-center">
                  <p class="text-sm font-medium text-gray-900 mr-2">{{ formatDuration(activity.duration) }}</p>
                  <ChevronRight
                    class="w-5 h-5 text-gray-400 group-hover:text-indigo-600 transition duration-150 ease-in-out" />
                </div>
              </div>
            </li>
          </ul>
        </section>
      </div>
    </div>

    <!-- Activity Details Modal -->
    <div v-if="selectedActivity"
      class="fixed inset-0 bg-black bg-opacity-50 overflow-y-auto h-full w-full flex items-center justify-center z-50">
      <div class="bg-white p-8 rounded-lg shadow-xl max-w-md w-full m-4">
        <h3 class="text-2xl font-semibold mb-4">{{ selectedActivity.name }}</h3>
        <p class="text-gray-600 mb-6">{{ formatTimeWindow(selectedActivity.startTime, selectedActivity.endTime) }} ({{
          formatDuration(selectedActivity.duration) }})</p>
        <button @click="selectedActivity = null"
          class="w-full bg-indigo-600 text-white px-4 py-2 rounded-md hover:bg-indigo-700 transition duration-150 ease-in-out focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2">Close</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { Star, Edit2, ChevronRight, X, Plus } from 'lucide-vue-next'

const daytistic = ref({
  date: new Date(),
  wellbeingRatings: {
    'Work': 3,
    'Productivity': 4,
    'Sport': 4,
    'Health': 3,
    'Familie & Friends': 5,
    'Happiness': 4,
    'Recreation': 4,
    'Time For Me': 4,
    'Gratitude': 4,
  },
  diaryEntry: "Today was a productive day. I managed to complete all my tasks and even had time for a short walk in the park. The fresh air really helped clear my mind.",
  momentOfHappiness: "Receiving a surprise call from an old friend made my day brighter.",
  activities: [
    { id: 1, name: "Morning Workout", startTime: "07:00", endTime: "08:00", duration: 60 },
    { id: 2, name: "Work", startTime: "09:00", endTime: "17:00", duration: 480 },
    { id: 3, name: "Reading", startTime: "19:00", endTime: "20:00", duration: 60 },
    { id: 4, name: "Meditation", startTime: "21:30", endTime: "22:00", duration: 30 }
  ]
})

const isEditingDiary = ref(false)
const editedDiaryEntry = ref(daytistic.value.diaryEntry)
const editedMomentOfHappiness = ref(daytistic.value.momentOfHappiness)
const selectedActivity = ref(null)

const formatDate = (date) => {
  return new Intl.DateTimeFormat('en-US', {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  }).format(date)
}

const formatTimeWindow = (start, end) => {
  return `${start} - ${end}`
}

const formatDuration = (minutes) => {
  const hours = Math.floor(minutes / 60)
  const mins = minutes % 60
  return hours > 0 ? `${hours}h ${mins}m` : `${mins}m`
}

const toggleDiaryEdit = () => {
  if (isEditingDiary.value) {
    // Cancel editing
    editedDiaryEntry.value = daytistic.value.diaryEntry
    editedMomentOfHappiness.value = daytistic.value.momentOfHappiness
  }
  isEditingDiary.value = !isEditingDiary.value
}

const saveDiaryChanges = () => {
  daytistic.value.diaryEntry = editedDiaryEntry.value
  daytistic.value.momentOfHappiness = editedMomentOfHappiness.value
  isEditingDiary.value = false
}

const viewActivityDetails = (activity) => {
  selectedActivity.value = activity
}
</script>