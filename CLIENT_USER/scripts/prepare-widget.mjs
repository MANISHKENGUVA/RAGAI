import { execFileSync } from 'node:child_process';
import { copyFileSync, mkdirSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const scriptDirectory = dirname(fileURLToPath(import.meta.url));
const repositoryRoot = resolve(scriptDirectory, '../..');
const widgetDirectory = resolve(repositoryRoot, 'Narada_SDK/dist');
const widgetBundle = resolve(widgetDirectory, 'ai-chat-widget.iife.js');
const widgetSourceMap = `${widgetBundle}.map`;
const publicDirectory = resolve(process.cwd(), 'public');

execFileSync('npm', ['run', 'build', '--workspace=@narada/ai-chat-widget'], {
  cwd: repositoryRoot,
  stdio: 'inherit',
});

mkdirSync(publicDirectory, { recursive: true });
copyFileSync(widgetBundle, resolve(publicDirectory, 'ai-chat-widget.iife.js'));
copyFileSync(widgetSourceMap, resolve(publicDirectory, 'ai-chat-widget.iife.js.map'));
