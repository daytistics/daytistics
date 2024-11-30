import { describe, it, expect } from 'vitest';
import { isValidPassword, isValidEmail, isValidUsername } from '~/utils/validation';

describe('Validation utils', () => {
    it('should validate password', () => {
        expect(isValidPassword('HelloWorld123!')).toBe(true);
        expect(isValidPassword('HelloWorld123§')).toBe(true);
        expect(isValidPassword('HelloWorld123')).toBe(false);
        expect(isValidPassword('HelloWorld!')).toBe(false);
        expect(isValidPassword('helloworld123!')).toBe(false);
        expect(isValidPassword('')).toBe(false);
        expect(isValidPassword('1234567890')).toBe(false);
        expect(isValidPassword('!@#$%^&*()')).toBe(false);
        expect(isValidPassword('HELLOWORLD123!')).toBe(false);
    });

    it('should validate email', () => {
        expect(isValidEmail('hello@gmail.com')).toBe(true);
        expect(isValidEmail('hello')).toBe(false);
        expect(isValidEmail('hello@gmail')).toBe(false);
        expect(isValidEmail('hello@gmail.')).toBe(false);
        expect(isValidEmail('hello@gmail.c')).toBe(false);
    });

    it('should validate username', () => {
        expect(isValidUsername('hello')).toBe(true);
        expect(isValidUsername('hello123')).toBe(true);
        expect(isValidUsername('Hello123')).toBe(true);
        expect(isValidUsername('hell')).toBe(false);
    });
});
