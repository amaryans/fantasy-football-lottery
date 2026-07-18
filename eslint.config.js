import js from '@eslint/js'
import tseslint from 'typescript-eslint'
import reactHooks from 'eslint-plugin-react-hooks'

export default tseslint.config(
  { ignores: ['dist', 'legacy', 'node_modules'] },
  {
    files: ['**/*.{ts,tsx}'],
    extends: [js.configs.recommended, ...tseslint.configs.recommended],
    plugins: {
      'react-hooks': reactHooks,
    },
    rules: {
      ...reactHooks.configs.recommended.rules,
    },
  },
  {
    // The lottery engine stays pure: no React, no network, no ambient randomness.
    files: ['src/engine/**/*.ts'],
    rules: {
      'no-restricted-imports': [
        'error',
        {
          patterns: [
            {
              group: [
                'react',
                'react-dom',
                'zustand',
                '**/data/**',
                '**/state/**',
                '**/components/**',
                '**/screens/**',
              ],
              message: 'engine/ must stay pure (no React, state, or data imports).',
            },
          ],
        },
      ],
      'no-restricted-globals': [
        'error',
        { name: 'fetch', message: 'engine/ must not perform network calls.' },
      ],
      'no-restricted-properties': [
        'error',
        { object: 'Math', property: 'random', message: 'Use the seeded rng from engine/rng.ts.' },
        { object: 'Date', property: 'now', message: 'engine/ must be deterministic.' },
      ],
    },
  },
  {
    // data/ is framework-free.
    files: ['src/data/**/*.ts'],
    rules: {
      'no-restricted-imports': [
        'error',
        {
          patterns: [
            {
              group: ['react', 'react-dom', '**/components/**', '**/screens/**'],
              message: 'data/ must not import React or UI code.',
            },
          ],
        },
      ],
    },
  },
)
