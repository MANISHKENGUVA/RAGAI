This is an example Python project used in Codeanywhere.

[Try it out](https://app.codeanywhere.com/#https://github.com/Codeanywhere-Templates/python)

### Narada embeddable chat widget

This repository now includes a first-pass foundation for the multi-tenant chatbot platform described in the design brief: schema-first validation, component registry metadata, token-based theming, and an OpenRouter provider abstraction that is compatible with Azure OpenAI and OpenAI behind the same interface.

The repository also includes the Vue 2/Vite SDK and runnable plain HTML, React,
Vue, and Angular host examples. Install the npm workspace from the repository
root, then build the SDK and all clients:

```sh
npm install
npm run build
```

Start a host example with `npm run dev:html`, `npm run dev:react`,
`npm run dev:vue`, or `npm run dev:angular`. See
[CLIENT_USER/README.md](./CLIENT_USER/README.md) for configuration details and
the [SDK guide](./Narada_SDK/README.md) for embedding and the streaming API
contract.

### Running the project

Open the terminal and run:
```sh
cd test-project
python -u hello.py
```
Or just press the *Run Code* button found in the top right of the editor panel.
### Want to contribute?

Feel free to [open a PR](https://github.com/Codeanywhere-Templates/python) with any suggestions for this test project 😃 