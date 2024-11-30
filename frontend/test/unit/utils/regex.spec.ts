import { describe, expect, it } from 'vitest';

describe('regex', () => {
    it('returns true if the string matches any of the patterns', () => {
        const patterns = [/foo/, /bar/];
        expect(matchesAnyPattern('foo', patterns)).toBe(true);
        expect(matchesAnyPattern('bar', patterns)).toBe(true);
        expect(matchesAnyPattern('baz', patterns)).toBe(false);
    });
});
