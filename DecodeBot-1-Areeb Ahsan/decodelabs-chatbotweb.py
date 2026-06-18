from flask import Flask, request, jsonify, render_template_string
import datetime

app = Flask(__name__)

# ============================================
# DECODELABS INTERNSHIP PROJECT
# Rule-Based AI Chatbot - IPO Model
# Web Interface via Flask
# Author Areeb Ahsan
# ============================================

# ---- KNOWLEDGE BASE (Dictionary) ----
knowledge_base = {
    # Greetings
    "hello": "Hello! I'm DecodeBot. How can I help you today?",
    "hello!": "Hello! I'm DecodeBot. How can I help you today?",
    "hi": "Hi there! What can I do for you?",
    "hi!": "Hi there! What can I do for you?",
    "hey": "Hey! How can I assist you today?",
    "hey!": "Hey! How can I assist you today?",

    # Farewells
    "bye": "Goodbye! Have a great day!",
    "goodbye": "See you later! Take care!",
    "arrivederci": "Until we meet again good sir, take rest",
    "see you": "See you later! Take care!",
    "see you later": "Bye! Come back anytime!",

    # About
    "what is your name": "I am DecodeBot, a rule-based chatbot built for DecodeLabs!",
    "what is your name?": "I am DecodeBot, a rule-based chatbot built for DecodeLabs!",
    "who are you": "I am DecodeBot, your AI assistant created during the DecodeLabs internship.",
    "who are you?": "I am DecodeBot, your AI assistant created during the DecodeLabs internship.",
    "what can you do": "I can answer basic questions, greet you, and have simple conversations!",
    "what can you do?": "I can answer basic questions, greet you, and have simple conversations!",
    "what else can you do": "I am DecodeBot, I'm simply an AI assistant which can only greet, bid farewell, and answer basic questions!",
    "are you a bot": "Yes! I am a rule-based chatbot built with Python.",
    "are you a bot?": "Yes! I am a rule-based chatbot built with Python.",
    "are you human": "No, I am a bot! But I try my best to be helpful.",
    "are you human?": "No, I am a bot! But I try my best to be helpful.",

    # Small talk
    "how are you": "I'm just a bot, but I'm doing great! How about you?",
    "how are you?": "I'm just a bot, but I'm doing great! How about you?",
    "what's up": "Not much! Just here to help you. What do you need?",
    "whats up": "Not much! Just here to help you. What do you need?",
    "thank you": "You're welcome! Is there anything else I can help with?",
    "thanks": "Happy to help! Anything else?",
    "im tired": "I'm sorry to hear that! Is there anything else I can help with?",
    "i'm tired": "I'm sorry to hear that! Is there anything else I can help with?",
    "im upset": "I'm sorry to hear that! Eat Healthy, Grind Harder, Earn Good, Travel the World & live life to the fullest!",
    "i'm upset": "I'm sorry to hear that! Eat Healthy, Grind Harder, Earn Good, Travel the World & live life to the fullest!",
    "ok": "Alright! Let me know if you need anything.",
    "okay": "Sure! Let me know if you need anything.",
    "cool": "Glad you think so! Anything else I can help with?",
    "tell me a joke": "Why do programmers prefer dark mode? Because light attracts bugs! 😄",
    "another joke": "Why did the Python programmer wear glasses? Because he couldn't C! 😂",

    # Help
    "help": "You can ask me: greetings, how I am, what I can do, jokes, or just chat!",
}

# ---- INPUT SANITIZATION ----
# NOTE: Sanitization is intentionally set to lowercase (.lower()) only,
# as per the project requirement of the IPO Model.
# This means all user input (Hi, HI, hI) is auto-converted to lowercase
# before lookup — eliminating the need for uppercase keys in the knowledge base.
# If required, uppercase handling could also be added by removing .lower()
# and manually adding uppercase variations in the knowledge base instead.
def sanitize(user_input):
    """Normalize input: lowercase + strip whitespace"""
    return user_input.lower().strip()

