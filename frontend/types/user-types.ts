interface User {
    username: string;
    email: string;
    isActive: boolean;
    isStaff: boolean;
    isSuperuser: boolean;
    groups: string[];
    permissions: string[];
    dateJoined: Date | null;
    lastLogin: Date | null;
}

enum AuthenticationStatus {
    AUTHENTICATED,
    UNAUTHENTICATED,
    PENDING,
}

export { type User, AuthenticationStatus };
