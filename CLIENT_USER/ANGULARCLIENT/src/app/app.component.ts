import { Component, CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';

@Component({
  selector: 'app-root',
  standalone: true,
  schemas: [CUSTOM_ELEMENTS_SCHEMA],
  template: `
    <main class="page">
      <p class="eyebrow">Angular integration</p>
      <h1>AI chat that fits your Angular app.</h1>
      <p class="intro">
        Register the SDK once with a script tag and use its custom element
        wherever your Angular template needs it.
      </p>
      <div class="code-card">
        <code>&lt;ai-chat-widget app-id="demo-workspace"&gt;&lt;/ai-chat-widget&gt;</code>
      </div>
      <div class="demo-controls" aria-label="Widget appearance controls">
        <label>
          Palette
          <select [value]="palette" (change)="setPalette($event)">
            <option value="indigo-modern">Indigo Modern</option>
            <option value="ocean-blue">Ocean Blue</option>
            <option value="modern-sky-blue">Modern Sky Blue</option>
          </select>
        </label>
        <button type="button" (click)="toggleTheme()">
          Switch to {{ theme === 'light' ? 'dark' : 'light' }} theme
        </button>
      </div>
      <ai-chat-widget
        app-id="demo-workspace"
        api-url="http://localhost:8000/api/chat"
        [attr.palette]="palette"
        [attr.theme]="theme"
      ></ai-chat-widget>
    </main>
  `,
})
export class AppComponent {
  palette = 'indigo-modern';
  theme = 'light';

  setPalette(event: Event): void {
    this.palette = (event.target as HTMLSelectElement).value;
  }

  toggleTheme(): void {
    this.theme = this.theme === 'light' ? 'dark' : 'light';
  }
}
