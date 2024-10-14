# https://cookbook.openai.com/examples/assistants_api_overview_python
from openai import OpenAI
import os
import time

STEPH_ID = os.getenv("ASSISTANT_ID")
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


if __name__=="__main__":
    print("^(Stephanie)^ :Welcome to the Adore Me Beta Testing Platform! As promised, our conversation is confidential and will not be shared outside of Adore Me. Are you ready to proceed further?")
    prompt0 = input("@(You)@:")
    thread1, run1 = create_thread_and_run(prompt0)
    run1 = wait_on_run(run1, thread1)
    messages = client.beta.threads.messages.list(thread_id=thread1.id, order="asc")
    pretty_print(messages)
    while True:
        prompt = input("@(You)@:")
        message = client.beta.threads.messages.create( thread_id=thread1.id, role="user", content = prompt)
        run2 = client.beta.threads.runs.create(thread_id=thread1.id, assistant_id = STEPH_ID)
        run2 = wait_on_run(run2, thread1)
        messages = get_response(thread1, message)
        pretty_print(messages)