import streamlit as st
from llama_query import LlamaQuery

# Load pre-trained model
st.title("RAG Chatbot")
st.write("This is a simple chatbot that uses the RAG model to generate responses. Extracts keywords from the user's prompt and performs a Google search to generate a response.")

st.divider()

api_key = "lm-studio"
llama_query = LlamaQuery("", api_key)

# Add a slider in the sidebar for the number of searches
st.sidebar.title("Settings")
use_RAG = st.sidebar.checkbox("Activate RAG", value=True)

num_max_keywords = st.sidebar.slider(
    "Number of Keywords", min_value=1, max_value=10, value=5)

num_searches = st.sidebar.slider(
    "Number of Searches for each keyword", min_value=1, max_value=10, value=3)

# Add a selectbox in the sidebar for language selection
language = st.sidebar.selectbox(
    "Select Language",
    ("en", "sp", "fr", "nl")
)

# Add a selectbox in the sidebar for region selection
region = st.sidebar.selectbox(
    "Select Region",
    ("uk", "us", "eu")
)

if st.sidebar.button("Clear Chat"):
    st.session_state['chat_history'] = []

llama_query.set_num_searches(num_searches)

# Initialize chat history if it doesn't exist
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

prompt = st.chat_input("Say something")
# Add a button to clear chat history

if prompt:
    st.session_state['chat_history'].append(f"{prompt}")
    llama_query.set_prompt(prompt)
    llama_query.set_language(language)
    llama_query.set_region(region)
    llama_query.set_max_num_keywords(num_max_keywords)
    completion = llama_query.run(use_RAG)
    links = llama_query.get_urls()
    keywords = llama_query.get_keywords()
    completion = llama_query.get_completion()
    llama_query.reset()
    if use_RAG:
        st.session_state['chat_history'].append(f"{completion}\n\n[Links] {links}\n\n[Keywords] {keywords}")
    else:
        st.session_state['chat_history'].append(f"{completion}")

# Display updated chat history with colors
for i, message in enumerate(st.session_state['chat_history']):
    if i % 2 == 0:
        with st.chat_message("user"):
            st.write(message)
    else:
        with st.chat_message("assistant"):
            st.write(message)
