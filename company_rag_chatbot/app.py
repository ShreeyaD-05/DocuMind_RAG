import streamlit as st
from rag_pipeline import retrieve_context, generate_answer

st.set_page_config(
    page_title="Flipkart Company Chatbot",
    page_icon="🛒",
    layout="centered"
)

st.markdown(
    """
    <style>
    .title {text-align:center; font-size:36px; font-weight:bold;}
    .subtitle {text-align:center; color:gray;}
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<div class="title">🛒 Flipkart Company Chatbot</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Context-aware RAG-based AI Assistant</div>', unsafe_allow_html=True)
st.markdown("---")

question = st.text_input("Ask a question about Flipkart")

if st.button("Get Answer"):
    if question.strip():
        with st.spinner("Thinking..."):
            context = retrieve_context(question)
            answer = generate_answer(question, context)
        st.success("Answer")
        st.write(answer)
    else:
        st.warning("Please enter a question")