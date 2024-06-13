import streamlit as st
from assistant import *
import time


with st.sidebar:
    # st.write("Vector store ID:", vector_store_id)
# st.write("Assistant ID:", assistant_id)
    assistant_id = st.text_input(
        "Provide your own assistant",
        "asst_iRAB8xpx9HNqn0EcCupWCLkP",
        key="assistant",
    )

    vector_store_id = st.text_input(
        "Provide your own vector store",
        "vs_skv7WVmYFuKulAGhceWzY0Vu",
        key="vectorstore",
    )

st.title("Copilot Assistant")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    if st.session_state.get('thread_id') is None:
        thread_id = startAssistantThread(prompt)
        st.session_state.thread_id = thread_id
    else:
        thread_id = st.session_state.get('thread_id')
        createMessage(thread_id, prompt)
        

    run_id = runAssistant(thread_id, assistant_id)
    # st.write("Run ID:" + run_id)
    st.session_state.run_id = run_id

    status = checkRunStatus(st.session_state.thread_id, st.session_state.run_id)
    st.session_state.status = status

    while st.session_state.status != 'completed':
        with st.spinner("Waiting for the process to complete ..."):
            time.sleep(10)
            st.session_state.status = checkRunStatus(st.session_state.thread_id, st.session_state.run_id)

    thread_messages = retrieveThread(st.session_state.thread_id)
    st.session_state.status = '';
    latestMessage = thread_messages[0]
    st.session_state.messages.append({"role": "assistant", "content": latestMessage['content']})
    st.chat_message("assistant").write(latestMessage['content'])
    # for message in thread_messages:
    #     msg = message['content']
    #     st.session_state.messages.append({"role": "assistant", "content": msg})
    #     st.chat_message("assistant").write(msg)
