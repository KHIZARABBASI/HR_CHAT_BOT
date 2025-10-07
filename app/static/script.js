const input = document.querySelector('.message-input');
const sendBtn = document.querySelector('.send-btn');
const chatItems = document.querySelectorAll('.chat-item');
const chatBody = document.querySelector('#chatBody');
const chatWidget = document.querySelector('#chatWidget');

// Chat data (simulated)
const chats = {
    chat1: {
        messages: [
            { text: "Hi there! Need help with your leave request? 😊<br>Would you like to check your balance?", type: 'bot' },
        ],
        // quickReplies: ["Yes, sure!", "No, thanks!"],
        // suggestedReply: "How many days do I have left?",

    }
};

// Load chat
function loadChat(chatId) {
    chatItems.forEach(item => item.classList.remove('active'));
    document.querySelector(`[data-chat="${chatId}"]`).classList.add('active');
    const chat = chats[chatId];
    chatBody.innerHTML = '';
    chat.messages.forEach(msg => {
        const div = document.createElement('div');
        div.classList.add('message', msg.type === 'bot' ? 'bot-message' : 'user-message');
        div.innerHTML = msg.text;
        chatBody.appendChild(div);
    });
    
    if (chat.quickReplies) {
        const quickRepliesDiv = document.createElement('div');
        quickRepliesDiv.classList.add('quick-replies');
        chat.quickReplies.forEach(reply => {
            const btn = document.createElement('button');
            btn.classList.add('quick-reply-btn');
            btn.textContent = reply;
            quickRepliesDiv.appendChild(btn);
        });
        chatBody.appendChild(quickRepliesDiv);
    }
    if (chat.suggestedReply) {
        const suggested = document.createElement('div');
        suggested.classList.add('suggested-reply');
        suggested.textContent = chat.suggestedReply;
        chatBody.appendChild(suggested);
    }
    chatBody.scrollTop = chatBody.scrollHeight;


    
}

// Switch chat
chatItems.forEach(item => {
    item.addEventListener('click', () => loadChat(item.getAttribute('data-chat')));
});

// Send message
sendBtn.addEventListener('click', sendMessage);
input.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') sendMessage();
});

async function sendMessage() {
    if (input.value.trim() === '') return;
    const activeChat = document.querySelector('.chat-item.active').getAttribute('data-chat');
    const userMsg = document.createElement('div');
    userMsg.classList.add('message', 'user-message');
    userMsg.textContent = input.value;
    chatBody.appendChild(userMsg);

    const query = input.value
    chats[activeChat].messages.push({ text: input.value, type: 'user' });
    chatBody.scrollTop = chatBody.scrollHeight;
    input.value = '';

    try {
        // Call FastAPI backend
        const response = await fetch("/query", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ query })
        });

        const result = await response.json();

        // Append bot response
        const botMsg = document.createElement('div');
        botMsg.classList.add('message', 'bot-message');
        // botMsg.textContent = result.answer;
        // chatBody.appendChild(botMsg);
        // chats[activeChat].messages.push({ text: result.answer, type: 'bot' });

        // chatBody.scrollTop = chatBody.scrollHeight;
        if (Array.isArray(result.answer)) {
            // Format nicely if it's a list of objects
            botMsg.innerHTML = result.answer.map(item => {
                if (typeof item === "object") {
                    return Object.entries(item).map(([key, value]) => `<b>${key}</b>: ${value}`).join(", ");
                }
                return item;
            }).join("<br>");
        } else if (typeof result.answer === "object") {
            // Handle single object
            botMsg.innerHTML = Object.entries(result.answer)
                .map(([key, value]) => `<b>${key}</b>: ${value}`)
                .join("<br>");
        } else {
            // Normal string/number
            botMsg.textContent = result.answer;
        }
        chatBody.appendChild(botMsg);
        chats[activeChat].messages.push({ text: result.answer, type: 'bot' });
    } catch (error) {
        console.error("Error:", error);
    }


}

// Load initial chat
loadChat('chat1');

// Quick reply functionality
document.querySelectorAll('.quick-reply-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        input.value = btn.textContent;
        sendMessage();
    });
});