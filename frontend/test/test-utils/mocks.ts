import type { Daytistic } from '~/types/daytistics';

const generateDaytistics = (n: number): Daytistic[] => {
    const startDate = new Date(0);

    return Array.from({ length: n }, (_, i) => ({
        id: i + 1,
        date: new Date(startDate.setDate(startDate.getDate() + 1)).toISOString(),
        average_wellbeing: Math.random() * 5,
        total_activities: 3,
        total_duration: 180,
        user: {
            username: `user${i + 1}`,
            email: `user${i + 1}@example.com`,
            is_active: true,
            is_staff: false,
            is_superuser: false,
            groups: ['user'],
            user_permissions: [],
            date_joined: new Date().toISOString(),
            last_login: new Date().toISOString(),
        },
        wellbeing: [{ id: 0, name: 'Happiness', rating: 4 }],
        activities: [
            {
                id: 1,
                name: 'Reading',
                duration: 60,
                start_time: 9,
                end_time: 10,
            },
            {
                id: 2,
                name: 'Running',
                duration: 30,
                start_time: 10,
                end_time: 10.5,
            },
            {
                id: 3,
                name: 'Coding',
                duration: 90,
                start_time: 11,
                end_time: 12.5,
            },
        ],
        diary: {
            entry: `This is a diary entry for Daytistic ${i + 1}.`,
            moment_of_happiness: `A happy moment on Daytistic ${i + 1}.`,
        },
    }));
};

export { generateDaytistics };
