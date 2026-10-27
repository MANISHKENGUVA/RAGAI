# Narada Dynamic SCSS Theme

This package contains Sass styles for the reusable Narada UI components and
the embeddable chat widget. The chat widget consumes semantic CSS custom
properties for its palette and light/dark surfaces at runtime. The standalone
UI component styles still compile Sass theme tokens into the selected palette.

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

The theme files emit runtime CSS custom properties. The widget's `.widget-shell`
uses `data-palette` and `data-theme` to select those tokens dynamically. The
standalone component styles (for example `.ui-button`) continue to use the
compile-time palette selected by `src/main.scss`; import `theme2/index.scss`
there to change that palette.

## Notes

- Runtime palette/surface switching is used by the chat widget; other library component styles remain compile-time themed.
- The styles use legacy `@import` syntax to match the current Sass setup. Dart Sass 1.80.0 and later may emit deprecation warnings for `@import` and `map-get()`.
