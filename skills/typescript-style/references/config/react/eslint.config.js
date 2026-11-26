import { defineConfig } from 'eslint/config';
import prettier from 'eslint-config-prettier/flat';
import jsxA11y from 'eslint-plugin-jsx-a11y';
import react from 'eslint-plugin-react';
import reactHooks from 'eslint-plugin-react-hooks';
import { createTypeScriptConfig } from '../eslint.config.js';

// Keep .ts in scope: custom Hooks need the same checks as .tsx components.
export function createReactConfig({
  files = ['**/*.{ts,tsx,mts,cts}'],
  tsconfigRootDir = import.meta.dirname,
  additionalEffectHooks,
} = {}) {
  return defineConfig(
    createTypeScriptConfig({ files, tsconfigRootDir }),
    {
      name: 'house/react',
      files,
      extends: [
        react.configs.flat.recommended,
        react.configs.flat['jsx-runtime'],
        reactHooks.configs.flat.recommended,
        jsxA11y.flatConfigs.recommended,
      ],
      settings: {
        react: { version: 'detect' },
        ...(additionalEffectHooks === undefined
          ? {}
          : { 'react-hooks': { additionalEffectHooks } }),
      },
      rules: {
        // React 19 and TypeScript replace the old runtime propTypes contract.
        'react/prop-types': 'off',
        'react/require-default-props': 'off',
        'react/button-has-type': 'error',
        'react/function-component-definition': [
          'error',
          {
            namedComponents: 'function-declaration',
            unnamedComponents: 'arrow-function',
          },
        ],
        'react/jsx-filename-extension': ['error', { extensions: ['.tsx'] }],
        'react/jsx-key': [
          'error',
          { checkFragmentShorthand: true, warnOnDuplicates: true },
        ],
        'react/jsx-no-script-url': 'error',
        'react/jsx-pascal-case': 'error',
        'react/no-access-state-in-setstate': 'error',
        'react/no-array-index-key': 'error',
        // A reviewed rich-HTML adapter needs a file-scoped override of this rule.
        'react/no-danger': 'error',
        'react/no-object-type-as-default-prop': 'error',
        'react/no-this-in-sfc': 'error',
        'react/no-unsafe': 'error',
        'react/no-unstable-nested-components': [
          'error',
          { allowAsProps: false },
        ],
        'react/prefer-stateless-function': 'error',
        'react/style-prop-object': 'error',
        'react/void-dom-elements-no-children': 'error',
        'react-hooks/exhaustive-deps': 'error',
        'react-hooks/incompatible-library': 'error',
        'react-hooks/unsupported-syntax': 'error',
        // 7.1.1's component-hook-factories rule is a deprecated no-op. The
        // static-components and no-unstable-nested-components rules stay on.
        // Severity-only override preserves the preset's element/role exclusions.
        'jsx-a11y/control-has-associated-label': 'error',
        'jsx-a11y/no-aria-hidden-on-focusable': 'error',
      },
    },
    // Remains last when framework presets are added after the TypeScript base.
    prettier,
  );
}

export default createReactConfig();
