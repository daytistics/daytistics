import type { Daytistic } from '~/types/daytistics';

export default function useEndpoints() {
    const { $api } = useNuxtApp();

    /**
     * Creates a daytistic and gives the user a toast (on success and error)
     * @param date The date to create the daytistic for. Only the date part is used, the time and the timezone are ignored
     * @returns The ID of the created daytistic or undefined if the creation failed
     */
    const createDaytistic = async (date: Date): Promise<number | undefined> => {
        let id: number | undefined = undefined;

        await $api('/api/daytistics/create', {
            method: 'POST',
            body: {
                date: date.toISOString().split('T')[0],
            },

            onResponse: ({ response }) => {
                if (response.status === 201) {
                    id = response._data.id;
                }
            },
        });

        return id;
    };

    const listDaytistics = async (
        page: number
    ): Promise<{
        count: number;
        items: Daytistic[];
    }> => {
        return await $api(`/api/daytistics/list?page=${page}`, {
            method: 'GET',
        });
    };

    return { createDaytistic, listDaytistics, payments };
}

const payments = {
    async getTotalTokens(): Promise<number> {
        return 0;
    },
};