# ---- RESPONSE ENGINE (.get() method) ----
def get_response(user_input):
    """Lookup intent with fallback in single atomic operation"""
    clean_input = sanitize(user_input)
    # EXIT STRATEGY check
    if clean_input in ["quit", "exit"]:
        return "EXIT"
    return knowledge_base.get(clean_input, "I'm not sure about that. Type 'help' to see what I can do!")

# ---- HTML TEMPLATE ----
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DecodeBot — DecodeLabs AI</title>
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">
    <style>
        *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

        :root {
            --bg:        #0a0a0f;
            --surface:   #111118;
            --panel:     #16161f;
            --border:    #1e1e2e;
            --accent:    #7c6aff;
            --accent2:   #4fc3f7;
            --green:     #4ade80;
            --text:      #e2e8f0;
            --muted:     #64748b;
            --bot-bg:    #13131c;
            --user-bg:   #1a1040;
        }

        body {
            background: var(--bg);
            color: var(--text);
            font-family: 'Inter', sans-serif;
            height: 100vh;
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }

        /* ── HEADER ── */
        header {
            background: var(--surface);
            border-bottom: 1px solid var(--border);
            padding: 0 28px;
            height: 64px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            flex-shrink: 0;
        }

        .brand {
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .brand-icon {
            width: 36px;
            height: 36px;
            background: linear-gradient(135deg, var(--accent), var(--accent2));
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 18px;
        }

        .brand-text {
            display: flex;
            flex-direction: column;
        }

        .brand-name {
            font-family: 'JetBrains Mono', monospace;
            font-weight: 700;
            font-size: 15px;
            color: var(--text);
            letter-spacing: 0.5px;
        }

        .brand-sub {
            font-size: 11px;
            color: var(--muted);
            letter-spacing: 0.3px;
        }

        .status-pill {
            display: flex;
            align-items: center;
            gap: 7px;
            background: rgba(74, 222, 128, 0.08);
            border: 1px solid rgba(74, 222, 128, 0.2);
            border-radius: 20px;
            padding: 5px 12px;
            font-size: 12px;
            color: var(--green);
            font-family: 'JetBrains Mono', monospace;
        }

        .status-dot {
            width: 7px;
            height: 7px;
            background: var(--green);
            border-radius: 50%;
            animation: pulse 2s infinite;
        }

        @keyframes pulse {
            0%, 100% { opacity: 1; transform: scale(1); }
            50% { opacity: 0.5; transform: scale(0.85); }
        }

        /* ── MAIN LAYOUT ── */
        .main {
            display: flex;
            flex: 1;
            overflow: hidden;
        }

        /* ── SIDEBAR ── */
        .sidebar {
            width: 240px;
            background: var(--surface);
            border-right: 1px solid var(--border);
            padding: 24px 16px;
            display: flex;
            flex-direction: column;
            gap: 6px;
            flex-shrink: 0;
        }

        .sidebar-label {
            font-size: 10px;
            color: var(--muted);
            font-family: 'JetBrains Mono', monospace;
            letter-spacing: 1.5px;
            text-transform: uppercase;
            padding: 0 8px;
            margin-bottom: 6px;
        }

        .quick-btn {
            background: transparent;
            border: 1px solid transparent;
            border-radius: 8px;
            padding: 9px 12px;
            color: var(--muted);
            font-size: 13px;
            cursor: pointer;
            text-align: left;
            transition: all 0.15s;
            font-family: 'Inter', sans-serif;
        }

        .quick-btn:hover {
            background: var(--panel);
            border-color: var(--border);
            color: var(--text);
        }

        .quick-btn span {
            margin-right: 8px;
        }

        .sidebar-divider {
            height: 1px;
            background: var(--border);
            margin: 12px 0;
        }

        .sidebar-info {
            margin-top: auto;
            padding: 12px;
            background: var(--panel);
            border-radius: 10px;
            border: 1px solid var(--border);
        }

        .sidebar-info-title {
            font-size: 11px;
            font-family: 'JetBrains Mono', monospace;
            color: var(--accent);
            margin-bottom: 6px;
        }

        .sidebar-info-text {
            font-size: 11px;
            color: var(--muted);
            line-height: 1.6;
        }

        /* ── CHAT AREA ── */
        .chat-container {
            flex: 1;
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }

        .messages {
            flex: 1;
            overflow-y: auto;
            padding: 28px 32px;
            display: flex;
            flex-direction: column;
            gap: 20px;
            scroll-behavior: smooth;
        }

        .messages::-webkit-scrollbar { width: 4px; }
        .messages::-webkit-scrollbar-track { background: transparent; }
        .messages::-webkit-scrollbar-thumb { background: var(--border); border-radius: 2px; }

        /* ── WELCOME ── */
        .welcome {
            text-align: center;
            padding: 40px 20px;
            opacity: 0;
            animation: fadeUp 0.6s ease forwards;
        }

        .welcome-icon {
            font-size: 48px;
            margin-bottom: 16px;
            display: block;
        }

        .welcome h2 {
            font-size: 22px;
            font-weight: 600;
            color: var(--text);
            margin-bottom: 8px;
        }

        .welcome p {
            font-size: 14px;
            color: var(--muted);
            line-height: 1.6;
            max-width: 380px;
            margin: 0 auto;
        }

        .welcome-tags {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            justify-content: center;
            margin-top: 20px;
        }

        .welcome-tag {
            background: var(--panel);
            border: 1px solid var(--border);
            border-radius: 20px;
            padding: 5px 12px;
            font-size: 12px;
            color: var(--muted);
            font-family: 'JetBrains Mono', monospace;
        }

        @keyframes fadeUp {
            from { opacity: 0; transform: translateY(12px); }
            to   { opacity: 1; transform: translateY(0); }
        }

        /* ── MESSAGES ── */
        .message {
            display: flex;
            gap: 12px;
            align-items: flex-start;
            animation: fadeUp 0.3s ease forwards;
            max-width: 780px;
        }

        .message.user {
            flex-direction: row-reverse;
            align-self: flex-end;
        }

        .avatar {
            width: 34px;
            height: 34px;
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 16px;
            flex-shrink: 0;
        }

        .avatar.bot {
            background: linear-gradient(135deg, var(--accent), var(--accent2));
        }

        .avatar.user {
            background: var(--user-bg);
            border: 1px solid var(--accent);
            font-size: 13px;
            color: var(--accent);
            font-family: 'JetBrains Mono', monospace;
            font-weight: 700;
        }

        .bubble {
            padding: 12px 16px;
            border-radius: 14px;
            font-size: 14px;
            line-height: 1.6;
            max-width: 520px;
        }

        .bubble.bot {
            background: var(--bot-bg);
            border: 1px solid var(--border);
            border-top-left-radius: 4px;
            color: var(--text);
        }

        .bubble.user {
            background: var(--user-bg);
            border: 1px solid rgba(124, 106, 255, 0.3);
            border-top-right-radius: 4px;
            color: var(--text);
        }

        .msg-time {
            font-size: 10px;
            color: var(--muted);
            font-family: 'JetBrains Mono', monospace;
            margin-top: 5px;
            padding: 0 4px;
        }

        .message.user .msg-time {
            text-align: right;
        }

        /* ── TYPING INDICATOR ── */
        .typing {
            display: flex;
            gap: 12px;
            align-items: center;
            animation: fadeUp 0.3s ease forwards;
        }

        .typing-dots {
            background: var(--bot-bg);
            border: 1px solid var(--border);
            border-radius: 14px;
            border-top-left-radius: 4px;
            padding: 14px 18px;
            display: flex;
            gap: 5px;
            align-items: center;
        }

        .typing-dot {
            width: 7px;
            height: 7px;
            background: var(--muted);
            border-radius: 50%;
            animation: typingBounce 1.2s infinite;
        }

        .typing-dot:nth-child(2) { animation-delay: 0.2s; }
        .typing-dot:nth-child(3) { animation-delay: 0.4s; }

        @keyframes typingBounce {
            0%, 60%, 100% { transform: translateY(0); opacity: 0.4; }
            30% { transform: translateY(-6px); opacity: 1; }
        }

        /* ── INPUT AREA ── */
        .input-area {
            padding: 20px 32px 24px;
            border-top: 1px solid var(--border);
            background: var(--surface);
        }

        .input-row {
            display: flex;
            gap: 12px;
            align-items: flex-end;
            background: var(--panel);
            border: 1px solid var(--border);
            border-radius: 14px;
            padding: 12px 16px;
            transition: border-color 0.2s;
        }

        .input-row:focus-within {
            border-color: var(--accent);
        }

        #userInput {
            flex: 1;
            background: transparent;
            border: none;
            outline: none;
            color: var(--text);
            font-size: 14px;
            font-family: 'Inter', sans-serif;
            resize: none;
            max-height: 120px;
            line-height: 1.5;
        }

        #userInput::placeholder {
            color: var(--muted);
        }

        .send-btn {
            width: 38px;
            height: 38px;
            background: linear-gradient(135deg, var(--accent), var(--accent2));
            border: none;
            border-radius: 10px;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
            transition: opacity 0.2s, transform 0.15s;
        }

        .send-btn:hover { opacity: 0.85; transform: scale(1.05); }
        .send-btn:active { transform: scale(0.95); }

        .send-btn svg {
            width: 18px;
            height: 18px;
            fill: white;
        }

        .input-hint {
            font-size: 11px;
            color: var(--muted);
            text-align: center;
            margin-top: 10px;
            font-family: 'JetBrains Mono', monospace;
        }

        .input-hint kbd {
            background: var(--panel);
            border: 1px solid var(--border);
            border-radius: 4px;
            padding: 1px 5px;
            font-size: 10px;
        }
    </style>
