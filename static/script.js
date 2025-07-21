async function sendMessage() {
    let inputField = document.getElementById("userInput");
    let messageText = inputField.value.trim();

    if (!messageText) return;  // Prevent sending empty messages

    let currentChat = document.getElementById("chatTitle").innerText;
    if (!currentChat || currentChat === "New Chat") {
        startNewChat();
        currentChat = document.getElementById("chatTitle").innerText;
    }

    let chatBox = document.getElementById("chatBox");
    
    // Append user message
    let userMessage = document.createElement("div");
    userMessage.classList.add("message", "user-message");
    userMessage.innerText = messageText;
    chatBox.appendChild(userMessage);

    // Store message in localStorage
    let chatHistory = JSON.parse(localStorage.getItem(currentChat)) || [];
    chatHistory.push({ sender: "user", text: messageText });
    localStorage.setItem(currentChat, JSON.stringify(chatHistory));

    // Clear input
    inputField.value = "";

    // Show typing indicator
    let typingIndicator = document.createElement("div");
    typingIndicator.classList.add("message", "ai-message", "typing");
    typingIndicator.innerText = "AI is thinking...";
    chatBox.appendChild(typingIndicator);

    // Get AI response
    try {
        let aiResponse = await getGeminiResponse(messageText);

        // Remove typing indicator
        typingIndicator.remove();

        // Append AI response
        let aiMessage = document.createElement("div");
        aiMessage.classList.add("message", "ai-message");
        aiMessage.innerText = aiResponse;
        chatBox.appendChild(aiMessage);

        // Store AI response
        chatHistory.push({ sender: "ai", text: aiResponse });
        localStorage.setItem(currentChat, JSON.stringify(chatHistory));

        // Scroll to the latest message
        chatBox.scrollTop = chatBox.scrollHeight;
    } catch (error) {
        typingIndicator.innerText = "⚠️ AI response failed. Try again.";
    }
}

// Function to Call Gemini AI API
async function getGeminiResponse(userMessage) {
    const apiKey = "YOUR_GEMINI_API_KEY";  // 🔥 Replace this with your actual API key
    const url = "https://generativelanguage.googleapis.com/v1/models/gemini-1.5-pro:generateText?key=" + apiKey;

    const requestBody = {
        prompt: { text: userMessage },
        temperature: 0.7,
        max_tokens: 200,
    };

    try {
        const response = await fetch(url, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(requestBody),
        });

        const data = await response.json();
        return data.candidates[0]?.output || "⚠️ AI could not generate a response.";
    } catch (error) {
        console.error("Error fetching AI response:", error);
        return "⚠️ AI service is unavailable. Try again later.";
    }
}
