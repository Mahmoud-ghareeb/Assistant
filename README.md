# Assistant

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

5. To run FastAPI Start the app
```shell
uvicorn main:app --port 8080
```
