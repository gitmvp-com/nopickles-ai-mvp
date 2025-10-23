# NoPickles.ai MVP

> A simplified conversational AI ordering system for fast food - MVP version of [iota-tec/nopickles](https://github.com/iota-tec/nopickles)

## Overview

This MVP demonstrates the core conversational ordering feature of NoPickles.ai using a web-based chat interface. It focuses on:

- **Natural Language Order Processing**: Take customer orders via text
- **Intent Recognition**: Identify customer intentions (ordering, asking questions, etc.)
- **Entity Extraction**: Extract menu items, sizes, and quantities from conversations
- **Price Calculation**: Automatically calculate order totals
- **Conversational AI**: GPT-based chatbot for natural interactions

## Features

✅ Text-based chat interface
✅ Intent classification (order, question, greeting, etc.)
✅ Named entity recognition for menu items
✅ Dynamic price calculation
✅ Conversational responses using OpenAI GPT
✅ In-memory session management

## Tech Stack

- **Backend**: FastAPI (Python 3.11+)
- **AI/ML**: OpenAI GPT-3.5-turbo, Transformers (BERT for NER)
- **Frontend**: HTML/CSS/JavaScript (vanilla)
- **Deployment**: Docker

## Simplified from Parent Repository

This MVP removes the following from the original project:
- Face recognition & customer identification
- Voice interaction (speech-to-text/text-to-speech)
- Age/gender/ethnicity prediction
- MySQL database (using in-memory storage)
- Complex multi-service architecture
- Authentication system

## Installation

### Prerequisites

- Python 3.11+
- OpenAI API key

### Setup

1. **Clone the repository**

```bash
git clone https://github.com/gitmvp-com/nopickles-ai-mvp.git
cd nopickles-ai-mvp
```

2. **Create virtual environment**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Set up environment variables**

```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
```

5. **Run the application**

```bash
python main.py
```

6. **Open browser**

Navigate to `http://localhost:8000`

## Usage

1. Open the web interface
2. Start chatting with the AI assistant
3. Order items like: "I'd like a large coffee and a donut"
4. The system will:
   - Recognize your intent to order
   - Extract menu items (coffee, donut) and sizes (large)
   - Calculate the total price
   - Respond conversationally

## Example Interactions

```
User: Hi there!
Bot: Hello! Welcome to our fast food kiosk. What can I get for you today?

User: I'd like a large coffee and a chocolate donut
Bot: Great choice! I've got a large coffee and a chocolate donut for you. That'll be $4.00. Anything else?

User: Add a medium cappuccino
Bot: Added a medium cappuccino. Your total is now $7.00. Would you like anything else?

User: That's all, thanks
Bot: Perfect! Your order total is $7.00. Thank you for your order!
```

## Project Structure

```
nopickles-ai-mvp/
├── main.py                 # FastAPI application entry point
├── app/
│   ├── __init__.py
│   ├── api.py             # API routes
│   ├── models.py          # Data models
│   ├── nlp/
│   │   ├── __init__.py
│   │   ├── intent.py      # Intent classification
│   │   ├── entities.py    # Entity extraction
│   │   └── chatbot.py     # GPT integration
│   └── menu.py            # Menu and pricing logic
├── static/
│   ├── index.html         # Web interface
│   ├── style.css
│   └── script.js
├── requirements.txt
├── .env.example
├── Dockerfile
└── README.md
```

## Configuration

The application can be configured via environment variables:

- `OPENAI_API_KEY`: Your OpenAI API key (required)
- `PORT`: Server port (default: 8000)
- `HOST`: Server host (default: 0.0.0.0)

## Docker Deployment

```bash
docker build -t nopickles-mvp .
docker run -p 8000:8000 -e OPENAI_API_KEY=your_key_here nopickles-mvp
```

## API Endpoints

### POST `/chat`

Send a message to the chatbot

**Request:**
```json
{
  "message": "I want a large coffee",
  "session_id": "optional-session-id"
}
```

**Response:**
```json
{
  "response": "Great! I've added a large coffee to your order. That'll be $2.10. Anything else?",
  "intent": "order",
  "entities": [
    {"value": "coffee", "type": "beverage"},
    {"value": "large", "type": "size"}
  ],
  "total_price": 2.10,
  "session_id": "abc123"
}
```

## Future Enhancements

Potential features to add:
- Persistent storage (PostgreSQL/MongoDB)
- User authentication
- Order history
- Voice interface
- Multi-language support
- Payment integration

## License

MIT License

## Credits

Based on [NoPickles.ai](https://github.com/iota-tec/nopickles) by iota-tec
