const chatMessages = document.getElementById('chatMessages');
const chatForm = document.getElementById('chatForm');
const messageInput = document.getElementById('messageInput');

const addMessage = (text, sender) => {
  const row = document.createElement('div');
  row.className = `message-row ${sender}`;

  const bubble = document.createElement('div');
  bubble.className = 'message-bubble';
  bubble.textContent = text;

  row.appendChild(bubble);
  chatMessages.appendChild(row);
  chatMessages.scrollTop = chatMessages.scrollHeight;
};

const sendMessage = async (event) => {
  event.preventDefault();

  const text = messageInput.value.trim();
  if (!text) {
    return;
  }

  addMessage(text, 'user');
  messageInput.value = '';
  messageInput.disabled = true;

  try {
    const response = await fetch('/api/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ message: text }),
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data?.detail || 'Unable to process message.');
    }

    addMessage(data.response, 'assistant');
  } catch (error) {
    addMessage('Sorry, please clarify.', 'assistant');
  } finally {
    messageInput.disabled = false;
    messageInput.focus();
  }
};

chatForm.addEventListener('submit', sendMessage);

addMessage('Hello. I am Bengoshi, the VakilBabu assistant.', 'assistant');
