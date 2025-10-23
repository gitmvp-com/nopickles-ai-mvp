// Session management
let sessionId = null;
let orderItems = [];

// DOM elements
const chatMessages = document.getElementById('chatMessages');
const chatForm = document.getElementById('chatForm');
const messageInput = document.getElementById('messageInput');
const sendButton = document.getElementById('sendButton');
const orderItemsContainer = document.getElementById('orderItems');
const totalPriceElement = document.getElementById('totalPrice');
const debugInfo = document.getElementById('debugInfo');
const debugContent = document.getElementById('debugContent');

// Event listeners
chatForm.addEventListener('submit', handleSubmit);

// Handle form submission
async function handleSubmit(e) {
    e.preventDefault();
    
    const message = messageInput.value.trim();
    if (!message) return;
    
    // Disable input while processing
    messageInput.disabled = true;
    sendButton.disabled = true;
    
    // Add user message to chat
    addMessage(message, 'user');
    
    // Clear input
    messageInput.value = '';
    
    try {
        // Send message to API
        const response = await fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: message,
                session_id: sessionId
            })
        });
        
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        
        const data = await response.json();
        
        // Update session ID
        sessionId = data.session_id;
        
        // Add bot response to chat
        addMessage(data.response, 'bot');
        
        // Update order summary
        updateOrderSummary(data.entities, data.total_price);
        
        // Show debug info (optional)
        showDebugInfo(data);
        
    } catch (error) {
        console.error('Error:', error);
        addMessage('Sorry, I encountered an error. Please try again.', 'bot');
    } finally {
        // Re-enable input
        messageInput.disabled = false;
        sendButton.disabled = false;
        messageInput.focus();
    }
}

// Add message to chat
function addMessage(text, sender) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    
    const label = sender === 'user' ? 'You' : 'Assistant';
    contentDiv.innerHTML = `<strong>${label}:</strong> ${escapeHtml(text)}`;
    
    messageDiv.appendChild(contentDiv);
    chatMessages.appendChild(messageDiv);
    
    // Scroll to bottom
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Update order summary
function updateOrderSummary(entities, totalPrice) {
    // Extract items from entities
    const items = entities.filter(e => e.type === 'beverage' || e.type === 'food');
    const sizes = entities.filter(e => e.type === 'size');
    
    // Add new items to order
    items.forEach((item, index) => {
        const size = sizes[index] ? sizes[index].value : null;
        orderItems.push({
            name: item.value,
            size: size
        });
    });
    
    // Update display
    if (orderItems.length === 0) {
        orderItemsContainer.innerHTML = '<p class="empty-order">No items yet</p>';
    } else {
        orderItemsContainer.innerHTML = '';
        orderItems.forEach((item, index) => {
            const itemDiv = document.createElement('div');
            itemDiv.className = 'order-item';
            
            const itemName = document.createElement('div');
            itemName.className = 'item-name';
            itemName.textContent = item.name;
            
            const itemDetails = document.createElement('div');
            itemDetails.className = 'item-details';
            itemDetails.textContent = item.size ? `Size: ${item.size}` : 'Regular';
            
            itemDiv.appendChild(itemName);
            itemDiv.appendChild(itemDetails);
            orderItemsContainer.appendChild(itemDiv);
        });
    }
    
    // Update total price
    totalPriceElement.textContent = totalPrice.toFixed(2);
}

// Show debug information
function showDebugInfo(data) {
    const debug = {
        intent: data.intent,
        entities: data.entities,
        total: data.total_price
    };
    
    debugContent.textContent = JSON.stringify(debug, null, 2);
}

// Escape HTML to prevent XSS
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Initialize
messageInput.focus();
