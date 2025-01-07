import streamlit as st
from openai import OpenAI
from datetime import datetime
from typing import Dict, List
import uuid
import pandas as pd

# Page configuration
st.set_page_config(layout="wide", page_title="Research Chat")

# Previous styling remains the same, adding new styles for panels
st.markdown("""
<style>

    /* Base styles */
    .stApp {
        background-color: #1e1e1e;
        color: #ffffff;
    }
    
    /* Topic panel styling */
    .topic-panel {
        background-color: #2d2d2d;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    
    .topic-list-container {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
        margin-top: 1rem;
    }
    
    .topic-button {
        background-color: #363636;
        color: #ffffff;
        border: 1px solid #404040;
        border-radius: 0.5rem;
        padding: 0.5rem 1rem;
        cursor: pointer;
        transition: all 0.2s;
    }
    
    .topic-button:hover {
        background-color: #404040;
        border-color: #505050;
    }
    
    .topic-button.selected {
        background-color: #0f62fe;
        border-color: #0f62fe;
    }
    
    /* New topic input group */
    .new-topic-group {
        display: flex;
        gap: 0.5rem;
        align-items: center;
        margin-bottom: 1rem;
        background-color: #363636;
        padding: 0.5rem;
        border-radius: 0.5rem;
    }
    
    .new-topic-input {
        flex-grow: 1;
        background-color: #2d2d2d;
        border: 1px solid #404040;
        color: #ffffff;
        padding: 0.5rem;
        border-radius: 0.25rem;
    }
    
    /* Chat container */
    .chat-container {
        background-color: #2d2d2d;
        border-radius: 0.5rem;
        padding: 1rem;
        height: calc(100vh - 200px);
        overflow-y: auto;
    }
    
    /* Messages */
    .stChatMessage {
        background-color: transparent;
        margin: 1rem 0;
    }
    
    .stChatMessage [data-testid="stChatMessageContent"] {
        background-color: #363636 !important;
        color: #ffffff !important;
        border-radius: 0.5rem;
        padding: 1rem !important;
    }
    
    /* Chat input */
    .stChatInputContainer {
        margin-top: 1rem;
    }
    
    .stChatInputContainer textarea {
        background-color: #363636;
        color: #ffffff;
        border: 1px solid #404040;
    }
    /* Previous styles remain... */
    
    /* Analytics Panel Styling */
    .analytics-panel {
        background-color: #2d2d2d;
        border-radius: 0.5rem;
        padding: 1rem;
        margin-bottom: 1rem;
    }
    
    .metric-card {
        background-color: #363636;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    
    .metric-value {
        font-size: 1.5rem;
        font-weight: bold;
        color: #0f62fe;
    }
    
    /* Summary Panel Styling */
    .summary-panel {
        background-color: #2d2d2d;
        border-radius: 0.5rem;
        padding: 1rem;
        margin-bottom: 1rem;
    }
    
    .conversation-item {
        padding: 0.5rem;
        margin: 0.25rem 0;
        border-radius: 0.25rem;
    }
    
    .human-message {
        background-color: #363636;
        border-left: 3px solid #0f62fe;
    }
    
    .ai-message {
        background-color: #363636;
        border-left: 3px solid #00c853;
    }
</style>
""", unsafe_allow_html=True)

class ResearchAnalytics:
    def __init__(self, topic_data: Dict):
        self.topic_data = topic_data
        self.messages = topic_data.get("messages", [])
    
    def calculate_metrics(self) -> Dict:
        """Calculate research metrics"""
        total_messages = len(self.messages)
        human_messages = len([m for m in self.messages if m["role"] == "user"])
        ai_messages = len([m for m in self.messages if m["role"] == "assistant"])
        
        # Dummy metrics for demonstration
        return {
            "Research Quality Score": "85%",
            "Source Reliability": "92%",
            "Fact Check Score": "88%",
            "Verification Index": "90%",
            "Citations Found": "12",
            "Research Depth": "High",
            "Total Exchanges": f"{human_messages}",
            "Average Response Length": "450 words"
        }
    
    def generate_summary(self) -> List[Dict]:
        """Generate conversation summary"""
        summary = []
        for msg in self.messages:
            summary.append({
                "role": msg["role"],
                "content": msg["content"][:200] + "..." if len(msg["content"]) > 200 else msg["content"],
                "timestamp": msg["timestamp"]
            })
        return summary

class TopicManager:
    def __init__(self):
        if "topics" not in st.session_state:
            st.session_state.topics = {}
        if "current_topic" not in st.session_state:
            st.session_state.current_topic = None
    
    def create_topic(self, name: str) -> str:
        topic_id = str(uuid.uuid4())
        st.session_state.topics[topic_id] = {
            "name": name,
            "messages": [],
            "created_at": datetime.now().isoformat()
        }
        return topic_id
    
    def select_topic(self, topic_id: str):
        st.session_state.current_topic = topic_id
        
