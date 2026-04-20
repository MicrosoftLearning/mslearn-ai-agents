// Configure marked for safe rendering
marked.setOptions({
    breaks: true,
    gfm: true,
});

const messagesContainer = document.getElementById("chat-messages");
const messageInput = document.getElementById("message-input");
const sendBtn = document.getElementById("send-btn");
const newChatBtn = document.getElementById("new-chat-btn");
const errorToast = document.getElementById("error-toast");

let conversationId = null;
let isWaiting = false;

// Initialize a new conversation on page load
async function initConversation() {
    try {
        const res = await fetch("/api/conversation", { method: "POST" });
        const data = await res.json();
        if (data.error) throw new Error(data.error);
        conversationId = data.conversation_id;
    } catch (err) {
        showError("Failed to connect to agent. Check your server configuration.");
        console.error("Init error:", err);
    }
}

// Send a message to the agent
async function sendMessage(text) {
    if (!text.trim() || isWaiting || !conversationId) return;

    // Remove welcome message if present
    const welcome = messagesContainer.querySelector(".welcome-message");
    if (welcome) welcome.remove();

    // Show user message
    appendMessage("user", text);
    messageInput.value = "";
    autoResize();
    updateSendButton();

    // Show typing indicator
    isWaiting = true;
    updateSendButton();
    const typingEl = showTypingIndicator();

    try {
        const res = await fetch("/api/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                conversation_id: conversationId,
                message: text,
            }),
        });

        const data = await res.json();
        typingEl.remove();

        if (data.error) {
            showError(data.error);
            return;
        }

        appendMessage("agent", data.text, data.citations, data.images);
    } catch (err) {
        typingEl.remove();
        showError("Failed to get response. Please try again.");
        console.error("Chat error:", err);
    } finally {
        isWaiting = false;
        updateSendButton();
    }
}

// Append a message bubble to the chat
function appendMessage(role, text, citations, images) {
    const msg = document.createElement("div");
    msg.className = `message ${role}`;

    const avatar = document.createElement("div");
    avatar.className = "message-avatar";
    avatar.textContent = role === "user" ? "👤" : "🤖";

    const content = document.createElement("div");
    content.className = "message-content";

    if (role === "agent" && text) {
        // Render markdown for agent messages
        content.innerHTML = marked.parse(text);
    } else {
        content.textContent = text;
    }

    // Add citations if present
    if (citations && citations.length > 0) {
        const citationsDiv = document.createElement("div");
        citationsDiv.className = "citations";

        const label = document.createElement("div");
        label.className = "citation-label";
        label.textContent = "Sources";
        citationsDiv.appendChild(label);

        // Deduplicate citations by filename
        const seen = new Set();
        citations.forEach((c) => {
            if (seen.has(c.filename)) return;
            seen.add(c.filename);
            const item = document.createElement("div");
            item.className = "citation-item";
            item.textContent = c.filename;
            citationsDiv.appendChild(item);
        });

        content.appendChild(citationsDiv);
    }

    // Add images if present
    if (images && images.length > 0) {
        images.forEach((img) => {
            const imgDiv = document.createElement("div");
            imgDiv.className = "generated-image";

            const imgEl = document.createElement("img");
            imgEl.src = img.data;
            imgEl.alt = img.filename || "Generated chart";
            imgDiv.appendChild(imgEl);

            if (img.filename) {
                const caption = document.createElement("div");
                caption.className = "image-caption";
                caption.textContent = img.filename;
                imgDiv.appendChild(caption);
            }

            content.appendChild(imgDiv);
        });
    }

    msg.appendChild(avatar);
    msg.appendChild(content);
    messagesContainer.appendChild(msg);
    scrollToBottom();
}

// Show the typing indicator
function showTypingIndicator() {
    const indicator = document.createElement("div");
    indicator.className = "typing-indicator";

    const avatar = document.createElement("div");
    avatar.className = "message-avatar";
    avatar.textContent = "🤖";
    avatar.style.background = "#e8e8e8";

    const dots = document.createElement("div");
    dots.className = "typing-dots";
    dots.innerHTML = "<span></span><span></span><span></span>";

    indicator.appendChild(avatar);
    indicator.appendChild(dots);
    messagesContainer.appendChild(indicator);
    scrollToBottom();

    return indicator;
}

function scrollToBottom() {
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

// Auto-resize textarea as user types
function autoResize() {
    messageInput.style.height = "auto";
    messageInput.style.height =
        Math.min(messageInput.scrollHeight, 120) + "px";
}

function updateSendButton() {
    sendBtn.disabled = !messageInput.value.trim() || isWaiting;
}

function showError(message) {
    errorToast.textContent = message;
    errorToast.classList.add("visible");
    setTimeout(() => errorToast.classList.remove("visible"), 5000);
}

// Start a new conversation
async function startNewChat() {
    messagesContainer.innerHTML = "";
    conversationId = null;

    // Restore welcome message
    messagesContainer.innerHTML = `
        <div class="welcome-message">
            <div class="welcome-icon">💬</div>
            <h2>Welcome to Contoso IT Support</h2>
            <p>Ask me about IT policies, request help with technical issues, or analyze system performance data.</p>
            <div class="suggestion-chips">
                <button class="chip" data-message="What's the policy for password resets?">🔑 Password reset policy</button>
                <button class="chip" data-message="How do I request new software?">💿 Software requests</button>
                <button class="chip" data-message="Analyze the system performance data and identify any concerning trends">📊 Analyze performance data</button>
                <button class="chip" data-message="Create a chart showing CPU usage over time">📈 CPU usage chart</button>
            </div>
        </div>
    `;

    bindChipListeners();
    await initConversation();
}

// Bind click handlers to suggestion chips
function bindChipListeners() {
    document.querySelectorAll(".chip").forEach((chip) => {
        chip.addEventListener("click", () => {
            const message = chip.getAttribute("data-message");
            if (message) sendMessage(message);
        });
    });
}

// Event listeners
messageInput.addEventListener("input", () => {
    autoResize();
    updateSendButton();
});

messageInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        if (!sendBtn.disabled) sendMessage(messageInput.value);
    }
});

sendBtn.addEventListener("click", () => {
    sendMessage(messageInput.value);
});

newChatBtn.addEventListener("click", startNewChat);

// Initialize
bindChipListeners();
initConversation();
