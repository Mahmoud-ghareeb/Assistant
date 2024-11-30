import chainlit as cl
import requests
import json
import yaml
import shutil
import hashlib

from src.assistant import Assistant, load_and_embedd, encode, create_memory, Args
from src.schema import Message


assistant = Assistant()
args = Args()


@cl.on_chat_start
async def start_chat():
    files = None
    
    embeddings = encode(model_id=args.model_id['multilingual-e5-base'], device="cpu", use_open_ai=True)
    memory = create_memory(args.k)
    config = yaml.load(open('configs/config.default.yaml', 'r'), Loader=yaml.FullLoader)

    assistant.g_vars['embedding'] = embeddings
    assistant.g_vars['dp'] = ''
    assistant.g_vars['memory'] = memory
    assistant.g_vars['config'] = config

    while files == None:
        files = await cl.AskFileMessage(
            content="Please upload a text file to begin!", accept=["application/pdf"]
        ).send()

    text_file = files[0]
    shutil.copy(text_file.path, f"files/{text_file.name}")
    
    file_location = f"files/{text_file.name}"

    hash_text = hashlib.sha1(text_file.name.encode("UTF-8")).hexdigest()

    assistant.g_vars['dp'] = load_and_embedd(
        file_location, assistant.g_vars['embedding'], hash_text)
    
    await cl.Message(
        content=f"`{text_file.name}` uploaded"
    ).send()


@cl.on_message
async def main(message: cl.Message):

    msg = cl.Message(content="")

    stream = assistant.stream_text(message.content)

    for part in stream:
        if token := part or "":
            await msg.stream_token(token)
    
    await msg.update()