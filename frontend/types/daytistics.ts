interface Daytistic {
    id: number;
    date: string;
    average_wellbeing: number;
    total_activities: number;
    total_duration: number;
    user: {
        username: string;
        email: string;
        is_active: boolean;
        is_staff: boolean;
        is_superuser: boolean;
        groups: string[];
        user_permissions: string[];
        date_joined: string;
        last_login: string;
    };
    wellbeing: {
        id: number;
        name: string;
        rating: number;
    }[];
    activities: {
        id: number;
        name: string;
        duration: number;
        start_time: number;
        end_time: number;
    }[];
    diary: {
        entry: string;
        moment_of_happiness: string;
    };
}

export type { Daytistic };
