import streamlit as st
from langchain.chat_models import init_chat_model
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage,AIMessage,SystemMessage
from langchain_core.prompts import ChatPromptTemplate
import os


st.set_page_config(page_title="Simple Langchain Chatbot with Groq" ,page_icon="🚀")
st.title("🚀 SimplyChat")
st.markdown("Learn langchain basic with groqs ultra-fast inference!")


with st.sidebar:
    st.header("Settings")

    api_key=st.text_input("GROQ API KEY",type="password",help="Get free API key at console.groq.com")
    model_name=st.selectbox(
        "Model",
        ["llama-3.1-8b-instant","deepseek-r1-distill-llama-70b","gemma2-9b-it"],
        index=0  )
    
    if st.button("Clear Chat"):
       st.session_state.messages=[]
       st.rerun()


if "messages" not in st.session_state:
    st.session_state.messages=[]

@st.cache_resource
def get_chain(api_key,model_name):
    if not api_key:
        return None
    
    llm=ChatGroq(groq_api_key=api_key,
             model_name=model_name,
             temperature=0.7,
             streaming=True)
    

    prompt=ChatPromptTemplate.from_messages([
        ("system","You are a helpful assistant powered by Groq. Answer question clearly and concisely"),
        ("user","{question}")
    ])

    ##create a chain 
    chain=prompt|llm|StrOutputParser()
    return chain

chain=get_chain(api_key,model_name)    

if not chain:
    st.warning("👆 Please enter your Groq API key in the sidebar to start chatting!")
    st.markdown("[Get your free API key here](https://console.groq.com)")

else:

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])


    if question:= st.chat_input("Ask me anything"):
        st.session_state.messages.append({"role":"user","content":question})
        with st.chat_message("user"):
            st.write(question)

        with st.chat_message("assistant"):
            message_placeholder=st.empty()
            full_response=""

            try:

                for chunk in chain.stream({"question":question}):
                    full_response+=chunk
                    message_placeholder.markdown(full_response+" ")

                message_placeholder.markdown(full_response)   
                 
                st.session_state.messages.append({"role":"assistant","content":full_response})
                


            except Exception as e:
                st.error(f"Error: {str(e)}")


st.markdown("---") 
st.markdown("### 💡 Try these examples")
col1, col2 = st.columns(2)
with col1:
    st.markdown("- What is LangChain and how does it work?")
    st.markdown("- Summarize the latest advancements in AI.")
with col2:
    st.markdown("- Explain the difference between supervised and unsupervised learning.")
    st.markdown("- How can I use Groq API with LangChain?")
st.markdown("---")
st.markdown(
            "<div style='text-align: center; color: gray;'>"
            "Made with ❤️ using Streamlit, LangChain, and Groq &copy; 2025"
            "</div>",
            unsafe_allow_html=True
        )




