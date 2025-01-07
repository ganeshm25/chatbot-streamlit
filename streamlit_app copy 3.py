import streamlit as st
from openai import OpenAI
from datetime import datetime
from typing import Dict, List
import uuid
import pandas as pd

# Page configuration
st.set_page_config(layout="wide", page_title="Research Assistant")

# Custom styling
st.markdown("""
<style>
    .stApp {
        background-color: #1e1e1e;
    }

    [data-testid="stSidebar"] {
        background-color: #2d2d2d;
        border-right: 1px solid #404040 !important;
    }
    .topic-sidebar {
        padding: 1rem;
        color: #ffffff;
    }
    .topic-list {
        padding: 1rem;
        color: #ffffff;
    }

    .stButton button {
        width: 100%;
        padding: 0.75rem 1rem;
        margin: 0.5rem 0;
        background-color: #363636 !important;
        color: #ffffff !important;
        border: 1px solid #404040 !important;
        border-radius: 0.375rem;
        text-align: left;
    }

    .stButton button:hover {
        background-color: #404040 !important;
        border-color: #505050 !important;
    }
    .stButton button:selected {
        background-color: #0f62fe;
        border-color: #0f62fe;
    }
    .stButton button[data-testid="baseButton-primary"] {
        background-color: #0f62fe !important;
        border-color: #0f62fe !important;
    }

    /* Main Content */
    .main-content {
        color: #ffffff;
        padding: 2rem;
    }
    
    /* Headers */
    h1, h2, h3, h4, h5, h6 {
        color: #ffffff !important;
        font-weight: 600;
    }

    [data-testid="stMarkdownContainer"] {
        color: #ffffff !important;
    }

    /* Input Fields */
    .stTextInput input, .stTextArea textarea {
        background-color: #363636 !important;
        color: #ffffff !important;
        border: 1px solid #404040 !important;
        border-radius: 0.375rem;
    }
    
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #0f62fe !important;
        box-shadow: 0 0 0 1px #0f62fe !important;
    }

    /* Metrics */
    [data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-size: 2rem !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: #a0a0a0 !important;
    }

    /* Chat Messages */
    .stChatMessage {
        background-color: transparent;
        margin: 1rem 0;
    }
    
    .stChatMessage [data-testid="stMarkdownContainer"] {
        color: #ffffff !important;
    }
    
    .stChatMessage [data-testid="stChatMessageContent"] {
        background-color: #363636 !important;
        border: 1px solid #404040;
        border-radius: 0.5rem;
        padding: 1rem;
    }

    /* Expander */
    .streamlit-expanderHeader {
        background-color: #363636 !important;
        color: #ffffff !important;
        border: 1px solid #404040;
        border-radius: 0.375rem;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #363636;
        padding: 0.5rem;
        border-radius: 0.375rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        color: #ffffff !important;
    }
    
    .stTabs [data-baseweb="tab-panel"] {
        color: #ffffff !important;
    }


    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #2d2d2d;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #505050;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #606060;
    }

    #MainMenu, footer {
        visibility: hidden;
    }
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Progress Bars */
    .stProgress > div > div > div {
        background-color: #0f62fe !important;
    }
    
    /* Info Messages */
    .stAlert {
        background-color: #363636;
        color: #ffffff;
        border: 1px solid #404040;
    }
</style>
""", unsafe_allow_html=True)

