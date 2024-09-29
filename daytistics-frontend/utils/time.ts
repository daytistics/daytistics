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

export {
    convertDateStringToIso,
    getTimezoneOffset,
    convertHHMMToMinutesSinceMidnight,
};
