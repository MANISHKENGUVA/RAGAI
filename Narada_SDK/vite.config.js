import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue2';

export default defineConfig(({ mode }) => {
  const minified = mode === 'minified';

  return {
    plugins: [vue()],
    define: {
      'process.env.NODE_ENV': JSON.stringify('production'),
    },
    build: {
      minify: minified ? 'esbuild' : false,
      sourcemap: true,
      emptyOutDir: !minified,
      lib: {
        entry: 'src/index.js',
        name: 'NaradaAIChatWidget',
        formats: ['iife', 'umd'],
        fileName: (format) => `ai-chat-widget.${format}${minified ? '.min' : ''}.js`,
      },
      cssCodeSplit: false,
      rollupOptions: {
        output: {
          inlineDynamicImports: true,
        },
      },
    },
  };
});
