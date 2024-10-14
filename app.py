# Fully using - https://cookbook.openai.com/examples/assistants_api_overview_python
import streamlit as st
from openai import OpenAI
import os
import time


STEPH_ID = STEPH_ID = os.getenv("ASSISTANT_ID")
client = OpenAI(api_key = os.getenv("OPENAI_API_KEY"))

def submit_message(assistant_id, thread, user_message):
    client.beta.threads.messages.create(
        thread_id=thread.id, role="user", content = user_message
    )
    return client.beta.threads.runs.create(
        thread_id = thread.id,
        assistant_id = assistant_id,
    )

def get_response(thread, message):
    #print(client.beta.threads.messages.list(thread_id=thread.id, order="asc"))
    return client.beta.threads.messages.list(thread_id=thread.id, order="asc", after=message.id)

def create_thread_and_run(user_input):
    thread = client.beta.threads.create()
    run = submit_message(STEPH_ID, thread, user_input)
    return thread, run

def pretty_print(messages):
    for m in messages:
        if m.role=="assistant":
            print(f"{m.role}: {m.content[0].text.value}")
    print()

def wait_on_run(run, thread):
    while run.status == "queued" or run.status == "in_progress":
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id,
        )
        time.sleep(0.1)
    return run


def generate_response(messages):
    for m in messages:
        return m.content[0].text.value 


#### ------------------- Streamlit -------------------------- ####

st.title("Stephanie, your user research assistant")
st.write("Welcome to the Adore Me Beta Testing Platform! As promised, our conversation is confidential and will not be shared outside of Adore Me. Are you ready to proceed further?")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt0 = "Let's start"
thread1, run1 = create_thread_and_run(prompt0)
run1 = wait_on_run(run1, thread1)

if prompt:=st.chat_input("Ask Stephanie.."):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    message = client.beta.threads.messages.create( thread_id=thread1.id, role="user", content = prompt)
    run2 = client.beta.threads.runs.create(thread_id=thread1.id, assistant_id = STEPH_ID)
    run2 = wait_on_run(run2, thread1)

    with st.chat_message("assistant"):
        reply0 = get_response(thread1, message)
        reply = generate_response(reply0)
        st.markdown(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})




