# Make Nice - Slack App

A Slack app that transforms your messages into work-appropriate, professional, and well-formatted communications using AI.

## Features

- **Slash Command**: Use `/make-nice` in any channel where the app is installed
- **AI-Powered**: Uses your specified LLM API to transform messages
- **Professional Output**: Automatically formats messages for workplace communication
- **Flexible**: Works with any OpenAI-compatible or custom LLM API

## Installation

### Prerequisites

- Python 3.8 or higher
- A Slack workspace where you have permission to install apps
- An LLM API endpoint (OpenAI, Anthropic, or your own)

### Setup

1. **Clone or download this repository**

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   ```bash
   cp env.example .env
   ```
   
   Edit `.env` and add your configuration:
   - `SLACK_BOT_TOKEN`: Your Slack bot token (xoxb-...)
   - `SLACK_SIGNING_SECRET`: Your Slack app signing secret
   - `SLACK_APP_TOKEN`: Your Slack app token (xapp-...)
   - `LLM_API_ENDPOINT`: Your LLM API endpoint
   - `LLM_API_KEY`: Your LLM API key (if required)
   - `LLM_API_TYPE`: API type (`openai`, `anthropic`, or `custom`)
   - `LLM_MODEL`: Model name to use
   - `LLM_MAX_TOKENS`: Maximum tokens for LLM response (default: 500)

4. **Create a Slack App**
   
   You can either use the manifest file or manually configure the app:
   
   **Option A: Use Manifest (Quick)**
   - Go to https://api.slack.com/apps
   - Click "Create New App" → "From manifest"
   - Select your workspace
   - Copy the contents of `slack-manifest.yaml` into the manifest editor
   - Click "Create"
   - Follow the app creation prompts to get your tokens
   
   **Option B: Manual Setup (Recommended)**
   - See detailed instructions in [SETUP_MANUAL.md](SETUP_MANUAL.md)
   - Step-by-step guide for manually configuring all settings

5. **Get your tokens**
   
   After creating the app:
   - Go to "OAuth & Permissions" → Copy the "Bot User OAuth Token"
   - Go to "Basic Information" → Copy the "Signing Secret"
   - Go to "Socket Mode" → Enable it and generate an "App Token"
   - Update your `.env` file with these values

6. **Install the app to your workspace**
   - Go to "Install App" in your Slack app settings
   - Click "Install to Workspace"
   - Approve the permissions

## Running the App

### Development
```bash
python app.py
```

### Production (using a process manager)
```bash
# Using gunicorn
gunicorn -b 0.0.0.0:8000 app:app

# Or using systemd, supervisor, etc.
```

## Usage

1. Add the app to any channel by mentioning it: `/invite @Make Nice`
2. Use the slash command in that channel: `/make-nice your message here`
3. The app will respond with a professional, work-appropriate version of your message

### Example

**Input:**
```
/make-nice dude this is so messed up can u believe it???
```

**Output:**
```
I'm surprised by this situation. Could you provide more details when you have a chance?
```

## Configuration

### LLM API Endpoints

The app supports multiple LLM providers. Update your configuration:

**OpenAI:**
```env
LLM_API_ENDPOINT=https://api.openai.com/v1/chat/completions
LLM_API_TYPE=openai
LLM_MODEL=gpt-4
LLM_API_KEY=sk-...
```

**Anthropic Claude:**
```env
LLM_API_ENDPOINT=https://api.anthropic.com/v1/messages
LLM_API_TYPE=anthropic
LLM_MODEL=claude-3-opus-20240229
LLM_API_KEY=sk-ant-...
```

**Custom LLM API:**
```env
LLM_API_ENDPOINT=http://your-llm-api.example.com/v1/chat/completions
LLM_API_TYPE=custom
LLM_MODEL=your-model-name
LLM_API_KEY=your-key
```

### Python Version

This app requires Python 3.8 or higher. You can check your version with:
```bash
python --version
```

### Adapting to Different LLM APIs

If your LLM API uses a different request/response format, you can modify `src/llm_handler.py`:
- Update `_build_request_payload()` to match your API's request format
- Update `_extract_response()` to parse your API's response format

The handler supports multiple response formats automatically, but you may need to add your custom format.

## Architecture

- **Backend**: Python 3.8+ with Slack Bolt framework
- **Slack Integration**: Socket Mode for real-time communication
- **LLM Integration**: Flexible API integration via HTTP requests using requests library
- **Error Handling**: Comprehensive error messages for debugging

## Troubleshooting

### "Cannot connect to LLM API"
- Verify your `LLM_API_ENDPOINT` is correct
- Check if your API requires authentication via `LLM_API_KEY`
- Ensure your server can reach the LLM API endpoint

### "LLM API endpoint is not configured"
- Set the `LLM_API_ENDPOINT` in your `.env` file

### "Sorry, I encountered an error processing your message"
- Check the server logs for detailed error messages
- Verify your LLM API key is valid
- Ensure the API endpoint is responding correctly

### Virtual Environment (Recommended)

For a cleaner setup, use a Python virtual environment:

```bash
# Create virtual environment
python -m venv venv

# Activate it (Mac/Linux)
source venv/bin/activate

# Activate it (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Security Notes

- Never commit your `.env` file to version control
- Keep your Slack tokens and API keys secure
- Use environment-specific configurations for production
- Consider using a secrets management system for production deployments

## License

MIT

