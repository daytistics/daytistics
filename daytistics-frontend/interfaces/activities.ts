export interface ActivityType {
    id: number;
    name: string;
    category: string;
    available: boolean;
    active: boolean;
}

export interface ActivityEntry {
    id: number;
    name: string;
    duration: number;
    start_time: number;
    end_time: number;
}
