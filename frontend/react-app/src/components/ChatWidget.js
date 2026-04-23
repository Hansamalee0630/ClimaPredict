import React, { useState, useRef, useEffect } from 'react';
import { MessageCircle, X, Send, Bot } from 'lucide-react';
import './ChatWidget.css';

const ChatWidget = ({ dashboardState }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [isClosing, setIsClosing] = useState(false);
  const [messages, setMessages] = useState([
    { role: 'bot', text: 'Hello! I am your ClimaPredict AI assistant. How can I help you analyze the dashboard today?' }
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [showWelcomeMessage, setShowWelcomeMessage] = useState(false);
  
  const messagesEndRef = useRef(null);

  useEffect(() => {
    // Show welcome message every time the page loads/refreshes
    const timer = setTimeout(() => {
      setShowWelcomeMessage(true);
    }, 1500);
    return () => clearTimeout(timer);
  }, []);

  const dismissWelcome = (e) => {
    if (e) e.stopPropagation();
    setShowWelcomeMessage(false);
  };

  // Auto-scroll to bottom of messages
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    if (isOpen) {
      scrollToBottom();
    }
  }, [messages, isOpen]);

  const handleToggle = () => {
    if (showWelcomeMessage) {
      dismissWelcome();
    }
    
    if (isOpen) {
      setIsClosing(true);
      setTimeout(() => {
        setIsOpen(false);
        setIsClosing(false);
      }, 300); // Wait for closing animation
    } else {
      setIsOpen(true);
    }
  };

  const handleSend = async (e) => {
    e?.preventDefault();
    if (!inputValue.trim() || isLoading) return;

    const userMessage = inputValue.trim();
    setInputValue('');
    
    // Add user message to UI
    const updatedMessages = [...messages, { role: 'user', text: userMessage }];
    setMessages(updatedMessages);
    setIsLoading(true);

    try {
      // Build request payload matching Backend expectations
      const payload = {
        message: userMessage,
        history: updatedMessages.map(msg => ({ role: msg.role, text: msg.text })),
        dashboard_state: dashboardState 
      };

      const response = await fetch('http://127.0.0.1:5000/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload)
      });

      if (!response.ok) {
        throw new Error(`API error: ${response.status}`);
      }

      const data = await response.json();
      
      if (data.status === 'success') {
        setMessages(prev => [...prev, { role: 'bot', text: data.reply }]);
      } else {
        throw new Error(data.message || 'Unknown error occurred');
      }

    } catch (error) {
      console.error('Chat error:', error);
      const errorMsg = error.message.includes('API error') 
         ? error.message 
         : error.message || 'Sorry, I am having trouble connecting to the backend. Please ensure the server is running.';
         
      setMessages(prev => [...prev, { 
        role: 'error', 
        text: `Backend Error: ${errorMsg}. If it mentions an AI service error, please check your Google API quota or wait a minute.`
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  // Safely parses **bold** markdown into React strong elements
  const parseMarkdownLine = (text) => {
    if (!text) return null;
    const parts = text.split(/(\*\*.*?\*\*)/g);
    return parts.map((part, i) => {
      if (part.startsWith('**') && part.endsWith('**')) {
        return <strong key={i}>{part.slice(2, -2)}</strong>;
      }
      return part;
    });
  };

  return (
    <div className="chat-widget-container">
      {isOpen && (
        <div className={`chat-window ${isClosing ? 'closing' : ''}`}>
          
          <div className="chat-header">
            <div className="chat-header-title">
              <Bot size={18} color="#a78bfa" />
              <span>ClimaPredict AI</span>
              <div className="live-indicator" title="Connected to active data context"></div>
            </div>
            <button className="chat-close-btn" onClick={handleToggle}>
              <X size={18} />
            </button>
          </div>

          <div className="chat-messages">
            {messages.map((msg, index) => (
              <div key={index} className={`chat-bubble ${msg.role}`}>
                {msg.text.split('\n').map((line, i) => (
                   <span key={i}>
                     {parseMarkdownLine(line)}
                     {i !== msg.text.split('\n').length - 1 && <br />}
                   </span>
                ))}
              </div>
            ))}
            
            {isLoading && (
              <div className="typing-indicator">
                <div className="typing-dot"></div>
                <div className="typing-dot"></div>
                <div className="typing-dot"></div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          <form className="chat-input-area" onSubmit={handleSend}>
            <input
              type="text"
              className="chat-input"
              placeholder="Ask about trends, alerts..."
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              disabled={isLoading}
            />
            <button 
              type="submit" 
              className="chat-send-btn"
              disabled={!inputValue.trim() || isLoading}
            >
              <Send size={18} />
            </button>
          </form>

        </div>
      )}

      {!isOpen && showWelcomeMessage && (
        <div className="chat-welcome-message fade-in-up" onClick={handleToggle}>
          <button className="chat-welcome-close" onClick={(e) => dismissWelcome(e)} title="Dismiss">
            <X size={14} />
          </button>
          <div className="chat-welcome-content">
            <span role="img" aria-label="wave" className="chat-welcome-icon">👋</span>
            <p>Hi! I'm your ClimaPredict AI assistant. Need any help analyzing the dashboard?</p>
          </div>
        </div>
      )}

      <button className="chat-toggle-btn" onClick={handleToggle} title="Chat with AI Assistant">
        {isOpen ? <X size={24} /> : <MessageCircle size={24} />}
      </button>
    </div>
  );
};

export default ChatWidget;
