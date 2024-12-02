import { describe, expect, it } from 'vitest';
import { generateDaytistics } from '~/test/test-utils/mocks';

describe('generateDaytistics', () => {
    it('should generate an array of daytistics', async () => {
        const daytistics = generateDaytistics(3);
        expect(daytistics).toHaveLength(3);
        expect(daytistics[0].id).toBe(1);
        expect(daytistics[1].id).toBe(2);
        expect(daytistics[2].id).toBe(3);
    });
});
