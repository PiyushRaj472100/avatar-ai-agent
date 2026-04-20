# Avatar AI Agent

An intelligent AI agent that can execute various actions through natural language commands.

## Project Structure

```
avatar-ai-agent/
|
|-- app/                         # Main application
|   |-- main.py                  # FastAPI entry point
|   |
|   |-- core/                    # Config & environment
|   |   `-- config.py
|   |
|   |-- api/                     # API layer
|   |   `-- routes.py
|   |
|   |-- agents/                  # Brain decision layer
|   |   `-- commander.py
|   |
|   |-- brain/                   # LLM interaction
|   |   `-- llm.py
|   |
|   |-- actions/                 # Tools Avatar can execute
|   |   |-- open_apps.py
|   |   |-- search_web.py
|   |   `-- system_control.py
|   |
|   |-- memory/                  # Temporary storage (JSON)
|   |   |-- memory.json
|   |   `-- memory_manager.py
|   |
|   |-- schemas/                 # Data validation
|   |   `-- command_schema.py
|   |
|   `-- utils/                   # Helpers
|       `-- helpers.py
|
|-- tests/                       # (empty for now, future use)
|
|-- .env                         # API keys (DO NOT PUSH)
|-- .gitignore
|-- requirements.txt
|-- Dockerfile                   # Container deployment
`-- README.md
```

## Features

- **Natural Language Processing**: Uses Google Gemini to understand and process commands
- **Multiple Actions**: 
  - Open applications and websites
  - Perform web searches
  - Control system functions
- **Memory Management**: Stores interaction history for context awareness
- **REST API**: FastAPI-based web interface
- **Docker Support**: Containerized deployment

## Getting Started

### Prerequisites

- Python 3.11+
- Google Gemini API key

### Installation

1. Clone the repository:
```bash
git clone https://github.com/PiyushRaj472100/avatar-ai-agent.git
cd avatar-ai-agent
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env and add your Google Gemini API key
```

5. Run the application:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

### API Endpoints

- `GET /` - Root endpoint
- `GET /health` - Health check
- `GET /api/v1/status` - Get agent status
- `POST /api/v1/command` - Execute a command

### Example Usage

```bash
# Check agent status
curl http://localhost:8000/api/v1/status

# Execute a command
curl -X POST "http://localhost:8000/api/v1/command" \
  -H "Content-Type: application/json" \
  -d '{"command": "open chrome"}'
```

## Docker Deployment

```bash
# Build the image
docker build -t avatar-ai-agent .

# Run the container
docker run -p 8000:8000 --env-file .env avatar-ai-agent
```

## Configuration

The application can be configured through environment variables in the `.env` file:

- `GEMINI_API_KEY`: Your Google Gemini API key (required)
- `MODEL_NAME`: Gemini model to use (default: gemini-pro)
- `API_HOST`: API host (default: 0.0.0.0)
- `API_PORT`: API port (default: 8000)

### Getting a Gemini API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Create a new API key
4. Copy the API key to your `.env` file

## Development

The project uses the following tools for development:

- **Black**: Code formatting
- **Flake8**: Linting
- **Pytest**: Testing

Run tests:
```bash
pytest
```

Format code:
```bash
black .
```

## License

This project is licensed under the MIT License.