class ResearchAnalytics:
    def __init__(self, topic_data: Dict):
        self.topic_data = topic_data
        self.messages = topic_data.get("messages", [])
    
    def calculate_metrics(self) -> Dict:
        total_messages = len(self.messages)
        human_messages = len([m for m in self.messages if m["role"] == "user"])
        ai_messages = total_messages - human_messages
        
        return {
            "Research Quality": "92%",
            "Sources Verified": f"{human_messages}",
            "Citations": f"{ai_messages}",
            "Completion": "75%"
        }
    
    def analyze_topic(self) -> List[str]:
        return [
            "Key finding 1 from the research",
            "Important insight 2",
            "Critical observation 3"
        ]
    
    def extract_sources(self) -> List[Dict]:
        return [
            {"title": "Source 1", "url": "#", "relevance": "High"},
            {"title": "Source 2", "url": "#", "relevance": "Medium"}
        ]

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
    
    def create_topic_sidebar(self):
        with st.sidebar:
            st.markdown('<div class="topic-sidebar">', unsafe_allow_html=True)
            st.title("Research Topics")
            
            # New topic creation
            new_topic = st.text_input("New Research Topic")
            if st.button("Create Topic", use_container_width=True):
                if new_topic:
                    topic_id = self.topic_manager.create_topic(new_topic)
                    self.topic_manager.select_topic(topic_id)
                    st.rerun()
            
            # Topic list
            if st.session_state.topics:
                for topic_id, topic in st.session_state.topics.items():
                    selected = topic_id == st.session_state.current_topic
                    if st.button(
                        topic["name"],
                        key=f"topic_{topic_id}",
                        use_container_width=True,
                        type="primary" if selected else "secondary"
                    ):
                        self.topic_manager.select_topic(topic_id)
                        st.rerun()
    
    def create_research_view(self):
        if not st.session_state.current_topic:
            st.info("Select a topic to begin research")
            return
        
        topic = st.session_state.topics[st.session_state.current_topic]
        analytics = ResearchAnalytics(topic)
        
        # Topic header
        st.title(topic["name"])
        
        # Analytics panel
        with st.expander("📊 Research Analytics", expanded=True):
            metrics = analytics.calculate_metrics()
            cols = st.columns(4)
            for (metric, value), col in zip(metrics.items(), cols):
                with col:
                    st.metric(metric, value)
            
            # Research progress
            st.subheader("Research Progress")
            progress_data = pd.DataFrame({
                'Metric': ['Depth', 'Quality', 'Coverage'],
                'Score': [85, 92, 78]
            })
            st.bar_chart(progress_data.set_index('Metric'))
        
        # Summary panel
        with st.expander("📝 Research Summary", expanded=True):
            tabs = st.tabs(["Key Findings", "Sources", "Timeline"])
            
            with tabs[0]:
                st.markdown("#### Key Findings")
                for finding in analytics.analyze_topic():
                    st.markdown(f"• {finding}")
            
            with tabs[1]:
                st.markdown("#### Sources")
                for source in analytics.extract_sources():
                    st.markdown(f"- [{source['title']}]({source['url']}) - {source['relevance']}")
            
            with tabs[2]:
                st.markdown("#### Research Timeline")
                for msg in topic["messages"]:
                    st.markdown(f"**{msg['timestamp']}** ({msg['role']})")
        
        # Chat interface
        st.markdown("### Research Chat")
        for message in topic["messages"]:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        if prompt := st.chat_input("Research query..."):
            # Add user message
            topic["messages"].append({
                "role": "user",
                "content": prompt,
                "timestamp": datetime.now().isoformat()
            })
            
            try:
                # Get AI response
                with st.chat_message("assistant"):
                    stream = self.client.chat.completions.create(
                        model="gpt-4-turbo-preview",
                        messages=[
                            {"role": m["role"], "content": m["content"]}
                            for m in topic["messages"]
                        ],
                        stream=True
                    )
                    response = st.write_stream(stream)
                
                # Store AI response
                topic["messages"].append({
                    "role": "assistant",
                    "content": response,
                    "timestamp": datetime.now().isoformat()
                })
                
            except Exception as e:
                st.error(f"Error: {str(e)}")
    
    def run(self):
        self.create_topic_sidebar()
        self.create_research_view()

def main():
    with st.sidebar:
        openai_api_key = st.text_input("OpenAI API Key", type="password")
    
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.", icon="🔑")
        return
    
    app = ResearchChat(openai_api_key)
    app.run()

if __name__ == "__main__":
    main()