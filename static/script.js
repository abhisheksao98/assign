const chatMessages = document.getElementById('chatMessages');
const chatInput = document.getElementById('chatInput');
const sendButton = document.getElementById('sendButton');
const productsContainer = document.getElementById('productsContainer');

// Add message to chat
function addMessage(text, isUser = false) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    
    // Convert markdown-like formatting to HTML
    let formattedText = text
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\*(.*?)\*/g, '<em>$1</em>')
        .replace(/\n/g, '<br>');
    
    contentDiv.innerHTML = formattedText;
    messageDiv.appendChild(contentDiv);
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Display products
function displayProducts(phones, responseType) {
    if (!phones || phones.length === 0) {
        productsContainer.classList.remove('active');
        return;
    }
    
    productsContainer.classList.add('active');
    
    if (responseType === 'comparison' && phones.length > 1) {
        // Show comparison table
        let html = '<h2 class="products-title">Comparison</h2>';
        html += '<div style="overflow-x: auto;"><table class="comparison-table">';
        html += '<thead><tr><th>Feature</th>';
        phones.forEach(phone => {
            html += `<th>
                <div class="comparison-phone-header">
                    <img src="${phone.image_url || 'https://via.placeholder.com/80x80?text=' + encodeURIComponent(phone.name)}" 
                         alt="${phone.name}" 
                         class="comparison-phone-image"
                         onerror="this.src='https://via.placeholder.com/80x80?text=' + encodeURIComponent('${phone.name}')">
                    <div>${phone.name}</div>
                </div>
            </th>`;
        });
        html += '</tr></thead><tbody>';
        
        const features = [
            { label: 'Price', key: 'price', format: (v) => `₹${v.toLocaleString('en-IN')}` },
            { label: 'Brand', key: 'brand' },
            { label: 'Display', key: 'display' },
            { label: 'Processor', key: 'processor' },
            { label: 'RAM', key: 'ram' },
            { label: 'Storage', key: 'storage' },
            { label: 'Rear Camera', key: 'camera_rear' },
            { label: 'Front Camera', key: 'camera_front' },
            { label: 'Battery', key: 'battery' },
            { label: 'Charging', key: 'charging' },
            { label: 'OS', key: 'os' },
            { label: 'Weight', key: 'weight' },
            { label: 'OIS', key: 'ois' },
            { label: 'EIS', key: 'eis' },
        ];
        
        features.forEach(feature => {
            html += '<tr>';
            html += `<td><strong>${feature.label}</strong></td>`;
            phones.forEach(phone => {
                let value = phone[feature.key];
                if (feature.format) {
                    value = feature.format(value);
                }
                html += `<td>${value || 'N/A'}</td>`;
            });
            html += '</tr>';
        });
        
        html += '</tbody></table></div>';
        productsContainer.innerHTML = html;
    } else {
        // Show product cards
        let html = '<h2 class="products-title">Recommended Phones</h2>';
        html += '<div class="products-grid">';
        
        phones.forEach(phone => {
            html += `
                <div class="product-card">
                    <div class="product-image-container">
                        <img src="${phone.image_url || 'https://via.placeholder.com/300x300?text=' + encodeURIComponent(phone.name)}" 
                             alt="${phone.name}" 
                             class="product-image"
                             onerror="this.src='https://via.placeholder.com/300x300?text=' + encodeURIComponent('${phone.name}')">
                        <div class="product-badge">${phone.brand}</div>
                    </div>
                    <div class="product-header">
                        <div>
                            <div class="product-name">${phone.name}</div>
                            <div class="product-brand">${phone.brand}</div>
                        </div>
                    </div>
                    <div class="product-price">₹${phone.price.toLocaleString('en-IN')}</div>
                    <div class="product-specs">
                        <div class="spec-item">
                            <span class="spec-label">Display</span>
                            <span class="spec-value">${phone.display}</span>
                        </div>
                        <div class="spec-item">
                            <span class="spec-label">Processor</span>
                            <span class="spec-value">${phone.processor}</span>
                        </div>
                        <div class="spec-item">
                            <span class="spec-label">RAM</span>
                            <span class="spec-value">${phone.ram}</span>
                        </div>
                        <div class="spec-item">
                            <span class="spec-label">Storage</span>
                            <span class="spec-value">${phone.storage}</span>
                        </div>
                        <div class="spec-item">
                            <span class="spec-label">Rear Camera</span>
                            <span class="spec-value">${phone.camera_rear}</span>
                        </div>
                        <div class="spec-item">
                            <span class="spec-label">Front Camera</span>
                            <span class="spec-value">${phone.camera_front}</span>
                        </div>
                        <div class="spec-item">
                            <span class="spec-label">Battery</span>
                            <span class="spec-value">${phone.battery}</span>
                        </div>
                        <div class="spec-item">
                            <span class="spec-label">Charging</span>
                            <span class="spec-value">${phone.charging}</span>
                        </div>
                        <div class="spec-item">
                            <span class="spec-label">OS</span>
                            <span class="spec-value">${phone.os}</span>
                        </div>
                        <div class="spec-item">
                            <span class="spec-label">Weight</span>
                            <span class="spec-value">${phone.weight}</span>
                        </div>
                        <div class="spec-item">
                            <span class="spec-label">OIS</span>
                            <span class="spec-value">${phone.ois}</span>
                        </div>
                        <div class="spec-item">
                            <span class="spec-label">EIS</span>
                            <span class="spec-value">${phone.eis}</span>
                        </div>
                    </div>
                    <div class="product-features">
                        <strong>Features:</strong> ${phone.features}
                    </div>
                </div>
            `;
        });
        
        html += '</div>';
        productsContainer.innerHTML = html;
    }
    
    // Scroll to products
    productsContainer.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// Send message
async function sendMessage() {
    const message = chatInput.value.trim();
    if (!message) return;
    
    // Add user message
    addMessage(message, true);
    chatInput.value = '';
    sendButton.disabled = true;
    
    // Show loading indicator
    const loadingDiv = document.createElement('div');
    loadingDiv.className = 'message bot-message';
    loadingDiv.innerHTML = '<div class="message-content"><div class="loading"></div> <span>Thinking...</span></div>';
    chatMessages.appendChild(loadingDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    
    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message }),
        });
        
        const data = await response.json();
        
        // Remove loading indicator
        chatMessages.removeChild(loadingDiv);
        
        // Add bot response
        addMessage(data.response, false);
        
        // Display products if available
        if (data.phones && data.phones.length > 0) {
            displayProducts(data.phones, data.type);
        } else {
            productsContainer.classList.remove('active');
        }
    } catch (error) {
        chatMessages.removeChild(loadingDiv);
        addMessage('Sorry, I encountered an error. Please try again.', false);
        console.error('Error:', error);
    } finally {
        sendButton.disabled = false;
        chatInput.focus();
    }
}

// Event listeners
sendButton.addEventListener('click', sendMessage);

chatInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        sendMessage();
    }
});

// Focus input on load
chatInput.focus();

