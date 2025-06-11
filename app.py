import validators,streamlit as st
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain.chains.summarize import load_summarize_chain
from langchain_community.document_loaders import YoutubeLoader,UnstructuredURLLoader

# Custom CSS for beautiful styling
st.markdown("""
<style>
    /* Main background gradient */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Custom header styling */
    .main-header {
        background: linear-gradient(90deg, #ff6b6b, #ffd93d, #6bcf7f, #4ecdc4, #45b7d1);
        background-size: 300% 300%;
        animation: gradient 8s ease infinite;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    }
    
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .main-header h1 {
        color: white;
        font-size: 3rem;
        font-weight: 700;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        margin: 0;
    }
    
    .main-header p {
        color: rgba(255,255,255,0.9);
        font-size: 1.2rem;
        margin-top: 0.5rem;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #2c3e50 0%, #3498db 100%);
    }
    
    /* Input fields styling - Enhanced contrast */
    .stTextInput > div > div > input {
        background: rgba(0, 0, 0, 0.8) !important;
        color: white !important;
        border: 2px solid rgba(255, 255, 255, 0.3);
        border-radius: 10px;
        padding: 0.75rem;
        font-size: 1rem;
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #4ecdc4 !important;
        box-shadow: 0 0 20px rgba(78, 205, 196, 0.5);
        background: rgba(0, 0, 0, 0.9) !important;
        color: white !important;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: rgba(255, 255, 255, 0.7) !important;
    }
    
    /* Sidebar input fields */
    .css-1d391kg .stTextInput > div > div > input {
        background: rgba(0, 0, 0, 0.7) !important;
        color: white !important;
        border: 2px solid rgba(255, 255, 255, 0.3);
    }
    
    .css-1d391kg .stTextInput > div > div > input:focus {
        background: rgba(0, 0, 0, 0.9) !important;
        color: white !important;
        border-color: #4ecdc4 !important;
    }
    
    .css-1d391kg .stTextInput > div > div > input::placeholder {
        color: rgba(255, 255, 255, 0.6) !important;
    }
    
    /* Label styling for better visibility */
    .stTextInput > label {
        color: white !important;
        font-weight: 600 !important;
        margin-bottom: 0.5rem !important;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(45deg, #ff6b6b, #ffd93d);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-size: 1.1rem;
        font-weight: 600;
        box-shadow: 0 4px 15px rgba(255, 107, 107, 0.3);
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(255, 107, 107, 0.4);
        background: linear-gradient(45deg, #ffd93d, #ff6b6b);
    }
    
    .stButton > button:active {
        transform: translateY(0px);
    }
    
    /* Success message styling */
    .stSuccess {
        background: linear-gradient(90deg, #6bcf7f, #4ecdc4);
        border-radius: 10px;
        padding: 1rem;
        border: none;
        color: white;
        font-weight: 500;
    }
    
    /* Warning message styling */
    .stWarning {
        background: linear-gradient(90deg, #ffd93d, #ff9068);
        border-radius: 10px;
        padding: 1rem;
        border: none;
        color: white;
        font-weight: 500;
    }
    
    /* Error message styling */
    .stError {
        background: linear-gradient(90deg, #ff6b6b, #ff8e8e);
        border-radius: 10px;
        padding: 1rem;
        border: none;
        color: white;
        font-weight: 500;
    }
    
    /* Card styling for content */
    .content-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    /* Spinner styling */
    .stSpinner {
        background: linear-gradient(45deg, #667eea, #764ba2);
        border-radius: 50%;
    }
    
    /* Info box styling */
    .info-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        text-align: center;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

## Enhanced Header
st.markdown("""
<div class="main-header">
    <h1>🎯 AI Content Summarizer</h1>
    <p>Transform YouTube videos and web articles into concise summaries using advanced AI</p>
</div>
""", unsafe_allow_html=True)

# Create columns for better layout
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    # Enhanced sidebar
    with st.sidebar:
        st.markdown("### 🔑 API Configuration")
        groq_api_key = st.text_input(
            "Enter your Groq API Key", 
            value="", 
            type="password",
            help="Get your free API key from https://console.groq.com/"
        )
        
        st.markdown("---")
        st.markdown("### 📋 Instructions")
        st.markdown("""
        1. **Get API Key**: Sign up at [Groq Console](https://console.groq.com/)
        2. **Enter URL**: Paste YouTube or website URL
        3. **Click Summarize**: Get AI-powered summary
        """)
        
        st.markdown("---")
        st.markdown("### 🌟 Features")
        st.markdown("""
        - 🎥 YouTube video summaries
        - 🌐 Website article summaries
        - 🤖 Multiple AI models
        - ⚡ Fast processing
        """)

    # URL input with enhanced styling
    st.markdown("### 🔗 Enter Content URL")
    generic_url = st.text_input(
        "URL", 
        label_visibility="collapsed",
        placeholder="Paste YouTube URL or website link here...",
        help="Supports YouTube videos and most website articles"
    )

    # Model initialization with visual feedback
    llm = None
    if groq_api_key.strip():
        with st.spinner("🚀 Initializing AI models..."):
            models_to_try = ["llama3-8b-8192", "llama3-70b-8192", "mixtral-8x7b-32768", "llama2-70b-4096"]
            
            for model in models_to_try:
                try:
                    llm = ChatGroq(model=model, groq_api_key=groq_api_key)
                    st.success(f"✅ Successfully connected with **{model}**")
                    break
                except Exception as e:
                    st.warning(f"⚠️ {model}: {str(e)[:50]}...")
                    continue
            
            if not llm:
                st.error("❌ Could not initialize any AI model. Please check your API key.")

    # Enhanced prompt template
    prompt_template = """
    📝 **CONTENT SUMMARY REQUEST**
    
    Please provide a comprehensive yet concise summary of the following content in approximately 300 words:
    
    **Content:** {text}
    
    **Instructions:**
    - Highlight the main points and key insights
    - Maintain the original tone and context
    - Structure the summary in a clear, readable format
    - Include any important statistics or quotes if present
    """
    
    prompt = PromptTemplate(template=prompt_template, input_variables=["text"])

    # Enhanced button with better spacing
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("🎯 Generate AI Summary", use_container_width=True):
        # Input validation with better error messages
        if not groq_api_key.strip():
            st.error("🔑 Please enter your Groq API key in the sidebar to continue.")
        elif not generic_url.strip():
            st.error("🔗 Please enter a valid URL (YouTube or website) to summarize.")
        elif not validators.url(generic_url):
            st.error("❌ Please enter a valid URL format. Ensure it starts with http:// or https://")
        elif not llm:
            st.error("🤖 AI model not initialized. Please check your API key and try again.")
        else:
            try:
                # Enhanced loading experience
                with st.spinner("🔍 Analyzing content and generating summary..."):
                    # Progress indicator
                    progress_bar = st.progress(0)
                    
                    # Loading content
                    progress_bar.progress(25)
                    if "youtube.com" in generic_url or "youtu.be" in generic_url:
                        st.info("🎥 Processing YouTube video...")
                        loader = YoutubeLoader.from_youtube_url(generic_url, add_video_info=True)
                    else:
                        st.info("🌐 Processing website content...")
                        loader = UnstructuredURLLoader(
                            urls=[generic_url],
                            ssl_verify=False,
                            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
                        )
                    
                    progress_bar.progress(50)
                    docs = loader.load()
                    
                    progress_bar.progress(75)
                    # Generate summary
                    chain = load_summarize_chain(llm, chain_type="stuff", prompt=prompt)
                    output_summary = chain.invoke({"input_documents": docs})
                    
                    progress_bar.progress(100)
                    
                    # Display results with enhanced formatting
                    st.markdown("---")
                    st.markdown("## 📄 AI-Generated Summary")
                    
                    # Simple text display without card styling
                    st.write(output_summary["output_text"])
                    
                    # Additional info
                    st.markdown("---")
                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.metric("📊 Content Source", "YouTube" if "youtube" in generic_url else "Website")
                    with col_b:
                        st.metric("🤖 AI Model", llm.model_name if llm else "Unknown")
                        
            except Exception as e:
                st.error(f"❌ **Error occurred:** {str(e)}")
                st.markdown("""
                **Possible solutions:**
                - Check if the URL is accessible
                - Verify your internet connection
                - Ensure the API key is valid
                - Try a different URL
                """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 2rem; color: rgba(255,255,255,0.8);">
    <p>🚀 Powered by <strong>Groq AI</strong> & <strong>LangChain</strong></p>
    <p>Made with ❤️ by <strong>Harsh</strong> using <strong>Streamlit</strong></p>
    <p>
        <a href="https://github.com/harsh-codess" target="_blank" style="
            color: #4ecdc4; 
            text-decoration: none; 
            font-weight: 600;
            transition: color 0.3s ease;
        " onmouseover="this.style.color='#ffd93d'" onmouseout="this.style.color='#4ecdc4'">
            🔗 GitHub: harsh-codess
        </a>
    </p>
</div>
""", unsafe_allow_html=True)
