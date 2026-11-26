import { defineConfig } from 'eslint/config';
import prettier from 'eslint-config-prettier/flat';
import vue from 'eslint-plugin-vue';
import tseslint from 'typescript-eslint';
import vueParser from 'vue-eslint-parser';
import { createTypeScriptConfig } from '../typescript/eslint.config.js';

// Keep the sibling TypeScript config when copying this module, or adjust its import.
export function createVueConfig({
  files = ['**/*.{ts,tsx,mts,cts,vue}'],
  tsconfigRootDir = import.meta.dirname,
  plainStyleFiles = ['**/App.vue'],
  // Add explicit async-component/exposed-ref integration paths as needed.
  // Pure TS modules retain all unsafe-* checks. vue-tsc checks these boundaries.
  sfcInteropFiles = ['**/main.ts', '**/router/**/*.{ts,mts,cts}'],
} = {}) {
  return defineConfig(
    createTypeScriptConfig({ files, tsconfigRootDir }),
    {
      name: 'house/vue/common',
      files,
      extends: [vue.configs['flat/recommended']],
      languageOptions: {
        // Use the same extension list for TS and SFCs to avoid project reloads.
        parserOptions: { extraFileExtensions: ['.vue'] },
      },
      rules: {
        'vue/no-ref-object-reactivity-loss': 'error',
        'vue/no-setup-props-reactivity-loss': 'error',
        'vue/require-typed-ref': 'error',
      },
    },
    {
      name: 'house/vue/sfc',
      files: files.map((pattern) => [pattern, '**/*.vue']),
      languageOptions: {
        parser: vueParser,
        parserOptions: {
          parser: tseslint.parser,
          projectService: true,
          tsconfigRootDir,
          extraFileExtensions: ['.vue'],
        },
      },
      rules: {
        // This preset's own globs only match TS extensions. SFC scripts need the
        // same core-rule replacements (including no-undef) as ordinary TS files.
        ...tseslint.configs.eslintRecommended.rules,
        'vue/attribute-hyphenation': ['error', 'always'],
        'vue/block-lang': ['error', { script: { lang: 'ts', required: true } }],
        'vue/block-order': [
          'error',
          { order: ['script', 'template', 'style'] },
        ],
        'vue/component-api-style': ['error', ['script-setup']],
        'vue/component-definition-name-casing': ['error', 'PascalCase'],
        'vue/component-name-in-template-casing': ['error', 'PascalCase'],
        'vue/custom-event-name-casing': ['error', 'camelCase'],
        'vue/define-emits-declaration': ['error', 'type-literal'],
        'vue/define-props-declaration': ['error', 'type-based'],
        'vue/define-props-destructuring': ['error', { destructure: 'always' }],
        'vue/enforce-style-attribute': [
          'error',
          { allow: ['scoped', 'module'] },
        ],
        // Not disabled by eslint-config-prettier 10.1.8; Prettier owns wrapping.
        'vue/first-attribute-linebreak': 'off',
        'vue/html-button-has-type': 'error',
        'vue/no-define-model-default': 'error',
        'vue/no-duplicate-attr-inheritance': 'error',
        'vue/no-import-compiler-macros': 'error',
        'vue/no-mutating-props': ['error', { shallowOnly: false }],
        'vue/no-undef-components': 'error',
        'vue/no-undef-directives': 'error',
        'vue/no-use-v-if-with-v-for': [
          'error',
          { allowUsingIterationVar: false },
        ],
        'vue/no-use-v-else-with-v-for': 'error',
        'vue/no-v-html': 'error',
        'vue/prefer-define-options': 'error',
        'vue/prefer-use-template-ref': 'error',
        'vue/prop-name-casing': ['error', 'camelCase'],
        // Absence can be meaningful. Optional props do not need invented values.
        'vue/require-default-prop': 'off',
        'vue/require-explicit-emits': 'error',
        'vue/require-explicit-slots': 'error',
        'vue/require-v-for-key': 'error',
        'vue/v-bind-style': ['error', 'shorthand'],
        'vue/v-on-event-hyphenation': ['error', 'always', { autofix: true }],
        'vue/v-on-style': ['error', 'shorthand'],
        'vue/v-slot-style': ['error', 'shorthand'],
        'vue/eqeqeq': ['error', 'always', { null: 'ignore' }],
      },
    },
    ...(sfcInteropFiles.length === 0
      ? []
      : [
          {
            name: 'house/vue/sfc-type-interop',
            files: files.flatMap((pattern) =>
              sfcInteropFiles.map((interopPattern) => [
                pattern,
                interopPattern,
              ]),
            ),
            rules: {
              '@typescript-eslint/no-unsafe-argument': 'off',
              '@typescript-eslint/no-unsafe-assignment': 'off',
              '@typescript-eslint/no-unsafe-return': 'off',
              '@typescript-eslint/no-unsafe-call': 'off',
              '@typescript-eslint/no-unsafe-member-access': 'off',
            },
          },
        ]),
    ...(plainStyleFiles.length === 0
      ? []
      : [
          {
            name: 'house/vue/explicit-plain-style-boundaries',
            files: files.flatMap((pattern) =>
              plainStyleFiles.map((plainPattern) => [
                pattern,
                '**/*.vue',
                plainPattern,
              ]),
            ),
            rules: {
              'vue/enforce-style-attribute': [
                'error',
                { allow: ['scoped', 'module', 'plain'] },
              ],
            },
          },
        ]),
    // Disable layout rules introduced after the TypeScript compatibility layer.
    prettier,
  );
}

export default createVueConfig();
