const pad = (n) => `${Math.floor(Math.abs(n))}`.padStart(2, '0');
// Get timezone offset in ISO format (+hh:mm or -hh:mm)
const getTimezoneOffset = (date) => {
    const tzOffset = -date.getTimezoneOffset();
    const diff = tzOffset >= 0 ? '+' : '-';
    return diff + pad(tzOffset / 60) + ':' + pad(tzOffset % 60);
};

function convertDateStringToIso(dateString: string): string {
    const date = new Date(dateString);

    const isoDate =
        date.getFullYear() +
        '-' +
        pad(date.getMonth() + 1) +
        '-' +
        pad(date.getDate()) +
        'T' +
        pad(date.getHours()) +
        ':' +
        pad(date.getMinutes()) +
        ':' +
        pad(date.getSeconds()) +
        getTimezoneOffset(date);
    console.log(isoDate);
    return isoDate;
}

function convertHHMMToMinutesSinceMidnight(hhmm: string): number {
    const [hh, mm] = hhmm.split(':').map(Number);
    return hh * 60 + mm;
}

function getCurrentTimezone(): string {
    return Intl.DateTimeFormat().resolvedOptions().timeZone;
}

/**
 * @params ISO format date string in any timezone
 * @returns ISO format date string in UTC timezone
 */
function convertToUUTC(dateString: string): string {
    const date = new Date(dateString);
    const utcDate = new Date(
        date.getUTCFullYear(),
        date.getUTCMonth(),
        date.getUTCDate(),
        date.getUTCHours(),
        date.getUTCMinutes(),
        date.getUTCSeconds()
    );
    return utcDate.toISOString();
}

/**
 * @params ISO format date string in UTC timezone
 * @returns ISO format date string in local timezone
 */
function convertToLocal(dateString: string): string {
    const date = new Date(dateString);
    const localDate = new Date(
        Date.UTC(
            date.getFullYear(),
            date.getMonth(),
            date.getDate(),
            date.getHours(),
            date.getMinutes(),
            date.getSeconds()
        )
    );
    return localDate.toISOString();
}

export {
    convertDateStringToIso,
    getTimezoneOffset,
    convertHHMMToMinutesSinceMidnight,
    getCurrentTimezone,
    convertToUTC,
    convertToLocal,
};
