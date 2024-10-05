export const useUtils = () => {
    const getGreeting = () => {
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
    };
    const convertDateStringToMMDDYYYY = (dateString: string) => {
        const date = new Date(dateString.toString());
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const day = String(date.getDate()).padStart(2, '0');
        const year = date.getFullYear();

        return `${month}/${day}/${year}`;
    };

    return {
        getGreeting,
        convertDateStringToMMDDYYYY,
    };
};
