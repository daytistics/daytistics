import withNuxt from './.nuxt/eslint.config.mjs';

export default withNuxt({
    files: ['**/*.ts', '**/*.tsx', '**/*.js', '**/*.jsx', '**/*.vue'],
    rules: {
        '@typescript-eslint/no-unused-vars': ['error', { argsIgnorePattern: '^_' }],
        '@vue'
    },
});
