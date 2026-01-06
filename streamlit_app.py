import streamlit as st
import requests
import json
import re
from typing import Optional, Dict, Any
import time

# Set page config
st.set_page_config(
    page_title="API Interface for Qwen",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for enhanced styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 2rem;
        color: #1f77b4;
    }
    
    .section-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #444;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
        border-bottom: 2px solid #1f77b4;
        padding-bottom: 0.5rem;
    }
    
    .api-response {
        background-color: #f8f9fa;
        border: 1px solid #e9ecef;
        border-radius: 8px;
        padding: 1rem;
        margin-top: 1rem;
        font-family: 'Courier New', monospace;
        white-space: pre-wrap;
        overflow-x: auto;
    }
    
    .stMarkdown {
        font-size: 1.1rem;
        line-height: 1.6;
    }
    
    .model-selector {
        margin-bottom: 1rem;
    }
    
    .context-section {
        background-color: #f0f8ff;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #1f77b4;
    }
    
    .question-section {
        background-color: #fff8f0;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #ff7f0e;
    }
    
    .response-section {
        background-color: #f0fff0;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #2ca02c;
    }
    
    .status-section {
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .status-ok {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
    }
    
    .status-error {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
    }
    
    .status-warning {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        color: #856404;
    }
    
    .math-equation {
        font-family: 'Cambria Math', serif;
        font-size: 1.1rem;
    }
    
    .stTextArea textarea {
        font-family: 'Courier New', monospace;
    }
    
    .stTextInput input {
        font-family: 'Courier New', monospace;
    }
    
    .chat-message {
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
    }
    
    .chat-message-user {
        background-color: #e3f2fd;
        border-left: 4px solid #2196f3;
    }
    
    .chat-message-assistant {
        background-color: #f3e5f5;
        border-left: 4px solid #9c27b0;
    }
    
    .model-info {
        font-size: 0.9rem;
        color: #6c757d;
        font-style: italic;
    }
</style>
""", unsafe_allow_html=True)

def get_api_status(api_url: str, headers: Dict[str, str]) -> Optional[Dict[str, Any]]:
    """Get the status of the API"""
    try:
        response = requests.get(f"{api_url}/status", headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"HTTP {response.status_code}: {response.text}"}
    except Exception as e:
        return {"error": str(e)}

def get_available_models(api_url: str, headers: Dict[str, str]) -> Optional[Dict[str, Any]]:
    """Get available models from the API"""
    try:
        response = requests.get(f"{api_url}/models", headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"HTTP {response.status_code}: {response.text}"}
    except Exception as e:
        return {"error": str(e)}

def send_chat_request(api_url: str, headers: Dict[str, str], payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Send a chat request to the API"""
    try:
        response = requests.post(f"{api_url}/chat/completions", headers=headers, json=payload)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"HTTP {response.status_code}: {response.text}"}
    except Exception as e:
        return {"error": str(e)}

def create_new_chat(api_url: str, headers: Dict[str, str], model: str, name: str = "New Chat") -> Optional[Dict[str, Any]]:
    """Create a new chat session"""
    try:
        payload = {"model": model, "name": name}
        response = requests.post(f"{api_url}/chats", headers=headers, json=payload)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"HTTP {response.status_code}: {response.text}"}
    except Exception as e:
        return {"error": str(e)}

def format_markdown_with_math(text: str) -> str:
    """Format markdown text with proper math rendering for Streamlit"""
    # First, temporarily encode the display math regions to avoid processing inside them
    display_math_pattern = r'\\\[(.*?)\\\]'
    display_placeholders = []
    
    def replace_display_math(match):
        content = match.group(1)
        placeholder = f"__DISPLAY_MATH_PLACEHOLDER_{len(display_placeholders)}__"
        display_placeholders.append(content)
        return placeholder
    
    text = re.sub(display_math_pattern, replace_display_math, text)
    
    # Then, temporarily encode the inline math regions to avoid processing inside them
    inline_math_pattern = r'\\\((.*?)\\\)'
    inline_placeholders = []
    
    def replace_inline_math(match):
        content = match.group(1)
        placeholder = f"__INLINE_MATH_PLACEHOLDER_{len(inline_placeholders)}__"
        inline_placeholders.append(content)
        return placeholder
    
    text = re.sub(inline_math_pattern, replace_inline_math, text)
    
    # Now handle the specific formula elements from the user's example
    # These are outside math regions so they won't be double-processed
    text = re.sub(r'K_\{газX\}', r'$K_{газX}$', text)
    text = re.sub(r'C_\{X-1\}', r'$C_{X-1}$', text)
    text = re.sub(r'C_\{X-4\}', r'$C_{X-4}$', text)
    text = re.sub(r'R_\{газj\}', r'$R_{газj}$', text)
    text = re.sub(r'\\sum_\{j=X-3\}\^\{X-1\}', r'$\\sum_{j=X-3}^{X-1}$', text)
    
    # Now restore the display math regions with proper $$...$$ formatting
    for i, content in enumerate(display_placeholders):
        placeholder = f"__DISPLAY_MATH_PLACEHOLDER_{i}__"
        text = text.replace(placeholder, f"$${content}$$")
    
    # And restore the inline math regions with proper $...$ formatting
    for i, content in enumerate(inline_placeholders):
        placeholder = f"__INLINE_MATH_PLACEHOLDER_{i}__"
        text = text.replace(placeholder, f"${content}$")
    
    return text

