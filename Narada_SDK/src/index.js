import Vue from 'vue';
import VueCustomElement from 'vue-custom-element';
import ChatContainer from './components/ChatContainer.vue';
import UiComponentGallery from './components/UiComponentGallery.vue';
import * as uiComponents from './components/ui';
import widgetStyles from '../dynamic-scss-theme/src/main.scss?inline';

Vue.use(VueCustomElement);

function attachWidgetStyles(root) {
  const rootNode = root.el.getRootNode();

  if (typeof ShadowRoot !== 'undefined' && rootNode instanceof ShadowRoot) {
    root.shadowRoot = rootNode;
    const style = document.createElement('style');
    style.textContent = widgetStyles;
    rootNode.appendChild(style);
  } else {
    root.shadowRoot = document.head;
  }

  return root;
}

Vue.customElement('ai-chat-widget', ChatContainer, {
  props: ['appId', 'apiUrl', 'title', 'welcomeMessage', 'palette', 'theme'],
  shadow: true,
  beforeCreateVueInstance: attachWidgetStyles,
});

Vue.customElement('narada-ui-gallery', UiComponentGallery, {
  props: ['palette', 'theme'],
  shadow: true,
  beforeCreateVueInstance: attachWidgetStyles,
});

ChatContainer.uiComponents = uiComponents;

export default ChatContainer;
