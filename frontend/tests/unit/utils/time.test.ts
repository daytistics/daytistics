// @ts-ignore
import { expect, test, describe } from 'bun:test';
import { convertTimeToIsoString } from '~/utils/time';

describe('convertTimeToIsoString', () => {
    test('valid inputs and keepTimezone = false', () => {
        const result = convertTimeToIsoString(
            '12:00',
            '2008-01-21T00:00:00+02:00'
        );
        expect(result).toBe('2008-01-21T10:00:00.000Z');
    });

    test('valid inputs and keepTimezone = true', () => {
        const result = convertTimeToIsoString(
            '12:00',
            '2008-01-21T00:00:00+02:00',
            true
        );
        expect(result).toBe('2008-01-21T12:00:00.000Z+02:00');
    });

    test('invalid time input', () => {
        expect(() =>
            convertTimeToIsoString('12:00:00', '2008-01-21T00:00:00')
        ).toThrow('Invalid time input');
    });
});
