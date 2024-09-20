export const useUtils = () => {
    function getGreeting() {
        const date = new Date();
        const hours = date.getHours();

        if (hours < 12) {
            return 'Good morning 🥱';
        } else if (hours < 18) {
            return 'Good afternoon 🌻';
        } else if (hours < 20) {
            return 'Good evening ⚽';
        } else {
            return 'Good night 🌛';
        }
    }

    return {
        getGreeting,
    };
};
