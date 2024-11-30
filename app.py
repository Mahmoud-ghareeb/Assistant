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
            content="Please upload a text file to begin!", accept=["application/pdf"], max_size_mb=20, max_files=5
        ).send()
        
    hash_text = hashlib.sha1(files[0].name.encode("UTF-8")).hexdigest()
    locations = []
    for file in files:
        shutil.copy(file.path, f"files/{file.name}")
        file_location = f"files/{file.name}"
        locations.append(file_location)

    assistant.g_vars['dp'] = load_and_embedd(
        locations, assistant.g_vars['embedding'], hash_text)
    
    await cl.Message(
        content=f"`files uploaded"
    ).send()


@cl.on_message
async def main(message: cl.Message):

    msg = cl.Message(content="")

    stream = assistant.stream_text(message.content)

    for part in stream:
        if token := part or "":
            await msg.stream_token(token)
            
    # await cl.Message(
    #     content=f"the source of the data is {assistant.sources}"
    # ).send()
    
    await msg.update()