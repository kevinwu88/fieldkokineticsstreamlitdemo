import streamlit as st
from openai import OpenAI
import os


def creaeteAssistant(vector_store_id, title):
	client = OpenAI(api_key=st.secrets["openai_api_key"])

	instructions = """ You are a helpful assistant. Use your knowledge to answer user's questions """

	assistant = client.beta.assistants.create(
	  name=title,
	  instructions=instructions,
	  tools=[{"type": "file_search"}],
	  model="gpt-4o",
	  tool_resources={"file_search": {"vector_store_ids": [vector_store_id]}},
	)

	return assistant.id


def saveFileOpenAI(location):
	client = OpenAI(api_key=st.secrets["openai_api_key"])
	file = client.files.create(file=open(location, "rb"), purpose="assistants")
	os.remove(location)
	return file.id

def createVectorStore(file_ids):
	client = OpenAI(api_key=st.secrets["openai_api_key"])

	vector_store = client.beta.vector_stores.create(
		name="Support Kevin Hello World",
		file_ids=file_ids
	)
	return vector_store.id



def startAssistantThread(prompt):
	messages = [{"role": "user", "content":prompt}]
	client = OpenAI(api_key=st.secrets["openai_api_key"])
	thread = client.beta.threads.create(messages=messages)
	return thread.id



def runAssistant(thread_id, assistant_id):
	client = OpenAI(api_key=st.secrets["openai_api_key"])
	run = client.beta.threads.runs.create(
			thread_id=thread_id,
			assistant_id=assistant_id
		)
	return run.id


def checkRunStatus(thread_id, run_id):
	client = OpenAI(api_key=st.secrets["openai_api_key"])
	run = client.beta.threads.runs.retrieve(
		thread_id=thread_id,
		run_id=run_id
		)
	return run.status


def retrieveThread(thread_id):
	client = OpenAI(api_key=st.secrets["openai_api_key"])
	thread_messages = client.beta.threads.messages.list(thread_id)
	list_messages = thread_messages.data
	thread_messages = []
	for message in list_messages:
		obj = {}
		obj['content'] = message.content[0].text.value
		obj['role'] = message.role
		thread_messages.append(obj)
	# return thread_messages[::-1]
	return thread_messages


def createMessage(thread_id, message):
	client = OpenAI(api_key=st.secrets["openai_api_key"])
	thread_message = client.beta.threads.messages.create(
							thread_id,
							role="user",
							content=message,)
	return thread_message.id