import { joinURL } from 'ufo';

export default defineEventHandler(async (event) => {
    const proxyUrl = useRuntimeConfig().public.apiAddress;
    const target = joinURL(proxyUrl, event.path);

    const headers = {
        ...Object.fromEntries(Object.entries(event.headers).filter(([key]) => key !== 'host')),
    };

    console.log(event.headers.get('Cookie'));

    const response = await proxyRequest(event, target, {
        headers: headers,
    });

    return response;
});
