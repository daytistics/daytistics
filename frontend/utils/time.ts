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

function convertTimeToIsoString(
    timeString: string,
    dateString: string,
    preserveTimezone = false
): string {
    const [hours, minutes] = timeString
        .split(':')
        .map((str) => parseInt(str, 10));

    const date = new Date(dateString);
    date.setHours(hours, minutes);

    debugger;

    if (preserveTimezone) {
        return date.toISOString();
    } else {
        // Convert to UTC ISO string with setting of timezone offset
        const utc = Date.UTC(
            date.getUTCFullYear(),
            date.getUTCMonth(),
            date.getUTCDate(),
            date.getUTCHours(),
            date.getUTCMinutes(),
            date.getUTCSeconds(),
            date.getUTCMilliseconds()
        );

        return new Date(utc).toISOString();
    }
}

function convertToIsoDate(date: Date): string {
    const day = String(date.getDate()).padStart(2, '0');
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const year = date.getFullYear();

    return `${year}-${month}-${day}`;
}

/**
 * Converts 24 hour time string (HH:mm) to minutes since midnight
 * @params ISO format date string in UTC timezone
 * @returns ISO format date string in local timezone
 */
function convert24toMinutes(time: string): number {
    const [hours, minutes] = time.split(':').map((str) => parseInt(str, 10));
    return hours * 60 + minutes;
}

export {
    convertToIsoDate,
    getCurrentTimezone,
    convertToUTC,
    convertToLocal,
    convertTimeToIsoString,
    convert24toMinutes,
};
