
from django_components import Component, register, types

@register("datepicker")
class DatePicker(Component):
    def get_context_data(self):
        return {}

    template: types.django_html = """
        <div x-data="datePicker()" class="relative inline-block text-left">
            <input type="text" x-model="formattedDate" @click="toggle" readonly class="py-2 px-4 bg-white border rounded-full shadow-md cursor-pointer focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500">
            <div x-show="isOpen" @click.away="isOpen = false" class="absolute mt-2 w-64 bg-white border border-gray-200 rounded-lg shadow-lg z-50">
                <div class="flex items-center justify-between px-4 py-2">
                    <button @click="previousMonth" class="px-2 py-1 text-gray-600 hover:text-gray-900">&lt;</button>
                    <span x-text="monthYear"></span>
                    <button @click="nextMonth" class="px-2 py-1 text-gray-600 hover:text-gray-900">&gt;</button>
                </div>
                <div class="grid grid-cols-7 gap-2 p-2">
                    <template x-for="(day, index) in days" :key="index">
                        <div x-text="day" class="text-center text-gray-600"></div>
                    </template>
                </div>
                <div class="grid grid-cols-7 gap-2 p-2">
                    <template x-for="blankDay in blankDays">
                        <div class="text-center text-transparent">.</div>
                    </template>
                    <template x-for="(date, index) in dates" :key="index">
                        <div @click="selectDate(date)" x-text="date" :class="{'bg-blue-500 text-white': isSelectedDate(date), 'text-gray-700': !isSelectedDate(date), 'cursor-pointer': true}" class="text-center py-1 rounded-full hover:bg-blue-300"></div>
                    </template>
                </div>
            </div>
        </div>
    """

    css = """"""
    js = """
    function datePicker() {
        return {
            isOpen: false,
            date: new Date(),
            days: ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'],
            blankDays: [],
            dates: [],
            selectedDate: null,
            formattedDate: '',
            monthYear: '',

            init() {
                this.updateCalendar();
            },

            toggle() {
                this.isOpen = !this.isOpen;
            },

            selectDate(date) {
                this.selectedDate = new Date(this.date.getFullYear(), this.date.getMonth(), date);
                this.formattedDate = this.selectedDate.toDateString();
                this.isOpen = false;
            },

            previousMonth() {
                this.date.setMonth(this.date.getMonth() - 1);
                this.updateCalendar();
            },

            nextMonth() {
                this.date.setMonth(this.date.getMonth() + 1);
                this.updateCalendar();
            },

            updateCalendar() {
                const firstDayOfMonth = new Date(this.date.getFullYear(), this.date.getMonth(), 1).getDay();
                const lastDateOfMonth = new Date(this.date.getFullYear(), this.date.getMonth() + 1, 0).getDate();

                this.blankDays = Array(firstDayOfMonth).fill(null);
                this.dates = Array.from({ length: lastDateOfMonth }, (_, i) => i + 1);
                this.monthYear = this.date.toLocaleDateString('default', { month: 'long', year: 'numeric' });
            },

            isSelectedDate(date) {
                if (!this.selectedDate) return false;
                return this.selectedDate.getDate() === date && this.selectedDate.getMonth() === this.date.getMonth() && this.selectedDate.getFullYear() === this.date.getFullYear();
            },
        }
    }
    """