</head>
<body>

<!-- HEADER -->
<header>
    <div class="brand">
        <div class="brand-icon">🤖</div>
        <div class="brand-text">
            <span class="brand-name">DecodeBot</span>
            <span class="brand-sub">DecodeLabs AI — IPO Model</span>
        </div>
    </div>
    <div class="status-pill">
        <div class="status-dot"></div>
        Online
    </div>
</header>

<div class="main">

    <!-- SIDEBAR -->
    <aside class="sidebar">
        <div class="sidebar-label">Quick Prompts</div>

        <button class="quick-btn" onclick="sendQuick('hello')"><span>👋</span>Say Hello</button>
        <button class="quick-btn" onclick="sendQuick('how are you')"><span>💬</span>How are you?</button>
        <button class="quick-btn" onclick="sendQuick('what is your name')"><span>🤖</span>Your name?</button>
        <button class="quick-btn" onclick="sendQuick('what can you do')"><span>⚡</span>What can you do?</button>
        <button class="quick-btn" onclick="sendQuick('tell me a joke')"><span>😄</span>Tell a joke</button>
        <button class="quick-btn" onclick="sendQuick('help')"><span>🆘</span>Help</button>

        <div class="sidebar-divider"></div>

        <button class="quick-btn" onclick="sendQuick('i am tired')"><span>😴</span>I'm tired</button>
        <button class="quick-btn" onclick="sendQuick('i am upset')"><span>😔</span>I'm upset</button>
        <button class="quick-btn" onclick="sendQuick('bye')"><span>👋</span>Goodbye</button>

        <div class="sidebar-info">
            <div class="sidebar-info-title">// Architecture</div>
            <div class="sidebar-info-text">
                IPO Model<br>
                Rule-Based · .get() Fallback<br>
                Input Sanitization Active<br>
                Discrete Intent Mapping
            </div>
        </div>
    </aside>

    <!-- CHAT -->
    <div class="chat-container">
        <div class="messages" id="messages">
            <div class="welcome" id="welcome">
                <span class="welcome-icon">🤖</span>
                <h2>Hey, I'm DecodeBot</h2>
                <p>A rule-based AI built on the IPO Model during the DecodeLabs internship. Ask me anything or pick a prompt from the sidebar.</p>
                <div class="welcome-tags">
                    <span class="welcome-tag">IPO Model</span>
                    <span class="welcome-tag">Rule-Based</span>
                    <span class="welcome-tag">.get() Fallback</span>
                    <span class="welcome-tag">Python</span>
                </div>
            </div>
        </div>

        <!-- INPUT -->
        <div class="input-area">
            <div class="input-row">
                <textarea id="userInput" rows="1" placeholder="Type a message..." onkeydown="handleKey(event)" oninput="autoResize(this)"></textarea>
                <button class="send-btn" onclick="sendMessage()">
                    <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                        <path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"/>
                    </svg>
                </button>
            </div>
            <div class="input-hint">Press <kbd>Enter</kbd> to send · <kbd>Shift+Enter</kbd> for new line</div>
        </div>
    </div>
