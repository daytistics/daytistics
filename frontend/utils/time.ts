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
 * Converts 24 hour time string (HH:m) to minutes since midnight
 * @params ISO format date string in UTC timezone
 * @returns ISO format date string in local timezone
 */
function convert24toMinutes(time: string): number {
    const [hours, minutes] = time.split(':').map((str) => parseInt(str, 10));
    return hours * 60 + minutes;
}

const localeDateFormat = () => {
    const formats = {
        'af-ZA': 'yyyy/m/dd',
        'am-ET': 'd/M/yyyy',
        'ar-AE': 'dd/m/yyyy',
        'ar-BH': 'dd/m/yyyy',
        'ar-DZ': 'dd-mm-yyyy',
        'ar-EG': 'dd/m/yyyy',
        'ar-IQ': 'dd/m/yyyy',
        'ar-JO': 'dd/m/yyyy',
        'ar-KW': 'dd/m/yyyy',
        'ar-LB': 'dd/m/yyyy',
        'ar-LY': 'dd/m/yyyy',
        'ar-MA': 'dd-mm-yyyy',
        'ar-OM': 'dd/m/yyyy',
        'ar-QA': 'dd/m/yyyy',
        'ar-SA': 'dd/m/yy',
        'ar-SY': 'dd/m/yyyy',
        'ar-TN': 'dd-mm-yyyy',
        'ar-YE': 'dd/m/yyyy',
        'arn-CL': 'dd-mm-yyyy',
        'as-IN': 'dd-mm-yyyy',
        'az-Cyrl-AZ': 'dd.mm.yyyy',
        'az-Latn-AZ': 'dd.mm.yyyy',
        'ba-RU': 'dd.mm.yy',
        'be-BY': 'dd.mm.yyyy',
        'bg-BG': 'dd.mm.yyyy',
        'bn-BD': 'dd-mm-yy',
        'bn-IN': 'dd-mm-yy',
        'bo-CN': 'yyyy/M/d',
        'br-FR': 'dd/m/yyyy',
        'bs-Cyrl-BA': 'd.mm.yyyy',
        'bs-Latn-BA': 'd.mm.yyyy',
        'ca-ES': 'dd/m/yyyy',
        'co-FR': 'dd/m/yyyy',
        'cs-CZ': 'd.mm.yyyy',
        'cy-GB': 'dd/m/yyyy',
        'da-DK': 'dd-mm-yyyy',
        'de-AT': 'dd.mm.yyyy',
        'de-CH': 'dd.mm.yyyy',
        'de-DE': 'dd.mm.yyyy',
        'de-LI': 'dd.mm.yyyy',
        'de-LU': 'dd.mm.yyyy',
        'dsb-DE': 'd. M. yyyy',
        'dv-MV': 'dd/m/yy',
        'el-GR': 'd/M/yyyy',
        'en-029': 'm/dd/yyyy',
        'en-AU': 'd/m/yyyy',
        'en-BZ': 'dd/m/yyyy',
        'en-CA': 'dd/m/yyyy',
        'en-GB': 'dd/m/yyyy',
        'en-IE': 'dd/m/yyyy',
        'en-IN': 'dd-mm-yyyy',
        'en-JM': 'dd/m/yyyy',
        'en-MY': 'd/M/yyyy',
        'en-NZ': 'd/m/yyyy',
        'en-PH': 'M/d/yyyy',
        'en-SG': 'd/M/yyyy',
        'en-TT': 'dd/m/yyyy',
        'en-US': 'M/d/yyyy',
        'en-ZA': 'yyyy/m/dd',
        'en-ZW': 'M/d/yyyy',
        'es-AR': 'dd/m/yyyy',
        'es-BO': 'dd/m/yyyy',
        'es-CL': 'dd-mm-yyyy',
        'es-CO': 'dd/m/yyyy',
        'es-CR': 'dd/m/yyyy',
        'es-DO': 'dd/m/yyyy',
        'es-EC': 'dd/m/yyyy',
        'es-ES': 'dd/m/yyyy',
        'es-GT': 'dd/m/yyyy',
        'es-HN': 'dd/m/yyyy',
        'es-MX': 'dd/m/yyyy',
        'es-NI': 'dd/m/yyyy',
        'es-PA': 'm/dd/yyyy',
        'es-PE': 'dd/m/yyyy',
        'es-PR': 'dd/m/yyyy',
        'es-PY': 'dd/m/yyyy',
        'es-SV': 'dd/m/yyyy',
        'es-US': 'M/d/yyyy',
        'es-UY': 'dd/m/yyyy',
        'es-VE': 'dd/m/yyyy',
        'et-EE': 'd.mm.yyyy',
        'eu-ES': 'yyyy/m/dd',
        'fa-IR': 'm/dd/yyyy',
        'fi-FI': 'd.mm.yyyy',
        'fil-PH': 'M/d/yyyy',
        'fo-FO': 'dd-mm-yyyy',
        'fr-BE': 'd/m/yyyy',
        'fr-CA': 'yyyy-mm-dd',
        'fr-CH': 'dd.mm.yyyy',
        'fr-FR': 'dd/m/yyyy',
        'fr-LU': 'dd/m/yyyy',
        'fr-MC': 'dd/m/yyyy',
        'fy-NL': 'd-mm-yyyy',
        'ga-IE': 'dd/m/yyyy',
        'gd-GB': 'dd/m/yyyy',
        'gl-ES': 'dd/m/yy',
        'gsw-FR': 'dd/m/yyyy',
        'gu-IN': 'dd-mm-yy',
        'ha-Latn-NG': 'd/M/yyyy',
        'he-IL': 'dd/m/yyyy',
        'hi-IN': 'dd-mm-yyyy',
        'hr-BA': 'd.mm.yyyy.',
        'hr-HR': 'd.mm.yyyy',
        'hsb-DE': 'd. M. yyyy',
        'hu-HU': 'yyyy. m. dd.',
        'hy-AM': 'dd.mm.yyyy',
        'id-ID': 'dd/m/yyyy',
        'ig-NG': 'd/M/yyyy',
        'ii-CN': 'yyyy/M/d',
        'is-IS': 'd.mm.yyyy',
        'it-CH': 'dd.mm.yyyy',
        'it-IT': 'dd/m/yyyy',
        'iu-Cans-CA': 'd/M/yyyy',
        'iu-Latn-CA': 'd/m/yyyy',
        'ja-JP': 'yyyy/m/dd',
        'ka-GE': 'dd.mm.yyyy',
        'kk-KZ': 'dd.mm.yyyy',
        'kl-GL': 'dd-mm-yyyy',
        'km-KH': 'yyyy-mm-dd',
        'kn-IN': 'dd-mm-yy',
        'ko-KR': 'yyyy. m. dd',
        'kok-IN': 'dd-mm-yyyy',
        'ky-KG': 'dd.mm.yy',
        'lb-LU': 'dd/m/yyyy',
        'lo-LA': 'dd/m/yyyy',
        'lt-LT': 'yyyy.mm.dd',
        'lv-LV': 'yyyy.mm.dd.',
        'mi-NZ': 'dd/m/yyyy',
        'mk-MK': 'dd.mm.yyyy',
        'ml-IN': 'dd-mm-yy',
        'mn-MN': 'yy.mm.dd',
        'mn-Mong-CN': 'yyyy/M/d',
        'moh-CA': 'M/d/yyyy',
        'mr-IN': 'dd-mm-yyyy',
        'ms-BN': 'dd/m/yyyy',
        'ms-MY': 'dd/m/yyyy',
        'mt-MT': 'dd/m/yyyy',
        'nb-NO': 'dd.mm.yyyy',
        'ne-NP': 'M/d/yyyy',
        'nl-BE': 'd/m/yyyy',
        'nl-NL': 'd-mm-yyyy',
        'nn-NO': 'dd.mm.yyyy',
        'nso-ZA': 'yyyy/m/dd',
        'oc-FR': 'dd/m/yyyy',
        'or-IN': 'dd-mm-yy',
        'pa-IN': 'dd-mm-yy',
        'pl-PL': 'dd.mm.yyyy',
        'prs-AF': 'dd/m/yy',
        'ps-AF': 'dd/m/yy',
        'pt-BR': 'd/M/yyyy',
        'pt-PT': 'dd-mm-yyyy',
        'qut-GT': 'dd/m/yyyy',
        'quz-BO': 'dd/m/yyyy',
        'quz-EC': 'dd/m/yyyy',
        'quz-PE': 'dd/m/yyyy',
        'rm-CH': 'dd/m/yyyy',
        'ro-RO': 'dd.mm.yyyy',
        'ru-RU': 'dd.mm.yyyy',
        'rw-RW': 'M/d/yyyy',
        'sa-IN': 'dd-mm-yyyy',
        'sah-RU': 'm.dd.yyyy',
        'se-FI': 'd.mm.yyyy',
        'se-NO': 'dd.mm.yyyy',
        'se-SE': 'yyyy-mm-dd',
        'si-LK': 'yyyy-mm-dd',
        'sk-SK': 'd. M. yyyy',
        'sl-SI': 'd.mm.yyyy',
        'sma-NO': 'dd.mm.yyyy',
        'sma-SE': 'yyyy-mm-dd',
        'smj-NO': 'dd.mm.yyyy',
        'smj-SE': 'yyyy-mm-dd',
        'smn-FI': 'd.mm.yyyy',
        'sms-FI': 'd.mm.yyyy',
        'sq-AL': 'yyyy-mm-dd',
        'sr-Cyrl-BA': 'd.mm.yyyy',
        'sr-Cyrl-CS': 'd.mm.yyyy',
        'sr-Cyrl-ME': 'd.mm.yyyy',
        'sr-Cyrl-RS': 'd.mm.yyyy',
        'sr-Latn-BA': 'd.mm.yyyy',
        'sr-Latn-CS': 'd.mm.yyyy',
        'sr-Latn-ME': 'd.mm.yyyy',
        'sr-Latn-RS': 'd.mm.yyyy',
        'sv-FI': 'd.mm.yyyy',
        'sv-SE': 'yyyy-mm-dd',
        'sw-KE': 'M/d/yyyy',
        'syr-SY': 'dd/m/yyyy',
        'ta-IN': 'dd-mm-yyyy',
        'te-IN': 'dd-mm-yy',
        'tg-Cyrl-TJ': 'dd.mm.yy',
        'th-TH': 'd/M/yyyy',
        'tk-TM': 'dd.mm.yy',
        'tn-ZA': 'yyyy/m/dd',
        'tr-TR': 'dd.mm.yyyy',
        'tt-RU': 'dd.mm.yyyy',
        'tzm-Latn-DZ': 'dd-mm-yyyy',
        'ug-CN': 'yyyy-mm-d',
        'uk-UA': 'dd.mm.yyyy',
        'ur-PK': 'dd/m/yyyy',
        'uz-Cyrl-UZ': 'dd.mm.yyyy',
        'uz-Latn-UZ': 'dd/m yyyy',
        'vi-VN': 'dd/m/yyyy',
        'wo-SN': 'dd/m/yyyy',
        'xh-ZA': 'yyyy/m/dd',
        'yo-NG': 'd/M/yyyy',
        'zh-CN': 'yyyy/M/d',
        'zh-HK': 'd/M/yyyy',
        'zh-MO': 'd/M/yyyy',
        'zh-SG': 'd/M/yyyy',
        'zh-TW': 'yyyy/M/d',
        'zu-ZA': 'yyyy/m/dd',
    };

    return formats[navigator.language as keyof typeof formats] || 'dd/m/yyyy';
};

export {
    convertToIsoDate,
    getCurrentTimezone,
    convertToUTC,
    convertToLocal,
    convertTimeToIsoString,
    convert24toMinutes,
    localeDateFormat,
};
