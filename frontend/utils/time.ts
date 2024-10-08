const pad = (n) => `${Math.floor(Math.abs(n))}`.padStart(2, '0');
// Get timezone offset in ISO format (+hh:mm or -hh:mm)
const getTimezoneOffset = (date) => {
    const tzOffset = -date.getTimezoneOffset();
    const diff = tzOffset >= 0 ? '+' : '-';
    return diff + pad(tzOffset / 60) + ':' + pad(tzOffset % 60);
};

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
function convertToUTC(isoString: string): string {
    const date = new Date(isoString);
    const utcDate = new Date(
        Date.UTC(
            date.getFullYear(),
            date.getMonth(),
            date.getDate(),
            date.getHours(),
            date.getMinutes(),
            date.getSeconds()
        )
    );
    return utcDate.toISOString();
}

/**
 * @params ISO format date string in UTC timezone
 * @returns ISO format date string in local timezone
 */
function convertToLocal(dateString: string): string {
    const date = new Date(dateString);
    const offset = date.getTimezoneOffset();
    const localDate = new Date(date.getTime() - offset * 60 * 1000);
    return localDate.toISOString();
}

export {
    getTimezoneOffset,
    convertHHMMToMinutesSinceMidnight,
    getCurrentTimezone,
    convertToUTC,
    convertToLocal,
    readableDateFromUTC,
};
