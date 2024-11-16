function isValidPassword(password: string) {
    return password.match(
        /^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&§*-]).{8,}$/
    );
}

function isValidEmail(email: string) {
    return email.match(/^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$/);
}

function isValidUsername(username: string) {
    return username.match(/^[a-zA-Z0-9_]{5,}$/);
}

export { isValidPassword, isValidEmail, isValidUsername };
