from src.assistant import Assistant
from src.assistant import load_and_embedd
from src.assistant import encode
from src.assistant import create_memory
from src.assistant import Args

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse
from contextlib import asynccontextmanager
from src.schema import Message
import shutil
import yaml
import hashlib
import os


assistant = Assistant()
args = Args()


@asynccontextmanager
async def lifespan(app: FastAPI):
    embeddings = encode(model_id="", device="cpu", use_open_ai=True)
    memory = create_memory(args.k)
    config = yaml.load(open('configs/config.default.yaml',
                       'r'), Loader=yaml.FullLoader)

    assistant.g_vars['embedding'] = embeddings
    assistant.g_vars['dp'] = ''
    assistant.g_vars['memory'] = memory
    assistant.g_vars['config'] = config
    yield
    assistant.g_vars.clear()


app = FastAPI(lifespan=lifespan)


@app.post("/")
async def create_upload_file(file: UploadFile = File(...)):
    """ Create embedding of the uploaded file

    :param file: the uploaded file should be (.docs, .pdf)
    """

    documents_folder = "files"
    if not os.path.exists(documents_folder):
        os.makedirs(documents_folder)

    file_location = f"{documents_folder}/{file.filename}"
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    name = file.filename

    hash_text = hashlib.sha1(name.encode("UTF-8")).hexdigest()

    assistant.g_vars['dp'] = load_and_embedd(
        file_location, assistant.g_vars['embedding'], hash_text)

    return {"filename": file.filename, "location": file_location}


@app.post("/text")
async def message(message: Message):

    return StreamingResponse(assistant.stream_text(message.message), media_type="text/plain")