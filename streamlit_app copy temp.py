import streamlit as st
from openai import OpenAI
from datetime import datetime
from typing import Dict, List
import uuid
import pandas as pd

# Page configuration
st.set_page_config(
    layout="wide",
    page_title="Authentifi",
    page_icon="🔐"
)
# Custom styling
st.markdown("""
<style>
    /* Base theme */
    .stApp {
        background-color: #ffffff;
    }
    
    /* Navigation */
    [data-testid="stSidebar"] {
        background-color: #f8f9fa;
        border-right: 1px solid #e5e7eb;
    }
    
    /* Search bar */
    .search-container {
        padding: 1rem;
        border-bottom: 1px solid #e5e7eb;
    }
    
    .search-input {
        width: 100%;
        padding: 0.5rem;
        border: 1px solid #e5e7eb;
        border-radius: 0.5rem;
    }
    
    /* Topic list */
    .topic-list {
        padding: 0.5rem;
    }
    
    .topic-item {
        padding: 0.75rem;
        margin: 0.25rem 0;
        border-radius: 0.5rem;
        background: transparent;
        border: 1px solid #e5e7eb;
        cursor: pointer;
        color: #374151;
    }
    
    .topic-item:hover {
        background-color: #f3f4f6;
    }
    
    .topic-item.active {
        background-color: #f0f7ff;
        border-color: #2563eb;
    }
    
    /* Content area */
    .main-content {
        padding: 2rem;
        color: #111827;
    }
    
    /* Research panels */
    .research-panel {
        background-color: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 0.5rem;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }
    
    /* Typography */
    h1, h2, h3, h4, h5, h6 {
        color: #111827 !important;
    }
    
    p, span, div {
        color: #374151;
    }
    
    /* Metrics */
    [data-testid="stMetric"] {
        background-color: #f9fafb;
        padding: 1rem;
        border-radius: 0.5rem;
    }
    
    /* Chat interface */
    .chat-container {
        border: 1px solid #e5e7eb;
        border-radius: 0.5rem;
        padding: 1rem;
    }
    
    .stChatMessage {
        background-color: transparent;
        padding: 0.5rem 0;
    }
    
    .stChatMessage [data-testid="stChatMessageContent"] {
        background-color: #f9fafb;
        border: 1px solid #e5e7eb;
        border-radius: 0.5rem;
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
    
    def create_header(self):
        """Create main header with search and filters"""
        st.markdown('<div class="search-container">', unsafe_allow_html=True)
        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            st.text_input("Search research topics...", placeholder="Enter keywords...")
        with col2:
            st.toggle("Pro", value=True)
        with col3:
            st.selectbox("Filter", ["All", "Recent", "Popular"])
        st.markdown("</div>", unsafe_allow_html=True)

    def create_topic_sidebar(self):
        with st.sidebar:
            st.markdown('<div class="topic-sidebar">', unsafe_allow_html=True)
            st.title("Authentifi")
            
            # Topic creation
            with st.expander("Create Topic", expanded=False):
                new_topic = st.text_input("Topic name", placeholder="Enter topic name")
                col1, col2 = st.columns([1,1])
                with col1:
                    st.toggle("Pro")
                with col2:
                    if st.button("Create", use_container_width=True):
                        if new_topic:
                            topic_id = self.topic_manager.create_topic(new_topic)
                            self.topic_manager.select_topic(topic_id)
                            st.rerun()
            
            # Topics list
            st.subheader("Research Topics")
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
        # Content header
        st.title(topic["name"])
        
    # Search and filters
        col1, col2, col3 = st.columns([3,1,1])
        with col1:
            st.text_input("Search within topic...", placeholder="Enter keywords...")
        with col2:
            st.toggle("Pro", value=True)
            st.button("🔗 Share", use_container_width=True)
        with col3:
            st.selectbox("Filter", ["All", "Recent", "Popular"])

        
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
    st.markdown("""
        <style>
            .app-header { text-align: center; padding: 1rem; }
        </style>
        <div class="app-header">
            <h1>Authentifi</h1>
            <p>AI-Powered Content Authentication & Research</p>
        </div>
    """, unsafe_allow_html=True)
    with st.sidebar:
        openai_api_key = st.text_input("OpenAI API Key", type="password")
    
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.", icon="🔑")
        return
    
    app = ResearchChat(openai_api_key)
    app.run()

if __name__ == "__main__":
    main()