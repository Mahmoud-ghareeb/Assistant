import gradio as gr
import hashlib
import os
import shutil
import yaml
import io

from src.assistant import Assistant, load_and_embedd, encode, create_memory, Args
from src.schema import Message

assistant = Assistant()
args = Args()

embeddings = encode(model_id=args.model_id['multilingual-e5-base'], device="cpu", use_open_ai=True)
memory = create_memory(args.k)
config = yaml.load(open('configs/config.default.yaml', 'r'), Loader=yaml.FullLoader)

assistant.g_vars['embedding'] = embeddings
assistant.g_vars['dp'] = ''
assistant.g_vars['memory'] = memory
assistant.g_vars['config'] = config


def upload_pdf(file):
    """Handle PDF upload and save it in a folder."""
    documents_folder = "files"
    print(file.name)
    # # Ensure the folder exists
    # if not os.path.exists(documents_folder):
    #     os.makedirs(documents_folder)

    # # Generate a unique hash for the file
    # hash_text = hashlib.sha1(file.name.encode("UTF-8")).hexdigest()
    # file_location = os.path.join(documents_folder, f"{hash_text}.pdf")

    # # Wrap the file content in a file-like object if needed
    # if not hasattr(file, "read"):  # If file is a NamedString
    #     file = io.BytesIO(file)

    # # Save the uploaded file to the specified location
    # with open(file_location, "wb") as buffer:
    #     shutil.copyfileobj(file, buffer)

    # return f"File successfully saved to: {file_location}"


def upload_file(file):
    """Handle file upload and create embeddings for the uploaded file."""
    print("hi")
    # documents_folder = "files"
    # if not os.path.exists(documents_folder):
    #     os.makedirs(documents_folder)

    # # Generate a unique name using a hash
    hash_text = hashlib.sha1(file.name.encode("UTF-8")).hexdigest()
    # file_location = os.path.join(documents_folder, f"{hash_text}.pdf")

    # # Save the uploaded file to the specified location
    # with open(file_location, "wb") as buffer:
    #     shutil.copyfileobj(file, buffer)

    # # name = f'{hash_text}.pdf'

    assistant.g_vars['dp'] = load_and_embedd(
        file.name, assistant.g_vars['embedding'], hash_text)

    return {"filename": file.name}

def chat_with_assistant(message, hi):
    """Handle chat messages and get responses from the assistant."""
    response = assistant.stream_text(message)
    return response

def generate(
    message: str,
    chat_history: list[dict],
):
    print(message)
    output = ""
    for character in message:
        output += character
        yield output


# Create Gradio interface
with gr.Blocks() as app:
    with gr.Tab("File Upload"):
        gr.Markdown("### Upload a file for embedding and processing")
        pdf_input = gr.File(label="Select PDF File", file_types=[".pdf"])
        upload_button = gr.Button("Upload PDF")
        response_output = gr.Textbox(label="Server Response", interactive=False)
        upload_button.click(upload_file, inputs=[pdf_input], outputs=[response_output])

    
    with gr.Tab("Chat with Assistant"):
        gr.ChatInterface(
            fn=generate,
            examples=[
                "Hey",
                "Can you explain briefly to me what is the Python programming language?",
            ],
            fill_height=True,
            fill_width=True,
            cache_examples=True,
            cache_mode="eager",
            type="messages"
        )

if __name__ == "__main__":
    app.launch()