</div>

<script>
    function getTime() {
        return new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    }

    function autoResize(el) {
        el.style.height = 'auto';
        el.style.height = Math.min(el.scrollHeight, 120) + 'px';
    }

    function handleKey(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    }

    function hideWelcome() {
        const w = document.getElementById('welcome');
        if (w) w.style.display = 'none';
    }

    function appendMessage(text, sender) {
        hideWelcome();
        const messages = document.getElementById('messages');
        const div = document.createElement('div');
        div.className = `message ${sender}`;

        const avatar = document.createElement('div');
        avatar.className = `avatar ${sender}`;
        avatar.textContent = sender === 'bot' ? '🤖' : 'ME';

        const content = document.createElement('div');

        const bubble = document.createElement('div');
        bubble.className = `bubble ${sender}`;
        bubble.textContent = text;

        const time = document.createElement('div');
        time.className = 'msg-time';
        time.textContent = getTime();

        content.appendChild(bubble);
        content.appendChild(time);
        div.appendChild(avatar);
        div.appendChild(content);
        messages.appendChild(div);
        messages.scrollTop = messages.scrollHeight;
    }

    function showTyping() {
        const messages = document.getElementById('messages');
        const div = document.createElement('div');
        div.className = 'typing';
        div.id = 'typing';

        const avatar = document.createElement('div');
        avatar.className = 'avatar bot';
        avatar.textContent = '🤖';

        const dots = document.createElement('div');
        dots.className = 'typing-dots';
        dots.innerHTML = '<div class="typing-dot"></div><div class="typing-dot"></div><div class="typing-dot"></div>';

        div.appendChild(avatar);
        div.appendChild(dots);
        messages.appendChild(div);
        messages.scrollTop = messages.scrollHeight;
    }

    function hideTyping() {
        const t = document.getElementById('typing');
        if (t) t.remove();
    }

    async function sendMessage() {
        const input = document.getElementById('userInput');
        const text = input.value.trim();
        if (!text) return;

        appendMessage(text, 'user');
        input.value = '';
        input.style.height = 'auto';

        showTyping();

        try {
            const res = await fetch('/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: text })
            });
            const data = await res.json();
            setTimeout(() => {
                hideTyping();
                appendMessage(data.response, 'bot');
            }, 600);
        } catch {
            hideTyping();
            appendMessage("Connection error. Is the server running?", 'bot');
        }
    }

    function sendQuick(text) {
        document.getElementById('userInput').value = text;
        sendMessage();
    }
</script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message', '')
    response = get_response(user_message)
    if response == "EXIT":
        response = "Goodbye! Close the browser tab to exit. 👋"
    return jsonify({'response': response})

if __name__ == '__main__':
    print("=" * 45)
    print("   DecodeBot - DecodeLabs AI Web Interface")
    print("=" * 45)
    print("   Server running at: http://localhost:5000")
    print("   Press CTRL+C to stop.\n")
    app.run(debug=True, port=5000)