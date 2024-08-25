# Local-RAG

No API tokens needed (not even OpenAPI), run the RAG from your laptop/desktop/server using any model from HuggingFace.

Inspired by [PromptEngineer48 ollama repo](https://github.com/PromptEngineer48/Ollama). Modified according to my needs.

## How to use/run/install

### Setup Ollama

You can select any method to install [ollama](https://github.com/ollama/ollama). I have used podman with the following commands (using GPU)

```bash
curl -s -L https://nvidia.github.io/libnvidia-container/stable/rpm/nvidia-container-toolkit.repo |   sudo tee /etc/yum.repos.d/nvidia-container-toolkit.repo
# Enable the repos in /etc/yum.repos.d/nvidia-container-toolkit.repo
sudo yum install -y nvidia-container-toolkit
docker run -d --gpus=all -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
```

If you do not have GPU's, you can ignore installing the nvidia container toolkit and run the podman command as follows (without the gpus flag): `docker run -d --gpus=all -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama`

This will ensure that you have the models in a persistent directory (docker volume) at the following path - `~/.local/share/containers/storage/volumes/ollama/_data`, you can check the path with the command : `podman volume inspect ollama`. This is very useful because if you need to update **ollama** without losing your models and data, you can do so. Just follow these steps:

* stop the container 
* remove it 
* Pull again
* start again.

Now, with fun part. Once ollama container is up and running, you will need to pull the LLM model that you wish to use.

First, go to the ollama container : `podman exec -it ollama bash`
Then, in the bash prompt within the ollama container, pull the model you wish to use. I am using [phi2 from Microsoft](https://huggingface.co/microsoft/phi-2) but you are free to change it. If you do change it, read below on how to change it for Retrieval.

### Setup RAG

1. Clone the repository: `git clone https://github.com/raj77in/Local-RAG` and cd to the folder: `cd Local-RAG`.
2. Prepare a virtual environment: `python -m venv .venv`
3. Install the requirements: `pip install -r requirements.txt`
4. Create the folder for source documents: `mkdir source_documents`.

and thats it.

## Note about markdown files

If you intend to ingest markdown files, then you need to follow the below steps:

```python
# Start python interpreter in your virtual envirionment
>>> import nltk
>>> nltk.download('punkt_tab')
>>> nltk.download('averaged_perceptron_tagger_eng')
```

## Add more files

Put any and all your files into the `source_documents` directory

The supported extensions are:

- `.csv`: CSV,
- `.docx`: Word Document,
- `.doc`: Word Document,
- `.enex`: EverNote,
- `.eml`: Email,
- `.epub`: EPub,
- `.html`: HTML File,
- `.md`: Markdown,
- `.msg`: Outlook Message,
- `.odt`: Open Document Text,
- `.pdf`: Portable Document Format (PDF),
- `.pptx` : PowerPoint Document,
- `.ppt` : PowerPoint Document,
- `.txt`: Text file (UTF-8)

To ingest the files, copy the files to **source_documents** folder and run the `ingest.py` script.

Note: you can set `EMBEDDINGS_MODEL_NAME` to select the model that you wish to use for embedding as and environment variablie, for ex: `EMBEDDINGS_MODEL_NAME=all-MPNet-base-v2 python ingest.py`.

## Running the chat application

You will need to run the chat application with `streamlit` application. Again, you can use envirionment variables to change the MODEL and embedding model as shown in example below.

```bash
source .venv/bin/activate
streamlit run app.py

# Another example with llama model
MODEL=llama3 streamlit run app.py
```

## Bonus

Additionally you can setup systemd service to start the streamlit application. An example of systemd service file is provided for reference. Change the folder names and copy to `/etc/systemd/system/` folder. 

* Reload the daemon : `systemd daemon-reload`
* Enable and activate the service: `systemctl enable --now streamlit-rag.service`

## Additional Bonus

If you have free RAM to keep the ollama model running, then you can use the python script `keep_ollama_warm.py` as systemd service or run in cron.

Or, you can use ollama API to achieve the same with following command in cron: `http://localhost:11434/api/generate -d '{"model": "llama3", "keep_alive": -1}'`, change llama3 to model that you want to keep warm.

This steps keeps the model loaded in RAM and hence you will get quicker response.
