import os
import time
import streamlit as st
from langchain.memory import ConversationBufferMemory
from langchain.agents import initialize_agent, AgentType
from langchain_community.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage, AIMessage
from langchain_community.tools import WikipediaQueryRun, ArxivQueryRun, DuckDuckGoSearchRun
from langchain_community.utilities import WikipediaAPIWrapper, ArxivAPIWrapper, DuckDuckGoSearchAPIWrapper
from langdetect import detect
from deep_translator import GoogleTranslator
from dotenv import load_dotenv, find_dotenv

# Load environment variables
load_dotenv(find_dotenv())

# Initialize AI Tools
wiki = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=200))
arxiv = ArxivQueryRun(api_wrapper=ArxivAPIWrapper(top_k_results=1, doc_content_chars_max=200))
duckduckgo_search = DuckDuckGoSearchRun(api_wrapper=DuckDuckGoSearchAPIWrapper(region="in-en", time="y", max_results=2))

tools = [wiki, arxiv, duckduckgo_search]

# Initialize LLM using OpenAI's Library but Pointing to Groq
def load_llm():
    groq_api_key = os.getenv("GROQ_API_KEY")
    if not groq_api_key:
        raise ValueError("GROQ_API_KEY not found in environment variables")
    
    return ChatOpenAI(
        model_name="openai/gpt-oss-120b",
        temperature=1,
        openai_api_key=groq_api_key,  # Must use openai_api_key for compatibility
        openai_api_base="https://api.groq.com/openai/v1"
    )

# Translate text to English
def translate_to_english(text):
    try:
        detected_lang = detect(text)  # Detect language
        if detected_lang == "en":
            return text, "en"  # No translation needed

        translated_text = GoogleTranslator(source=detected_lang, target="en").translate(text)
        return translated_text, detected_lang  # Return translated text and original language
    except Exception as e:
        return text, "unknown"  # Return original text if translation fails

# Translate text back to the original language
def translate_back(text, target_lang):
    try:
        if target_lang == "en":
            return text  # No translation needed

        return GoogleTranslator(source="en", target=target_lang).translate(text)
    except Exception as e:
        return text  # Return original if translation fails

# Ensure Memory is Persistent Across Sessions
if "chat_memory" not in st.session_state:
    st.session_state.chat_memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# Create Conversational Agent with Proper Memory Usage
def get_conversational_agent():
    llm = load_llm()
    return initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        memory=st.session_state.chat_memory,
        verbose=True,
        return_intermediate_steps=True,
        max_iterations=5,
        handle_parsing_errors=True
    )

