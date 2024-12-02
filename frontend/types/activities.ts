interface ActivityType {
    id: number;
    name: string;
    category: string;
    available: boolean;
    active: boolean;
}

interface ActivityEntry {
    id: number;
    name: string;
    duration: number;
    start_time: number;
    end_time: number;
}

export type { ActivityEntry, ActivityType };
