import streamlit as st
import os
import sys
import base64
from PIL import Image
import json
from typing import List, Dict, Optional
from datetime import datetime

# Add project root to sys.path for agent_manager import
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)
sys.path.append(PROJECT_ROOT)

# Import AgentManager
try:
    from agents.agent_manager import AgentManager
except ImportError:
    st.error("Could not import AgentManager. Please check your project structure.")
    st.stop()

# Page configuration
st.set_page_config(
    page_title=" Finance Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #1f77b4;
        font-size: 2.5em;
        margin-bottom: 1em;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        flex-direction: column;
    }
    .chat-message.user {
        background-color: #e3f2fd;
        border-left: 4px solid #2196f3;
    }
    .chat-message.assistant {
        background-color: #f5f5f5;
        border-left: 4px solid #4caf50;
    }
    .chat-message.tool {
        background-color: #fff3e0;
        border-left: 4px solid #ff9800;
    }
    .message-header {
        font-weight: bold;
        margin-bottom: 0.5rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .tool-output {
        background-color: #f8f9fa;
        border: 1px solid #dee2e6;
        border-radius: 0.25rem;
        padding: 0.75rem;
        margin: 0.5rem 0;
        font-family: monospace;
        font-size: 0.9em;
    }
    .sidebar-info {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .stButton>button {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

def encode_image_to_base64(image_file) -> str:
    """Convert uploaded image to base64 string."""
    return base64.b64encode(image_file.read()).decode('utf-8')

def get_image_info(uploaded_file) -> Dict:
    """Get image information for processing."""
    if uploaded_file is not None:
        # Get file extension to determine media type
        file_extension = uploaded_file.name.split('.')[-1].lower()
        media_type_map = {
            'jpg': 'image/jpeg',
            'jpeg': 'image/jpeg',
            'png': 'image/png',
            'gif': 'image/gif',
            'webp': 'image/webp'
        }
        media_type = media_type_map.get(file_extension, 'image/jpeg')

        # Reset file pointer and encode
        uploaded_file.seek(0)
        image_data = encode_image_to_base64(uploaded_file)

        return {
            "type": "base64",
            "media_type": media_type,
            "data": image_data
        }
    return None

def display_chat_message(role: str, content: str, timestamp: str = None):
    """Display a chat message with proper formatting."""
    if role == "user":
        icon = "👤"
        css_class = "user"
    elif role == "assistant":
        icon = "🤖"
        css_class = "assistant"
    else:
        icon = "🛠️"
        css_class = "tool"

    st.markdown(f"""
    <div class="chat-message {css_class}">
        <div class="message-header">
            <span>{icon} {role.title()}</span>
            <span style="font-size: 0.8em; color: #666;">{timestamp or datetime.now().strftime('%H:%M:%S')}</span>
        </div>
        <div>{content}</div>
    </div>
    """, unsafe_allow_html=True)

def display_tool_outputs(tool_outputs: List[Dict]):
    """Display tool outputs in a formatted way."""
    if not tool_outputs:
        return

    st.markdown("### 🛠️ Tool Outputs")

    for i, tool_output in enumerate(tool_outputs, 1):
        tool_name = tool_output.get('tool_name', 'Unknown Tool')
        tool_data = tool_output.get('data', {})

        with st.expander(f"🔧 {tool_name} - Result {i}", expanded=False):
            if 'error' in tool_output:
                st.error(f"Error: {tool_output['error']}")
            elif isinstance(tool_data, dict):
                # Pretty print the tool data
                st.json(tool_data)
            else:
                st.code(str(tool_data), language='json')

def main():
    # Main header
    st.markdown('<h1 class="main-header">🤖 Finance Agent</h1>', unsafe_allow_html=True)
    st.markdown("---")

    # Sidebar
    with st.sidebar:
        st.markdown('<div class="sidebar-info">', unsafe_allow_html=True)
        st.markdown("### 🎯 Agent Selection")
        agent_type = st.selectbox(
            "Choose Agent Type:",
            ["financial_assistant", "utility_assistant"],
            help="Financial Assistant: Stock analysis, news, crypto\nUtility Assistant: Weather, search, conversions"
        )

        st.markdown("### 📊 Agent Info")
        if agent_type == "financial_assistant":
            st.info("💰 **Financial Assistant**\n- Stock market data\n- Financial news\n- Crypto analysis\n- Trend analysis")
        else:
            st.info("🛠️ **Utility Assistant**\n- Weather updates\n- Wikipedia search\n- Unit conversions\n- Calendar reminders")

        st.markdown("### 📁 File Upload")
        uploaded_file = st.file_uploader(
            "Upload an image (optional)",
            type=['png', 'jpg', 'jpeg', 'gif', 'webp'],
            help="Upload an image to include in your query"
        )

        if uploaded_file:
            st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)

        st.markdown('</div>', unsafe_allow_html=True)

    # Initialize session state for chat history
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'agent_manager' not in st.session_state:
        st.session_state.agent_manager = None
    if 'current_agent_type' not in st.session_state:
        st.session_state.current_agent_type = None

    # Initialize or reinitialize agent manager if agent type changed
    if st.session_state.current_agent_type != agent_type:
        try:
            with st.spinner("Initializing agent..."):
                st.session_state.agent_manager = AgentManager(agent_type=agent_type)
                st.session_state.current_agent_type = agent_type
            st.success(f"✅ {agent_type.replace('_', ' ').title()} initialized successfully!")
        except Exception as e:
            st.error(f"❌ Failed to initialize agent: {str(e)}")
            return

    # Chat interface
    st.markdown("### 💬 Chat Interface")

    # Display chat history
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.chat_history:
            display_chat_message(
                message['role'],
                message['content'],
                message.get('timestamp')
            )

    # Input area
    with st.form(key="chat_form", clear_on_submit=True):
        user_input = st.text_area(
            "Enter your message:",
            height=100,
            placeholder="Ask me about stocks, weather, news, or any other query...",
            help="Type your question or request here"
        )

        col1, col2 = st.columns([4, 1])
        with col1:
            submit_button = st.form_submit_button("➣ Send Message", use_container_width=True)
        with col2:
            clear_button = st.form_submit_button("🗑️ Clear Chat", use_container_width=True)

    # Handle clear chat
    if clear_button:
        st.session_state.chat_history = []
        st.rerun()

    # Handle message submission
    if submit_button and user_input.strip():
        # Add user message to history
        timestamp = datetime.now().strftime('%H:%M:%S')
        user_message = {
            'role': 'user',
            'content': user_input,
            'timestamp': timestamp
        }
        st.session_state.chat_history.append(user_message)

        # Display user message
        with chat_container:
            display_chat_message('user', user_input, timestamp)

        # Process the query
        with st.spinner("🤔 Thinking..."):
            try:
                # Prepare image data if uploaded
                image_data = None
                if uploaded_file:
                    image_data = get_image_info(uploaded_file)

                # Prepare history for agent (exclude tool messages)
                history_for_agent = [
                    {"role": msg['role'], "content": msg['content']}
                    for msg in st.session_state.chat_history[:-1]  # Exclude current user message
                    if msg['role'] in ['user', 'assistant']
                ]

                # Process query
                result = st.session_state.agent_manager.process_query(
                    query=user_input,
                    history=history_for_agent,
                    image=image_data
                )

                # Extract response
                response_text = result.get("text_response", "No response generated.")
                tool_outputs = result.get("tool_outputs", [])

                # Add assistant response to history
                assistant_message = {
                    'role': 'assistant',
                    'content': response_text,
                    'timestamp': datetime.now().strftime('%H:%M:%S')
                }
                st.session_state.chat_history.append(assistant_message)

                # Display assistant response
                with chat_container:
                    display_chat_message('assistant', response_text, assistant_message['timestamp'])

                # Display tool outputs if any
                if tool_outputs:
                    display_tool_outputs(tool_outputs)

                # Clear uploaded file after processing
                if uploaded_file:
                    st.sidebar.success("✅ Image processed successfully!")

            except Exception as e:
                error_message = f"❌ Error processing request: {str(e)}"
                st.error(error_message)

                # Add error to chat history
                error_msg = {
                    'role': 'assistant',
                    'content': error_message,
                    'timestamp': datetime.now().strftime('%H:%M:%S')
                }
                st.session_state.chat_history.append(error_msg)

                with chat_container:
                    display_chat_message('assistant', error_message, error_msg['timestamp'])

    # Footer
    st.markdown("---")
    st.markdown("### 📋 Usage Tips")
    with st.expander("💡 How to use this Finance Agent"):
        st.markdown("""
        **Financial Assistant Examples:**
        - "What's the current price of Apple stock?"
        - "Show me Tesla's stock performance over the last 30 days"
        - "What's the latest news about Bitcoin?"
        - "Analyze the trend for Microsoft stock"

        **Utility Assistant Examples:**
        - "What's the weather like in New York?"
        - "Convert 100 USD to EUR"
        - "Search Wikipedia for quantum computing"
        - "Set a reminder for tomorrow at 3 PM"

        **Image Support:**
        - Upload images along with your queries for multi-modal analysis
        - Great for analyzing charts, documents, or visual data
        """)

if __name__ == "__main__":
    main()
