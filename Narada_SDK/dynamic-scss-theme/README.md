# Narada Dynamic SCSS Theme

This package contains the Sass styles for the reusable Narada UI components.
Component styles use Sass theme tokens directly, so their colors are resolved
at compile time.

## Files

- `src/colors.scss`: palette maps (`$color-map-v01`, `$color-map-v02`,
  `$color-map-v03`) and shared semantic colors.
- `src/themes/theme1/index.scss` and `src/themes/theme2/index.scss`: Sass theme
  tokens (including `$primary-base`) and
  runtime CSS custom properties for every palette and surface theme.
- `src/components/`: component styles for Button, IconButton, TextField,
  Textarea, Select, Checkbox, RadioGroup, Switch, DatePicker, and Rating,
  plus shared field styles and `ChatWidget.scss`.
- `src/main.scss`: stylesheet entry point importing the theme and all component
  styles.

## Use

Import `src/main.scss` once from your app entry point:

```js
import "./src/main.scss";
```

Use the matching component classes under a shared themed root:

```jsx
<div data-palette="indigo-modern" data-theme="light">
  <button className="ui-button ui-button--primary">Primary</button>
  <input className="ui-text-field" aria-label="Name" />
</div>
```

Supported `data-theme` values:

- `light`
- `dark`

Supported `data-palette` values:

- `indigo-modern` (V01 — Indigo Modern)
- `ocean-blue` (V02 — Ocean Blue)
- `modern-sky-blue` (V03 — Modern Sky Blue)

The theme files also emit runtime CSS custom properties for consumers that use
them directly. However, changing `data-palette` or `data-theme` does not change
the component colors: those are compiled from the selected Sass theme. To use a
different compile-time palette, import `theme2/index.scss` instead of
`theme1/index.scss` in `src/main.scss`.

## Notes

- The Sass variables in `src/themes/theme1/index.scss` and `src/themes/theme2/index.scss` use different compile-time palettes.
- The runtime CSS custom properties support consumers that reference those properties directly; component styles use the compile-time Sass tokens.
- The styles use legacy `@import` syntax to match the current Sass setup. Dart Sass 1.80.0 and later may emit deprecation warnings for `@import` and `map-get()`.
