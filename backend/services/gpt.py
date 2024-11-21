from openai import AsyncOpenAI

from utils.config import (
    get_openai_api_key,
    get_openai_assistant_id,
    get_openai_thread_id,
)

client = None
API_KEY = get_openai_api_key()
ASSISTANT_ID = get_openai_assistant_id()
THREAD_ID = get_openai_thread_id()


def get_client() -> AsyncOpenAI:
    global client
    if client is None:
        if not API_KEY:
            raise RuntimeError("API_KEYが設定されていません")
        AsyncOpenAI.api_key = API_KEY
        client = AsyncOpenAI()
    return client


async def create_new_thread_id() -> str:
    client = get_client()
    thread = await client.beta.threads.create()
    return thread.id


async def delete_thread_id(thread_id: str):
    client = get_client()
    await client.beta.threads.delete(thread_id)


async def generate_text(prompt: str, thread_id: str = THREAD_ID) -> str:
    client = get_client()
    await client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=prompt,
    )

    run = await client.beta.threads.runs.create_and_poll(
        thread_id=thread_id,
        assistant_id=ASSISTANT_ID,
    )

    messages = await client.beta.threads.messages.list(
        thread_id=thread_id, run_id=run.id
    )
    message_content = messages.data[0].content[0].text
    annotations = message_content.annotations
    citations = []

    for index, annotation in enumerate(annotations):
        message_content.value = message_content.value.replace(
            annotation.text, f"[{index}]"
        )

        if file_citation := getattr(annotation, "file_citation", None):
            cited_file = client.files.retrieve(file_citation.file_id)
            citations.append(f"[{index}] {cited_file.filename}")

    return message_content.value