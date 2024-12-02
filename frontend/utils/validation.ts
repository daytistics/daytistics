function isValidPassword(password: string) {
    return (
        password.match(/^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&§*-]).{8,}$/) !== null
    );
}

function isValidEmail(email: string) {
    return email.match(/^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}$/) !== null;
}

function isValidUsername(username: string) {
    return username.match(/^[a-zA-Z0-9_]{5,}$/) !== null;
}

export { isValidPassword, isValidEmail, isValidUsername };
