export const useInputValidation = () => {
    const isValidPassword = (password: string) => {
        // Mindestens 8 Zeichen, mindestens ein Großbuchstabe, ein Kleinbuchstabe, eine Zahl und ein Sonderzeichen
        return password.match(
            /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/
        );
    };

    const isValidEmail = (email: string) => {
        return email.match(/^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$/);
    };

    const isValidUsername = (username: string) => {
        return username.match(/^[a-zA-Z0-9_]{5,}$/);
    };

    return {
        isValidPassword,
        isValidEmail,
        isValidUsername,
    };
};
