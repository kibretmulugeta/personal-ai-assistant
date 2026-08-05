# Widget Integration Guide

**Embeddable AI Assistant Widget for Portfolio Websites**

---

## 1. Vanilla HTML Script Embedding

Add this snippet to your portfolio HTML file right before `</body>`:

```html
<!-- Load Widget CSS and JS -->
<script src="https://api.alemukibret.dev/widget.js"></script>
<script>
  WebsiteAssistant.init({
    apiKey: "your-api-key",
    apiEndpoint: "https://api.alemukibret.dev/api/v1",
    theme: "dark",             // "dark" | "light"
    position: "bottom-right",  // "bottom-right" | "bottom-left"
    primaryColor: "#6366f1",
    welcomeMessage: "Hello! I am the AI Digital Twin of Alemu Kibret Mulugeta. Ask me about Alemu's research, projects, or download his resume!"
  });
</script>
```

---

## 2. React / Next.js Component Integration

Import `WebsiteAssistantWidget` in your App layout or main portfolio page:

```jsx
import { WebsiteAssistantWidget } from './components/WebsiteAssistantWidget';

export default function PortfolioPage() {
  return (
    <main>
      <h1>Alemu Kibret Mulugeta Portfolio</h1>
      {/* Embedded Floating Widget */}
      <WebsiteAssistantWidget 
        apiEndpoint="https://api.alemukibret.dev/api/v1"
        theme="dark"
        position="bottom-right"
      />
    </main>
  );
}
```
