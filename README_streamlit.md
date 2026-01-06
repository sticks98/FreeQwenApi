# Streamlit Interface for Qwen API

This repository contains a modern Streamlit interface for interacting with the Qwen API. The interface provides a user-friendly way to send requests to the Qwen API and receive responses.

## Features

- **Modern UI**: Clean and responsive interface built with Streamlit
- **Chat Interface**: Interactive chat interface with message history
- **Context Upload**: Upload text files to provide context for the AI
- **Model Selection**: Choose from available Qwen models
- **API Configuration**: Flexible API URL and authentication settings
- **Session Management**: Maintain chat sessions with chat IDs
- **Math Rendering**: Support for mathematical formulas
- **File Upload**: Upload context files for processing

## Requirements

- Python 3.7+
- Streamlit
- Requests library

## Installation

1. Install the required packages:

```bash
pip install streamlit requests
```

Or install from the requirements file:

```bash
pip install -r requirements.txt
```

## Usage

1. Make sure your Qwen API server is running (typically on `http://localhost:3264/api`)

2. Run the Streamlit application:

```bash
streamlit run streamlit_app.py
```

3. Access the interface at `http://localhost:8501`

## Configuration

- **API Base URL**: Enter the base URL for your Qwen API (default: `http://localhost:3264/api`)
- **API Key**: If your API requires authentication, enter your API key
- **Model Selection**: Choose from the available models or enter a custom model name

## How to Use

1. **Configure API Settings**: Set your API URL and API key in the sidebar
2. **Test Connection**: Click "Test Connection" to verify API connectivity
3. **Upload Context**: Upload a text file or enter context manually
4. **Enter Question**: Type your question in the input field
5. **Submit Request**: Click "Submit Request" to send your query
6. **View Response**: See the AI's response in the chat history panel
7. **Manage Chat**: Use the "Clear Chat" button to start a new conversation

## Additional Tools

- **Create New Chat**: Start a new chat session with a custom name
- **Raw API Request**: View the current API configuration details
- **Chat History**: Maintain conversation context across messages

## API Endpoints Used

- `/status` - Check API authentication status
- `/models` - Get available models
- `/chat/completions` - Send chat completion requests
- `/chats` - Create new chat sessions

## Troubleshooting

- Ensure your Qwen API server is running before using the interface
- Check that the API URL is correct in the configuration
- Verify API key if authentication is required
- Make sure the API supports the models you're trying to use

## Development

The Streamlit interface was created based on the existing HTML interface (`index.html`) and API implementation in the project. It maintains compatibility with the existing API endpoints while providing a modern, user-friendly experience.