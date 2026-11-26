import js from '@eslint/js';
import { defineConfig } from 'eslint/config';
import prettier from 'eslint-config-prettier/flat';
import tseslint from 'typescript-eslint';

const restrictedSyntax = [
  {
    selector: 'ExportDefaultDeclaration',
    message:
      'Use named exports; framework-required defaults need a scoped override.',
  },
  {
    selector: 'ExportNamedDeclaration > VariableDeclaration[kind="let"]',
    message: 'Expose mutable state through functions rather than export let.',
  },
  {
    selector: 'TSEnumDeclaration[const=true]',
    message: 'Use an ordinary enum or a literal union instead of const enum.',
  },
];

// Framework additions can pass their file globs and the consuming project root.
// Vue additionally needs vue-eslint-parser and parserOptions.extraFileExtensions.
export function createTypeScriptConfig({
  files = ['**/*.{ts,tsx,mts,cts}'],
  tsconfigRootDir = import.meta.dirname,
} = {}) {
  return defineConfig(
    {
      name: 'house/typescript/ignores',
      ignores: ['**/node_modules/**', '**/dist/**', '**/coverage/**'],
    },
    {
      name: 'house/typescript',
      files,
      extends: [
        js.configs.recommended,
        ...tseslint.configs.strictTypeChecked,
        ...tseslint.configs.stylisticTypeChecked,
      ],
      languageOptions: {
        parserOptions: {
          projectService: true,
          tsconfigRootDir,
        },
      },
      linterOptions: {
        reportUnusedDisableDirectives: 'error',
      },
      rules: {
        eqeqeq: ['error', 'always', { null: 'ignore' }],
        'no-eval': 'error',
        'no-new-func': 'error',
        'no-extend-native': 'error',
        'no-restricted-syntax': ['error', ...restrictedSyntax],
        '@typescript-eslint/array-type': [
          'error',
          { default: 'array-simple', readonly: 'array-simple' },
        ],
        '@typescript-eslint/ban-ts-comment': [
          'error',
          {
            'ts-check': false,
            'ts-expect-error': true,
            'ts-ignore': true,
            'ts-nocheck': true,
          },
        ],
        '@typescript-eslint/consistent-type-assertions': [
          'error',
          { assertionStyle: 'as', objectLiteralTypeAssertions: 'never' },
        ],
        '@typescript-eslint/consistent-type-exports': 'error',
        // The compiler's verbatimModuleSyntax checks type imports. Avoid competing
        // autofixes, especially around Nest's runtime decorator metadata.
        '@typescript-eslint/consistent-type-imports': 'off',
        '@typescript-eslint/explicit-member-accessibility': [
          'error',
          {
            accessibility: 'no-public',
            overrides: { parameterProperties: 'off' },
          },
        ],
        '@typescript-eslint/explicit-module-boundary-types': 'error',
        '@typescript-eslint/no-extraneous-class': [
          'error',
          { allowWithDecorator: true },
        ],
        '@typescript-eslint/no-floating-promises': [
          'error',
          { ignoreVoid: false, ignoreIIFE: false },
        ],
        '@typescript-eslint/no-import-type-side-effects': 'error',
        '@typescript-eslint/no-unused-vars': [
          'error',
          { args: 'all', argsIgnorePattern: '^_', caughtErrors: 'all' },
        ],
        // Strict forbids postfix !, so stylistic must not suggest introducing it.
        '@typescript-eslint/non-nullable-type-assertion-style': 'off',
        '@typescript-eslint/prefer-readonly': 'error',
        '@typescript-eslint/return-await': ['error', 'always'],
        '@typescript-eslint/strict-boolean-expressions': [
          'error',
          { allowString: false, allowNumber: false },
        ],
        '@typescript-eslint/switch-exhaustiveness-check': [
          'error',
          { considerDefaultExhaustiveForUnions: false },
        ],
      },
    },
    {
      name: 'house/typescript/tool-config-defaults',
      files: files.map((pattern) => [pattern, '**/*.config.{ts,mts,cts}']),
      rules: {
        'no-restricted-syntax': [
          'error',
          ...restrictedSyntax.filter(
            ({ selector }) => selector !== 'ExportDefaultDeclaration',
          ),
        ],
      },
    },
    {
      name: 'house/typescript/type-tests',
      files: ['**/*.type-test.ts'],
      rules: {
        '@typescript-eslint/ban-ts-comment': [
          'error',
          {
            'ts-check': false,
            'ts-expect-error': 'allow-with-description',
            'ts-ignore': true,
            'ts-nocheck': true,
            minimumDescriptionLength: 10,
          },
        ],
      },
    },
    prettier,
  );
}

export default createTypeScriptConfig();
