# Avatar AI Agent - Setup & Running Guide

## Prerequisites
- Python 3.11+
- Google Gemini API Key

## Step-by-Step Setup

### 1. Clone the Repository
```bash
git clone https://github.com/PiyushRaj472100/avatar-ai-agent.git
cd avatar-ai-agent
```

### 2. Create Virtual Environment
```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate

# On macOS/Linux:
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables
```bash
# Copy environment template
copy .env.example .env

# Edit .env file and add your Gemini API key
# Replace AIzaSyDQKJp3wFnafc4s58GT6JKBWCrK_vuO3Xo with your actual API key
```

### 5. Get Your Gemini API Key
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Create a new API key
4. Copy the API key to your `.env` file

### 6. Run the Application
```bash
# Method 1: Direct run
uvicorn app.main:app --reload

# Method 2: Using Python
python -m uvicorn app.main:app --reload

# Method 3: Using the app module
python -m app.main
```

### 7. Access the API
- **API Base URL**: http://localhost:8000
- **Health Check**: http://localhost:8000/health
- **API Documentation**: http://localhost:8000/docs
- **Agent Status**: http://localhost:8000/api/v1/status

## API Endpoints

### Simple Commands (Auto-detects Agent Mode)
```bash
curl -X POST "http://localhost:8000/api/v1/command" \
  -H "Content-Type: application/json" \
  -d '{"command": "Find the best Python course"}'
```

### Force Agent Mode (Multi-step planning)
```bash
curl -X POST "http://localhost:8000/api/v1/agent" \
  -H "Content-Type: application/json" \
  -d '{"command": "Research and compare 3 Python courses"}'
```

### Force Simple Mode (Single action)
```bash
curl -X POST "http://localhost:8000/api/v1/simple" \
  -H "Content-Type: application/json" \
  -d '{"command": "open chrome"}'
```

## Example Commands to Test

### Intelligent Agent Mode (Thought-First)
```bash
# These will use search_summary (intelligent analysis)
curl -X POST "http://localhost:8000/api/v1/command" \
  -H "Content-Type: application/json" \
  -d '{"command": "Find the best Python course and compare it"}'

curl -X POST "http://localhost:8000/api/v1/command" \
  -H "Content-Type: application/json" \
  -d '{"command": "Research top 5 AI tools"}'
```

### Simple Actions
```bash
# These will use simple actions
curl -X POST "http://localhost:8000/api/v1/command" \
  -H "Content-Type: application/json" \
  -d '{"command": "open google.com"}'

curl -X POST "http://localhost:8000/api/v1/command" \
  -H "Content-Type: application/json" \
  -d '{"command": "search for python tutorials"}'
```

## Virtual Environment Commands

### Create .venv
```bash
python -m venv .venv
```

### Activate .venv
```bash
# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate
```

### Deactivate .venv
```bash
deactivate
```

### Delete .venv (if needed)
```bash
# Windows
rmdir /s .venv

# macOS/Linux
rm -rf .venv
```

## Troubleshooting

### Common Issues

1. **ModuleNotFoundError**: Make sure virtual environment is activated
2. **API Key Error**: Check your .env file has correct Gemini API key
3. **Port Already in Use**: Change port with `--port 8001`
4. **Dependencies Issues**: Try `pip install --upgrade -r requirements.txt`

### Debug Mode
```bash
# Run with debug logging
uvicorn app.main:app --reload --log-level debug

# Run on different port
uvicorn app.main:app --reload --port 8001
```

## Development Commands

### Code Formatting
```bash
# Format code
black .

# Check code style
flake8 .
```

### Testing
```bash
# Run tests (when available)
pytest

# Run specific test file
pytest tests/test_agent.py
```

## Docker Setup (Optional)

### Build and Run
```bash
# Build Docker image
docker build -t avatar-ai-agent .

# Run container
docker run -p 8000:8000 --env-file .env avatar-ai-agent
```

## Project Structure
```
avatar-ai-agent/
|
|-- app/                    # Main application
|   |-- main.py            # FastAPI entry point
|   |-- agents/            # AI agents
|   |-- brain/             # LLM integration
|   |-- actions/           # Available tools
|   |-- api/               # API routes
|   |-- core/              # Configuration
|   |-- memory/            # Memory management
|   |-- schemas/           # Data validation
|   `-- utils/             # Helper functions
|
|-- .venv/                 # Virtual environment
|-- .env                   # Environment variables (API keys)
|-- .env.example           # Environment template
|-- requirements.txt       # Python dependencies
|-- Dockerfile            # Container setup
`-- SETUP.md              # This file
```

## Next Steps

1. **Test Simple Commands**: Try basic actions first
2. **Test Agent Mode**: Try complex multi-step tasks
3. **Explore API Docs**: Visit http://localhost:8000/docs
4. **Customize**: Add your own actions and tools
5. **Deploy**: Use Docker for production deployment

## Support

If you encounter issues:
1. Check the terminal logs for error messages
2. Verify your Gemini API key is valid
3. Ensure all dependencies are installed
4. Make sure the virtual environment is activated

Happy coding with Avatar AI Agent!
