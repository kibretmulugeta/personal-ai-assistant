import React, { useEffect } from 'react';

/**
 * WebsiteAssistantWidget - React / Next.js Component Wrapper
 * 
 * Embeds Alemu Kibret Mulugeta's AI Digital Twin Widget into React applications.
 */
export const WebsiteAssistantWidget = ({
  apiKey = '',
  apiEndpoint = 'https://api.alemukibret.dev/api/v1',
  theme = 'dark',
  position = 'bottom-right',
  primaryColor = '#6366f1',
  welcomeMessage = "Hello! I am the AI Digital Twin of Alemu Kibret Mulugeta. Ask me about Alemu's research, projects, skills, or download his resume!",
}) => {
  useEffect(() => {
    // Inject stylesheet
    if (!document.getElementById('wa-widget-styles')) {
      const link = document.createElement('link');
      link.id = 'wa-widget-styles';
      link.rel = 'stylesheet';
      link.href = apiEndpoint.replace('/api/v1', '') + '/widget.css';
      document.head.appendChild(link);
    }

    // Inject script
    const scriptId = 'wa-widget-script';
    let script = document.getElementById(scriptId);

    const initWidget = () => {
      if (window.WebsiteAssistant) {
        window.WebsiteAssistant.init({
          apiKey,
          apiEndpoint,
          theme,
          position,
          primaryColor,
          welcomeMessage,
        });
      }
    };

    if (!script) {
      script = document.createElement('script');
      script.id = scriptId;
      script.src = apiEndpoint.replace('/api/v1', '') + '/widget.js';
      script.async = true;
      script.onload = initWidget;
      document.body.appendChild(script);
    } else {
      initWidget();
    }
  }, [apiKey, apiEndpoint, theme, position, primaryColor, welcomeMessage]);

  return null; // Renders floating widget in portal/DOM root
};

export default WebsiteAssistantWidget;
