import { joinURL } from 'ufo';

export default defineEventHandler(async (event) => {
    const proxyUrl = useRuntimeConfig().public.apiAddress;
    const target = joinURL(proxyUrl, event.path);

    const response = await proxyRequest(event, target, {});

    return response;
});
