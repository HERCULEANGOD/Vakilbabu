const chatMessages = document.getElementById('chatMessages');
const chatForm = document.getElementById('chatForm');
const messageInput = document.getElementById('messageInput');
const guideToggle = document.getElementById('guideToggle');
const questionGuide = document.getElementById('questionGuide');
const faqTopics = document.getElementById('faqTopics');

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

const loadQuestionGuide = async () => {
  try {
    const response = await fetch('/api/faqs');
    if (!response.ok) {
      throw new Error('Unable to load questions.');
    }

    const categories = await response.json();
    faqTopics.replaceChildren();

    categories.forEach((category, index) => {
      const section = document.createElement('details');
      section.className = 'faq-category';
      section.open = index === 0;

      const heading = document.createElement('summary');
      heading.textContent = category.category;
      section.appendChild(heading);

      const questions = document.createElement('div');
      questions.className = 'faq-questions';
      category.questions.forEach((question) => {
        const button = document.createElement('button');
        button.className = 'faq-question';
        button.type = 'button';
        button.textContent = question;
        button.addEventListener('click', () => {
          messageInput.value = question;
          questionGuide.hidden = true;
          guideToggle.setAttribute('aria-expanded', 'false');
          chatForm.requestSubmit();
        });
        questions.appendChild(button);
      });

      section.appendChild(questions);
      faqTopics.appendChild(section);
    });

    if (categories.length === 0) {
      faqTopics.textContent = 'No questions are available yet.';
    }
  } catch (error) {
    faqTopics.textContent = 'The question guide is unavailable right now.';
  }
};

guideToggle.addEventListener('click', () => {
  const isExpanded = guideToggle.getAttribute('aria-expanded') === 'true';
  guideToggle.setAttribute('aria-expanded', String(!isExpanded));
  questionGuide.hidden = isExpanded;
});

loadQuestionGuide();
chatForm.addEventListener('submit', sendMessage);

addMessage('Hello. I am Babu, the VakilBabu assistant.', 'assistant');
