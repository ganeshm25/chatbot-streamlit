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

# Custom styling combining both versions
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

    .stButton button[data-testid="baseButton-primary"] {
        background-color: #0f62fe !important;
        border-color: #0f62fe !important;
    }

    /* Added filters button style */
    .filter-button {
        background-color: #363636 !important;
        color: #ffffff !important;
        border: 1px solid #404040;
        padding: 0.5rem;
        border-radius: 0.375rem;
    }

    [data-testid="stMarkdownContainer"] {
        color: #ffffff !important;
    }

    .stTextInput input {
        background-color: #363636 !important;
        color: #ffffff !important;
        border: 1px solid #404040 !important;
    }

    [data-testid="stMetricValue"] {
        color: #ffffff !important;
    }

    [data-testid="stMetricLabel"] {
        color: #a0a0a0 !important;
    }

    .stChatMessage [data-testid="stChatMessageContent"] {
        background-color: #363636 !important;
        color: #ffffff !important;
        border: 1px solid #404040 !important;
    }

    .streamlit-expanderHeader {
        background-color: #363636 !important;
        color: #ffffff !important;
    }

    .stTabs [data-baseweb="tab"] {
        color: #ffffff !important;
    }

    .stAlert {
        background-color: #363636;
        color: #ffffff;
        border: 1px solid #404040;
    }

    /* Maintain dark scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }

    ::-webkit-scrollbar-track {
        background: #2d2d2d;
    }

    ::-webkit-scrollbar-thumb {
        background: #505050;
        border-radius: 4px;
    }

    #MainMenu, footer {
        visibility: hidden;
    }

    /* Chart colors */
    .stChart > div > div > svg {
        background-color: #363636 !important;
    }
  
    /* Filter Panel */
    .filter-panel {
        background-color: #363636;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #404040;
    }
    
    .stSlider [data-baseweb="slider"] {
        background-color: #505050;
    }
    
    .stMultiSelect {
        background-color: #363636;
        border-color: #404040;
    }
     
    [data-testid="baseButton-secondary"]:has(div:contains("Filter")) {
        background-color: #f3f4f6 !important;
        border-radius: 1.5rem !important;
        width: auto !important;
    }
            
                /* New filter panel styles */
    .filter-column {
        position: sticky;
        top: 0;
        background: #363636;
        border-left: 1px solid #404040;
        padding: 1rem;
        height: 100vh;
        overflow-y: auto;
    }
    
    .research-input-container {
        display: flex;
        gap: 1rem;
        align-items: center;
        margin-top: 1rem;
    }
    
    .filter-button-container {
        display: flex;
        justify-content: flex-end;
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
        
            # Dummy metrics for demonstration
        return {
            "Overall Authenticity Score": "85%",
            "Research Quality Score": "85%",
            "Sources Verified": f"{human_messages}",
            "Source Reliability": "92%",
            "Citations": f"{ai_messages}",
            "Fact Check Score": "88%",
            "Verification Index": "90%",
            "Bias Score": "88%",
            "Interpretability Found": "12",
            "Research Depth": "High",
            "Total Exchanges": f"{human_messages}",
            "Average Response Length": "450 words",
            "Completion": "25%"
        }
    
    def analyze_topic(self) -> List[str]:
        return [
            "Key finding 1 from the research",
            "Important insight 2",
            "Critical observation 3"
        ]
    
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

    def create_filter_panel(self):
        st.markdown('<div class="filter-panel">', unsafe_allow_html=True)
        st.markdown("### Research Filters")
        st.divider()
        
        st.markdown("#### Year Range")
        years = st.slider("Select years", 2000, 2024, (2020, 2024))
        
        st.markdown("#### Source Type")
        st.multiselect(
            "Select sources",
            ["Academic Papers", "Journals", "Conference Proceedings", "Books"],
            default=["Academic Papers"]
        )
        
        st.markdown("#### Research Domain")
        st.multiselect(
            "Select domains",
            ["Computer Science", "Engineering", "Mathematics", "Physics"],
            default=["Computer Science"]
        )
        
        st.markdown("#### Country/Region")
        st.multiselect(
            "Select regions",
            ["North America", "Europe", "Asia", "Global"],
            default=["Global"]
        )
        st.markdown('</div>', unsafe_allow_html=True)

    def create_topic_sidebar(self):
        with st.sidebar:
            st.markdown('<div class="topic-sidebar">', unsafe_allow_html=True)
            st.title("Authentifi.ai")
            st.image("logo.png", width=150)  # Add your logo
            
            # Search and filters
            st.text_input("Search topics...", placeholder="Enter keywords...")
            col1, col2 = st.columns([1,1])
            with col1:
                st.toggle("Pro")
            with col2:
                st.selectbox("Filter", ["All", "Recent"])
            
            st.divider()
            
            tabs = st.tabs(["Topics", "History"])
       
            # Topics tab
            with tabs[0]:
                # Topic creation
                new_topic = st.text_input("New Research Topic")
                if st.button("Create Topic", use_container_width=True):
                    if new_topic:
                        topic_id = self.topic_manager.create_topic(new_topic)
                        self.topic_manager.select_topic(topic_id)
                        st.rerun()
                
                # Topics list
                if st.session_state.topics:
                    st.markdown("### Research Topics")
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
                   # History tab
            with tabs[1]:
                if st.session_state.topics:
                    for topic_id, topic in sorted(
                        st.session_state.topics.items(),
                        key=lambda x: x[1]["created_at"],
                        reverse=True
                    ):
                        st.markdown(
                            f"""
                            **{topic['name']}**  
                            Created: {datetime.fromisoformat(topic['created_at']).strftime('%Y-%m-%d %H:%M')}
                            """
                        )
                        st.divider()
    
    def create_research_view(self):
        if not st.session_state.current_topic:
            st.info("Select a topic to begin research")
            return
        
        if 'show_filters' not in st.session_state:
            st.session_state.show_filters = False

        topic = st.session_state.topics[st.session_state.current_topic]
        analytics = ResearchAnalytics(topic)
        summary = analytics.generate_summary()

        # Topic header with actions
        main_col, filter_col, share_col = st.columns([6,1,1])
        with main_col:
            st.title(topic["name"])
            # Analytics panel
            with st.expander("📊 Research Analytics", expanded=True):
                metrics = analytics.calculate_metrics()
                cols = st.columns(4)
                for (metric, value), col in zip(metrics.items(), cols):
                    with col:
                        st.metric(metric, value)
                
                st.subheader("Research Progress")
                progress_data = pd.DataFrame({
                    'Metric': ['Depth', 'Quality', 'Coverage'],
                    'Score': [85, 92, 78]
                })
                st.bar_chart(progress_data.set_index('Metric'))
            
            # Summary panel
            with st.expander("📝 Research Summary", expanded=True):
                tabs = st.tabs(["Interaction Summary", "Sources", "Timeline", "Key Findings"])
                
                with tabs[0]:
                    st.markdown("#### Interaction Summary")
                    for finding in analytics.generate_summary():
                        st.markdown("### Key Interactions")
                
                        for msg in summary:
                            role_icon = "👤" if msg["role"] == "user" else "🤖"
                            role_class = "human-message" if msg["role"] == "user" else "ai-message"
                            
                            st.markdown(f"""
                                <div class="conversation-item {role_class}">
                                    <strong>{role_icon} {msg["role"].title()}</strong><br>
                                    {msg["content"]}
                                </div>
                            """, unsafe_allow_html=True)
                
                with tabs[1]:
                    st.markdown("#### Sources")
                    for source in analytics.extract_sources():
                        st.markdown(f"- [{source['title']}]({source['url']}) - {source['relevance']}")
                
                with tabs[2]:
                    st.markdown("#### Research Timeline")
                    for msg in topic["messages"]:
                        st.markdown(f"**{msg['timestamp']}** ({msg['role']})")
                with tabs[3]:
                    st.markdown("#### Key Findings")
                    for finding in analytics.analyze_topic():
                        st.markdown(f"• {finding}")

                # Chat interface
                st.markdown("### Research Chat")
                for message in topic["messages"]:
                    with st.chat_message(message["role"]):
                        st.markdown(message["content"])
                
                chat_container = st.container()
                with chat_container:
                    input_col, filter_btn_col = st.columns([5,1])
                    with input_col:
                        prompt = st.chat_input("Enter your Research query...")
                    with filter_btn_col:
                        if st.button("🔍 Filter"):
                            st.session_state.show_filters = not st.session_state.show_filters


                if prompt:
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
        with share_col:
            st.button("🔗 Collaborate ", use_container_width=True)
        with filter_col:
            if st.session_state.show_filters:
                self.create_filter_panel()

    
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
            <p>AI-Powered Trust and Transparency in Education Research</p>
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