class ResearchChat:
    def __init__(self, openai_api_key: str):
        self.client = OpenAI(api_key=openai_api_key)
        self.topic_manager = TopicManager()
    
    def create_topic_panel(self):
        """Create the topic management panel"""
        st.markdown('<div class="topic-panel">', unsafe_allow_html=True)
        
        # New topic input and button in a single row
        col1, col2 = st.columns([3, 1])
        with col1:
            new_topic_name = st.text_input(
                "New topic",
                key="new_topic_input",
                label_visibility="collapsed",
                placeholder="Enter new topic name"
            )
        with col2:
            if st.button("New Research Topic", use_container_width=True):
                if new_topic_name:
                    topic_id = self.topic_manager.create_topic(new_topic_name)
                    self.topic_manager.select_topic(topic_id)
                    st.rerun()
        
        # Topic list as horizontal buttons
        if st.session_state.topics:
            st.markdown("### Research Topics")
            cols = st.columns(4)  # Adjust number based on screen size
            for idx, (topic_id, topic_data) in enumerate(st.session_state.topics.items()):
                col_idx = idx % 4
                with cols[col_idx]:
                    if st.button(
                        topic_data["name"],
                        key=f"topic_{topic_id}",
                        use_container_width=True,
                        type="secondary" if topic_id != st.session_state.current_topic else "primary"
                    ):
                        self.topic_manager.select_topic(topic_id)
                        st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    # Previous initialization remains the same...
    
    def create_analytics_panel(self, topic_data: Dict):
        """Create the research analytics panel"""
        analytics = ResearchAnalytics(topic_data)
        metrics = analytics.calculate_metrics()
        
        with st.expander("📊 Research Analytics", expanded=True):
            st.markdown("### Research Quality Metrics")
            
            # Display metrics in a grid
            cols = st.columns(4)
            for idx, (metric, value) in enumerate(metrics.items()):
                with cols[idx % 4]:
                    st.markdown(f"""
                        <div class="metric-card">
                            <div>{metric}</div>
                            <div class="metric-value">{value}</div>
                        </div>
                    """, unsafe_allow_html=True)
            
            # Research progress visualization
            st.markdown("### Research Progress")
            progress_data = pd.DataFrame({
                'Metric': ['Completeness', 'Depth', 'Accuracy'],
                'Value': [75, 85, 90]
            })
            st.progress(0.85)  # Overall progress
            st.bar_chart(progress_data.set_index('Metric'))
    
    def create_summary_panel(self, topic_data: Dict):
        """Create the conversation summary panel"""
        analytics = ResearchAnalytics(topic_data)
        summary = analytics.generate_summary()
        
        with st.expander("📝 Conversation Summary", expanded=True):
            st.markdown("### Key Exchanges")
            
            for msg in summary:
                role_icon = "👤" if msg["role"] == "user" else "🤖"
                role_class = "human-message" if msg["role"] == "user" else "ai-message"
                
                st.markdown(f"""
                    <div class="conversation-item {role_class}">
                        <strong>{role_icon} {msg["role"].title()}</strong><br>
                        {msg["content"]}
                    </div>
                """, unsafe_allow_html=True)
    
    def create_chat_interface(self):
        """Create the main chat interface"""
        if not st.session_state.current_topic:
            st.info("👆 Select or create a new research topic to start chatting.")
            return
        
        current_topic = st.session_state.topics[st.session_state.current_topic]
        
        # Show analytics and summary panels
        self.create_analytics_panel(current_topic)
        self.create_summary_panel(current_topic)
        
        # Chat container
        st.markdown("### Research Chat")
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        
        # Rest of the chat interface remains the same...
    # Display messages
        for message in current_topic["messages"]:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Chat input
        if prompt := st.chat_input("Research your topic..."):
            # Add user message
            current_topic["messages"].append({
                "role": "user",
                "content": prompt,
                "timestamp": datetime.now().isoformat()
            })
            
            try:
                # Stream the response
                with st.chat_message("assistant"):
                    stream = self.client.chat.completions.create(
                        model="gpt-4-turbo-preview",
                        messages=[
                            {"role": m["role"], "content": m["content"]}
                            for m in current_topic["messages"]
                        ],
                        stream=True,
                    )
                    response = st.write_stream(stream)
                
                # Store assistant response
                current_topic["messages"].append({
                    "role": "assistant",
                    "content": response,
                    "timestamp": datetime.now().isoformat()
                })
                
            except Exception as e:
                st.error(f"Error: {str(e)}")
        
        st.markdown('</div>', unsafe_allow_html=True)

    def run(self):
        """Run the main application"""
        # Create the topic panel
        self.create_topic_panel()
        
        # Create the enhanced chat interface
        self.create_chat_interface()

def main():
    # Get API key
    with st.sidebar:
        openai_api_key = st.text_input("OpenAI API Key", type="password")
    
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.", icon="🔑")
        return
    
    # Initialize and run the chat application
    app = ResearchChat(openai_api_key)
    app.run()

if __name__ == "__main__":
    main()