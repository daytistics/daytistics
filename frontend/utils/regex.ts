function matchesAnyPattern(input: string, patterns: RegExp[]): boolean {
    return patterns.some((pattern) => pattern.test(input));
}

export { matchesAnyPattern };