def main():
    st.markdown('<h1 class="main-header">🤖 API Interface for Qwen</h1>', unsafe_allow_html=True)
    
    # Initialize session state
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'current_chat_id' not in st.session_state:
        st.session_state.current_chat_id = None
    if 'current_parent_id' not in st.session_state:
        st.session_state.current_parent_id = None
    if 'api_url' not in st.session_state:
        st.session_state.api_url = "http://localhost:3264/api"
    if 'api_key' not in st.session_state:
        st.session_state.api_key = ""
    if 'selected_model' not in st.session_state:
        st.session_state.selected_model = "qwen-max"
    if 'available_models' not in st.session_state:
        st.session_state.available_models = []
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        st.session_state.api_url = st.text_input(
            "API Base URL",
            value=st.session_state.api_url,
            help="Enter the base URL for the API (e.g., http://localhost:3264/api)"
        )
        
        st.session_state.api_key = st.text_input(
            "API Key (optional)",
            value=st.session_state.api_key,
            type="password",
            help="Enter API key if required for authentication"
        )
        
        # Test API connection
        headers = {"Content-Type": "application/json"}
        if st.session_state.api_key:
            headers["Authorization"] = f"Bearer {st.session_state.api_key}"
        
        if st.button("🔄 Test Connection"):
            with st.spinner("Testing API connection..."):
                status = get_api_status(st.session_state.api_url, headers)
                if status and "error" not in status:
                    st.success("✅ Connection successful!")
                    if "authenticated" in status:
                        auth_status = "✅ Authenticated" if status["authenticated"] else "⚠️ Authentication required"
                        st.info(f"Authorization: {auth_status}")
                    
                    # Get available models
                    models = get_available_models(st.session_state.api_url, headers)
                    if models and "error" not in models and "data" in models:
                        st.session_state.available_models = [model["id"] for model in models["data"]]
                        st.success(f"Available models: {len(st.session_state.available_models)}")
                    else:
                        st.warning("Could not fetch models")
                else:
                    st.error(f"❌ Connection failed: {status.get('error', 'Unknown error')}")
        
        # Model selection
        if st.session_state.available_models:
            st.session_state.selected_model = st.selectbox(
                "Select Model",
                options=st.session_state.available_models,
                index=next((i for i, m in enumerate(st.session_state.available_models) 
                           if st.session_state.selected_model in m), 0),
                help="Choose the model to use for API requests"
            )
        else:
            st.session_state.selected_model = st.text_input(
                "Model Name",
                value=st.session_state.selected_model,
                help="Enter the model name to use (e.g., qwen-max, qwen-plus)"
            )
    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown('<h2 class="section-header">📝 Input</h2>', unsafe_allow_html=True)
        
        # File upload for context
        uploaded_file = st.file_uploader(
            "Upload context file (TXT)",
            type=["txt"],
            help="Upload a text file to use as context for the AI"
        )
        
        context = ""
        if uploaded_file is not None:
            context = uploaded_file.read().decode("utf-8")
        
        context = st.text_area(
            "Context (optional)",
            value=context,
            height=200,
            help="Provide context for the AI to use in answering your question",
            placeholder="Enter context here or upload a file..."
        )
        
        question = st.text_input(
            "Question",
            help="Enter your question for the AI",
            placeholder="What would you like to ask?"
        )
        
        # Submit button
        submit_button = st.button("🚀 Submit Request", type="primary")
    
    with col2:
        st.markdown('<h2 class="section-header">💬 Chat History</h2>', unsafe_allow_html=True)
        
        # Clear chat button
        if st.button("🗑️ Clear Chat"):
            st.session_state.chat_history = []
            st.session_state.current_chat_id = None
            st.session_state.current_parent_id = None
        
        # Display chat history
        for i, message in enumerate(st.session_state.chat_history):
            role = message["role"]
            content = message["content"]
            
            if role == "user":
                st.markdown(
                    f'<div class="chat-message chat-message-user">'
                    f'<strong>You:</strong> {content}'
                    f'</div>',
                    unsafe_allow_html=True
                )
            elif role == "assistant":
                st.markdown(
                    f'<div class="chat-message chat-message-assistant">'
                    f'<strong>AI:</strong> {format_markdown_with_math(content)}'
                    f'</div>',
                    unsafe_allow_html=True
                )
    
    # Handle API request
    if submit_button:
        if not question:
            st.warning("Please enter a question")
        else:
            with st.spinner("Processing your request..."):
                # Prepare the messages array
                messages = []
                
                # Add system message if context is provided
                if context.strip():
                    messages.append({
                        "role": "system",
                        "content": f"Контекст: {context}; Задача: Используя только контекст ответь на вопрос. Если в контексте нет информации по вопросу, тогда ответь 'Я не знаю'"
                    })
                
                # Add previous messages if in a chat session
                for msg in st.session_state.chat_history:
                    messages.append({
                        "role": msg["role"],
                        "content": msg["content"]
                    })
                
                # Add the current question
                messages.append({
                    "role": "user",
                    "content": question
                })
                
                # Prepare the payload
                payload = {
                    "messages": messages,
                    "model": st.session_state.selected_model,
                }
                
                # Add chat ID and parent ID if available
                if st.session_state.current_chat_id:
                    payload["chatId"] = st.session_state.current_chat_id
                if st.session_state.current_parent_id:
                    payload["parentId"] = st.session_state.current_parent_id
                
                # Send the request
                response = send_chat_request(st.session_state.api_url, headers, payload)
                
                if response and "error" not in response:
                    # Extract the response content
                    content = response["choices"][0]["message"]["content"]
                    
                    # Store chat IDs if provided
                    if "chatId" in response:
                        st.session_state.current_chat_id = response["chatId"]
                    if "parentId" in response:
                        st.session_state.current_parent_id = response["parentId"]
                    
                    # Update chat history
                    st.session_state.chat_history.append({
                        "role": "user",
                        "content": question
                    })
                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": content
                    })
                    
                    # Show success message
                    st.success("✅ Request completed successfully!")
                    
                    # Rerun to update the UI
                    st.rerun()
                else:
                    st.error(f"❌ Error: {response.get('error', 'Unknown error')}")
    
    # Show current session info
    if st.session_state.current_chat_id:
        st.info(f"🔄 Current Chat ID: {st.session_state.current_chat_id}")
    
    # Additional API tools section
    st.markdown('<h2 class="section-header">🔧 Additional Tools</h2>', unsafe_allow_html=True)
    
    with st.expander("Create New Chat Session"):
        new_chat_name = st.text_input("Chat Name", value="New Chat", help="Name for the new chat session")
        if st.button("Create New Chat"):
            with st.spinner("Creating new chat..."):
                result = create_new_chat(
                    st.session_state.api_url, 
                    headers, 
                    st.session_state.selected_model, 
                    new_chat_name
                )
                
                if result and "error" not in result:
                    st.session_state.current_chat_id = result["chatId"]
                    st.session_state.current_parent_id = None
                    st.session_state.chat_history = []
                    st.success(f"✅ New chat created with ID: {result['chatId']}")
                    st.rerun()
                else:
                    st.error(f"❌ Error creating chat: {result.get('error', 'Unknown error')}")
    
    with st.expander("Raw API Request"):
        st.markdown("**Current API Configuration:**")
        st.code(f"""
API URL: {st.session_state.api_url}
Headers: {json.dumps(headers, indent=2)}
Selected Model: {st.session_state.selected_model}
Current Chat ID: {st.session_state.current_chat_id or 'None'}
Current Parent ID: {st.session_state.current_parent_id or 'None'}
        """)
    
    # Footer
    st.markdown("---")
    st.markdown(
        '<div class="model-info" style="text-align: center; padding: 1rem;">'
        'Powered by Qwen API Interface • Streamlit Application'
        '</div>',
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()