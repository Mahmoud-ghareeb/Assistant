# Assistant

## Overview

This application allows users to interact with a chatbot powered by a custom assistant. It uses **Chainlit** for the chat interface, **OpenAI API** for processing, and provides functionality for processing PDF files. Users can upload a PDF file, and the assistant will process its content, embed it for memory, store it in vector DB and respond to user messages based on the file content.

## Features

- **File Upload**: Users can upload a PDF file that the assistant will process.
- **Text Embedding & Memory**: The assistant processes the content of the uploaded file and embeds it into memory for future reference.
- **Real-time Chat**: The assistant can answer questions based on the contents of the uploaded file.
- **Streaming Responses**: The assistant streams responses token by token for a dynamic chat experience.

## Project Structure

```
/project-root
    |── configs
    │   ├── config.default.yaml  # Contains configuration settings (e.g., system propmt)
    |── files                    # Directory to store uploaded files
    │   ├── pdf files to test the app 
    ├── /src  
    │   ├── /assistant.py          # Assistant main class
    │   ├── /schema.py            # Contains message schema definitions
    │   ├── /embedding.py         # Embedding logic, splitting text and creating vector DB
    │   ├── /args.py              # Contains the Arguments
    │   ├── /memory.py            # Logic for file handling the memory
    ├── /app.py                   # contain the chainlit app logic
    ├── /requirements.txt         # Project dependencies
    └── /README.md                # This file

```

### Installation Guide

1. Clone the repo
```shell
git clone https://github.com/Mahmoud-ghareeb/Assistant.git
``` 

1. Create Python Environment
```shell
conda create --name assistant python==3.12
```

2. Activate the environment
```shell
conda activate assistant
```

3. install the requirments
```shell
pip install -r requirements.txt
```

4. Rename .env.example to .env and add the secret keys of 
    - openai


### Running The APP

To Start The Chat GUI
```shell
chainlit run app.py -w
```