# Streamlit Chat UI
def main():
    # Set Background Image and Styling
    page_bg_img = '''
    <style>
    .stApp {
        background: linear-gradient(rgba(0, 0, 0, 0.4), rgba(0, 0, 0, 0.4)), 
                   url("https://images.squarespace-cdn.com/content/v1/6418b0756bfdeb13a8c56fcf/c976ed04-1ebc-4a48-b0fc-ac2dd8d8995c/Nakalembe_RSGraphic.png?format=1500w") no-repeat center center fixed;
        background-size: cover;
        color: white;
    }
    
    .stApp > div {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 25px;
        padding: 20px;
        margin: 10px;
        backdrop-filter: blur(5px);
    }
    
    .stChatMessage {
        background: rgba(255, 255, 255, 0.2) !important;
        backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        padding: 15px !important;
        border-radius: 20px !important;
        margin-bottom: 15px !important;
        color: #000 !important;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1) !important;
    }
    
    /* Force all text in chat messages to be black */
    .stChatMessage p, .stChatMessage div, .stChatMessage span, .stChatMessage * {
        color: #000 !important;
    }
    
    /* User message specific styling */
    div[data-testid="user-message"] {
        background: rgba(255, 255, 255, 0.15) !important;
        backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
    }
    
    div[data-testid="user-message"] p, 
    div[data-testid="user-message"] div, 
    div[data-testid="user-message"] span, 
    div[data-testid="user-message"] * {
        color: #000 !important;
    }
    
    /* Assistant message specific styling */
    div[data-testid="assistant-message"] {
        background: rgba(255, 255, 255, 0.25) !important;
        backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(255, 255, 255, 0.4) !important;
    }
    
    div[data-testid="assistant-message"] p, 
    div[data-testid="assistant-message"] div, 
    div[data-testid="assistant-message"] span, 
    div[data-testid="assistant-message"] * {
        color: #000 !important;
    }
    }
    
    h1, h2, h3 {
        color: white !important;
        text-align: center !important;
        font-weight: bold !important;
        background: none !important;
        -webkit-text-fill-color: white !important;
    }
    
    /* Ensure titles are always white and visible */
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        color: white !important;
        -webkit-text-fill-color: white !important;
        font-family: 'Dosis', sans-serif !important;
        italic: true !important;
    }
    .stWrite {
        font-family: 'Montserrat', sans-serif !important;
        italic: true !important;
    }
    .stButton > button {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 25px !important;
        padding: 12px 25px !important;
        font-weight: bold !important;
        font-size: 16px !important;
        box-shadow: 0 4px 15px rgba(17, 153, 142, 0.4) !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #38ef7d 0%, #11998e 100%) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(17, 153, 142, 0.6) !important;
    }
    
        .stTextInput > div > div > input {
        background-color: rgba(255, 255, 255, 0.9) !important;
        border-radius: 25px !important;
    }
    
    /* Logo styling */
    .logo-container {
        text-align: center;
        margin-bottom: 20px;
    }

    
    .stChatMessage {
        background: #F1F0F0; /* Light grey for assistant messages */
        padding: 10px;
        border-radius: 15px;
        margin-bottom: 10px;
        color: black; /* Ensures text is dark for readability */
    }
    .stChatMessage.user {
        background: #DCF8C6; /* Light green for user messages */
    }


    
    /* Success and warning messages */
    .stSuccess, .stWarning, .stError {
        border-radius: 15px !important;
        border: none !important;
        color: white !important;
        font-weight: bold !important;
    }
    
    .stSuccess {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%) !important;
        box-shadow: 0 4px 15px rgba(56, 239, 125, 0.4) !important;
    }
    
    .stWarning {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%) !important;
        box-shadow: 0 4px 15px rgba(240, 147, 251, 0.4) !important;
    }
    
    .stError {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a52 100%) !important;
        box-shadow: 0 4px 15px rgba(255, 107, 107, 0.4) !important;
    }
    
    /* Sidebar styling if any */
    .stSidebar {
        background-color: rgba(255, 255, 255, 0.1) !important;
    }
    
    /* st.write styling - italic and curly font */
    .stMarkdown, .stText {
        font-style: italic !important;
        color: white !important;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.7) !important;
    }
    
    /* Specific targeting for st.write content */
    div[data-testid="stMarkdownContainer"] p {
        font-style: italic !important;
        color: white !important;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.7) !important;
    }
    </style>
    '''
    st.markdown(page_bg_img, unsafe_allow_html=True)
    
    # Add logo at the top
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        try:
            st.image("RootSourcelogo.png", width=400, use_container_width=False)
        except:
            st.write("🌱 RootSource AI 🌱")  # Fallback if logo doesn't load
    
    st.title("RootSource AI")
    st.subheader("Ask your farming-related questions in any language, and get accurate answers!")
    st.write("Developed by : Team 'BlueDot'") 
    st.divider()
    


    if st.button("Reset Conversation"):
        st.session_state.chat_memory.clear()
        st.session_state.messages = []
        st.success("Chat history cleared!")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display past chat history
    for message in st.session_state.messages:
        st.chat_message(message["role"]).markdown(message["content"])

    # Get user input
    prompt = st.chat_input(" Ask your farming-related question here (in any language)..... ")

    if prompt:
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        try:
            translated_query, original_lang = translate_to_english(prompt)

            st.write(f"🔍 *Detected Language:* {original_lang.upper()}")  # Show detected language
            st.write(f"🔄 *Translated Query:* {translated_query}")  # Show translated query

            agent = get_conversational_agent()

            def trim_chat_memory(max_length=5):#
                """ Retains only the last `max_length` messages in memory. """
                chat_history = st.session_state.chat_memory.load_memory_variables({})["chat_history"]
                if len(chat_history) > max_length:
                    st.session_state.chat_memory.chat_memory.messages = chat_history[-max_length:]#
                return chat_history

            # Apply trimming before invoking the agent
            chat_history = trim_chat_memory(max_length=5)#

            conversation_context = "\n".join([msg.content for msg in chat_history])

            full_prompt = f"""
You are a helpful and expert AI assistant for farming and agriculture questions.
Your primary goal is to answer the USER'S QUESTION accurately and concisely.

**IMPORTANT INSTRUCTIONS:**
1. **If the question is not related at all to agriculture domain, strictly say that ""please ask questions related to agriculture only"".** Only answer if its related to agricultural field.

2. **Understand the User's Question First:** Carefully analyze the question to determine what the user is asking about farming or agriculture.

3. **Search Strategically (Maximum 2 Searches):** You are allowed to use tools (search engine, Wikipedia, Arxiv) for a MAXIMUM of TWO searches to find specific information DIRECTLY related to answering the USER'S QUESTION.  Do not use tools for general background information unless absolutely necessary to answer the core question.

4. **STOP Searching and Answer Directly:**  **After a maximum of TWO searches, IMMEDIATELY STOP using tools.**  Even if you haven't found a perfect answer, stop searching.

5. **Formulate a Concise Final Answer:** Based on the information you have (from searches or your existing knowledge), construct a brief, direct, and helpful answer to the USER'S QUESTION.  Focus on being accurate and to-the-point.

6. **If you ALREADY KNOW the answer confidently without searching, answer DIRECTLY and DO NOT use tools.** Only use tools if you genuinely need to look up specific details to answer the user's question.


Question: [User's Question]
Thought: I need to think step-by-step how to best answer this question.
Action: [Tool Name] (if needed, otherwise skip to Thought: Final Answer)
Action Input: [Input for the tool]
Observation: [Result from the tool]
... (repeat Thought/Action/Observation up to 2 times MAX)
Thought: Final Answer - I have enough information to answer the user's question now.
Final Answer: [Your concise and accurate final answer to the User's Question]


**User's Question:** {prompt}
"""

            # Retry in case of rate-limit errors
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    response = agent.invoke({"input": full_prompt})
                    break  # Exit loop if successful
                except Exception as e:
                    st.warning(f"⚠ API Rate Limit! Retrying {attempt + 1}/{max_retries}...")
                    time.sleep(2)  # Wait and retry

            response_text = response["output"] if isinstance(response, dict) and "output" in response else str(response)
            final_response = translate_back(response_text, original_lang)  # Translate back to original language

            st.chat_message("assistant").markdown(final_response)
            st.session_state.messages.append({"role": "assistant", "content": final_response})

        except Exception as e:
            st.error(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
