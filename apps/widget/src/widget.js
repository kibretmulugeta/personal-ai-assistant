/**
 * Personal Website AI Assistant - Embeddable Floating Widget
 * Digital Twin of Kibret Mulugeta
 * Version: 1.0.0
 */

(function () {
  'use strict';

  var WebsiteAssistant = {
    config: {
      apiKey: '',
      apiEndpoint: 'http://localhost:8000/api/v1',
      theme: 'dark',
      position: 'bottom-right',
      primaryColor: '#6366f1',
      welcomeMessage: "Hello! I am the AI Digital Twin of Kibret Mulugeta. Ask me about Kibret's research, projects, skills, or download his resume!",
    },
    state: {
      isOpen: false,
      sessionId: 'sess_' + Math.random().toString(36).substring(2, 12),
      messages: [],
      isStreaming: false,
    },
    elements: {},

    init: function (options) {
      if (options) {
        for (var key in options) {
          if (options.hasOwnProperty(key)) {
            this.config[key] = options[key];
          }
        }
      }
      this.injectStyles();
      this.renderWidget();
      this.bindEvents();
      this.addWelcomeMessage();
    },

    injectStyles: function () {
      if (document.getElementById('wa-widget-styles')) return;
      var link = document.createElement('link');
      link.id = 'wa-widget-styles';
      link.rel = 'stylesheet';
      link.href = this.config.apiEndpoint.replace('/api/v1', '') + '/widget.css';
      document.head.appendChild(link);
    },

    renderWidget: function () {
      var container = document.createElement('div');
      container.className = 'wa-widget-container wa-position-' + this.config.position;
      container.setAttribute('data-theme', this.config.theme);

      container.innerHTML = `
        <div class="wa-chat-panel" id="wa-chat-panel">
          <div class="wa-header">
            <div class="wa-header-info">
              <div class="wa-avatar">KM</div>
              <div>
                <div class="wa-title">Kibret Mulugeta AI</div>
                <div class="wa-subtitle">Digital Twin • Online</div>
              </div>
            </div>
            <div class="wa-header-actions">
              <button class="wa-icon-btn" id="wa-theme-btn" title="Toggle Theme">☀️</button>
              <button class="wa-icon-btn" id="wa-reset-btn" title="Reset Chat">🔄</button>
              <button class="wa-icon-btn" id="wa-close-btn" title="Close Panel">✕</button>
            </div>
          </div>
          <div class="wa-body" id="wa-chat-body"></div>
          <div class="wa-footer">
            <div class="wa-input-wrapper">
              <textarea id="wa-chat-input" class="wa-chat-input" placeholder="Ask about research, projects, skills..." rows="1"></textarea>
              <button id="wa-send-btn" class="wa-send-btn" aria-label="Send message">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="22" y1="2" x2="11" y2="13"></line><polygon points="22 2 15 22 11 13 2 9 22 2"></polygon></svg>
              </button>
            </div>
          </div>
        </div>
        <button class="wa-toggle-btn" id="wa-toggle-btn" aria-label="Open AI Assistant">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path></svg>
        </button>
      `;

      document.body.appendChild(container);

      this.elements.container = container;
      this.elements.panel = container.querySelector('#wa-chat-panel');
      this.elements.toggleBtn = container.querySelector('#wa-toggle-btn');
      this.elements.closeBtn = container.querySelector('#wa-close-btn');
      this.elements.resetBtn = container.querySelector('#wa-reset-btn');
      this.elements.themeBtn = container.querySelector('#wa-theme-btn');
      this.elements.body = container.querySelector('#wa-chat-body');
      this.elements.input = container.querySelector('#wa-chat-input');
      this.elements.sendBtn = container.querySelector('#wa-send-btn');
    },

    bindEvents: function () {
      var self = this;

      self.elements.toggleBtn.addEventListener('click', function () {
        self.togglePanel();
      });

      self.elements.closeBtn.addEventListener('click', function () {
        self.togglePanel(false);
      });

      self.elements.resetBtn.addEventListener('click', function () {
        self.resetChat();
      });

      self.elements.themeBtn.addEventListener('click', function () {
        var currentTheme = self.elements.container.getAttribute('data-theme');
        var newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        self.elements.container.setAttribute('data-theme', newTheme);
      });

      self.elements.sendBtn.addEventListener('click', function () {
        self.handleSend();
      });

      self.elements.input.addEventListener('keydown', function (e) {
        if (e.key === 'Enter' && !e.shiftKey) {
          e.preventDefault();
          self.handleSend();
        }
      });
    },

    togglePanel: function (open) {
      var self = this;
      self.state.isOpen = open !== undefined ? open : !self.state.isOpen;
      if (self.state.isOpen) {
        self.elements.panel.classList.add('wa-open');
        self.elements.input.focus();
      } else {
        self.elements.panel.classList.remove('wa-open');
      }
    },

    addWelcomeMessage: function () {
      this.appendMessage('assistant', this.config.welcomeMessage);
    },

    resetChat: function () {
      this.elements.body.innerHTML = '';
      this.state.messages = [];
      this.state.sessionId = 'sess_' + Math.random().toString(36).substring(2, 12);
      this.addWelcomeMessage();
    },

    handleSend: function () {
      var text = this.elements.input.value.trim();
      if (!text || this.state.isStreaming) return;

      this.appendMessage('user', text);
      this.elements.input.value = '';
      this.streamResponse(text);
    },

    appendMessage: function (role, content) {
      var msgDiv = document.createElement('div');
      msgDiv.className = 'wa-message wa-msg-' + role;

      var bubble = document.createElement('div');
      bubble.className = 'wa-bubble';
      bubble.innerHTML = this.parseMarkdown(content);

      msgDiv.appendChild(bubble);
      this.elements.body.appendChild(msgDiv);
      this.scrollToBottom();

      this.state.messages.push({ role: role, content: content });
      return bubble;
    },

    fetchFallbackResponse: function (query, typingDiv) {
      var self = this;
      fetch(self.config.apiEndpoint + '/chat/message', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: query, session_id: self.state.sessionId }),
      })
        .then(function (res) { return res.json(); })
        .then(function (data) {
          if (typingDiv && typingDiv.parentNode) {
            self.elements.body.removeChild(typingDiv);
          }
          var b = self.appendMessage('assistant', data.response || 'No response received.');
          if (data.action) {
            self.renderActionCard(b, data.action);
          }
          self.state.isStreaming = false;
        })
        .catch(function (err) {
          if (typingDiv && typingDiv.parentNode) {
            self.elements.body.removeChild(typingDiv);
          }
          self.appendMessage('assistant', 'Sorry, I encountered an issue connecting to the AI Digital Twin service.');
          self.state.isStreaming = false;
        });
    },

    streamResponse: function (query) {
      var self = this;
      self.state.isStreaming = true;

      // Show typing bubble
      var typingDiv = document.createElement('div');
      typingDiv.className = 'wa-message wa-msg-assistant';
      typingDiv.innerHTML = `
        <div class="wa-bubble wa-typing">
          <div class="wa-dot"></div><div class="wa-dot"></div><div class="wa-dot"></div>
        </div>
      `;
      self.elements.body.appendChild(typingDiv);
      self.scrollToBottom();

      var streamUrl = self.config.apiEndpoint + '/chat/stream?message=' + encodeURIComponent(query) + '&session_id=' + encodeURIComponent(self.state.sessionId);

      var responseBubble = null;
      var accumulatedText = '';

      if (window.EventSource) {
        var es = new EventSource(streamUrl);

        es.onmessage = function (event) {
          try {
            var data = JSON.parse(event.data);
            if (data.type === 'content' && data.delta) {
              if (!responseBubble) {
                if (typingDiv && typingDiv.parentNode) {
                  self.elements.body.removeChild(typingDiv);
                }
                responseBubble = self.appendMessage('assistant', '');
              }
              accumulatedText += data.delta;
              responseBubble.innerHTML = self.parseMarkdown(accumulatedText);
              if (data.action) {
                self.renderActionCard(responseBubble, data.action);
              }
              self.scrollToBottom();
            } else if (data.type === 'done') {
              es.close();
              self.state.isStreaming = false;
            }
          } catch (e) {
            console.error('SSE Error', e);
          }
        };

        es.onerror = function () {
          es.close();
          if (!responseBubble) {
            // Fallback to standard POST request if SSE fails or buffers on Vercel
            self.fetchFallbackResponse(query, typingDiv);
          } else {
            self.state.isStreaming = false;
          }
        };
      } else {
        self.fetchFallbackResponse(query, typingDiv);
      }
    },

    renderActionCard: function (containerBubble, action) {
      if (!action || !action.name) return;

      var card = document.createElement('div');
      card.className = 'wa-action-card';

      if (action.name === 'download_resume' || action.name === 'download_cv') {
        var url = (action.data && action.data.download_url) ? action.data.download_url : 'https://interactive-portfolio-pied-three.vercel.app/api/resume/download';
        card.innerHTML = `
          <div class="wa-card-title">📄 Professional Resume / CV</div>
          <div class="wa-card-desc">Click below to download Kibret Mulugeta's official resume PDF.</div>
          <a href="${url}" target="_blank" rel="noopener noreferrer" class="wa-btn-primary">Download Resume (PDF)</a>
        `;
      } else if (action.name === 'submit_contact_form') {
        card.innerHTML = `
          <div class="wa-card-title">✉️ Get in Touch</div>
          <div class="wa-card-desc">Send an email directly to Kibret Mulugeta.</div>
          <a href="mailto:Kibretmail@gmail.com" class="wa-btn-primary">Send Email</a>
        `;
      } else if (action.name === 'list_projects') {
        card.innerHTML = `
          <div class="wa-card-title">💻 Explore Projects</div>
          <div class="wa-card-desc">Visit Kibret Mulugeta's GitHub repositories and interactive portfolio.</div>
          <a href="https://github.com/kibretmulugeta" target="_blank" rel="noopener noreferrer" class="wa-btn-primary">View GitHub Profile</a>
        `;
      } else {
        return;
      }

      containerBubble.appendChild(card);
    },

    parseMarkdown: function (str) {
      if (!str) return '';
      var html = str
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\*(.*?)\*/g, '<em>$1</em>')
        .replace(/`([^`]+)`/g, '<code>$1</code>')
        .replace(/\n\n/g, '<br><br>')
        .replace(/\n/g, '<br>');
      return html;
    },

    scrollToBottom: function () {
      if (this.elements.body) {
        this.elements.body.scrollTop = this.elements.body.scrollHeight;
      }
    },
  };

  window.WebsiteAssistant = WebsiteAssistant;
})();
