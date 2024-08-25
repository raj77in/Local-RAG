#!/usr/bin/env python

import os
import time
import streamlit as st
from langchain.chains import RetrievalQA
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.llms import Ollama
from constants import CHROMA_SETTINGS
from pprint import pprint
import json

st.set_page_config(page_title="Amit Agarwal's RAG", layout="wide")

# Initialize the model and database
model = os.environ.get("MODEL", "phi3")
embeddings_model_name = os.environ.get("EMBEDDINGS_MODEL_NAME", "all-MPnet-base-v2")
persist_directory = os.environ.get("PERSIST_DIRECTORY", "db")
target_source_chunks = st.slider("Number of Documents to Retrieve (top_k)", 1, 50, 15)


def get_all_docs():
    print(db.get().keys())
    all_data=[]

    docs = db.get()['metadatas']

    for x in docs:
        all_data.append(x['source'])

    return set(all_data)


embeddings = HuggingFaceEmbeddings(model_name=embeddings_model_name)
db = Chroma(persist_directory=persist_directory, embedding_function=embeddings)
retriever = db.as_retriever(search_kwargs={"k": target_source_chunks})
llm = Ollama(model=model)
qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever, return_source_documents=True)

# Initialize Streamlit session state
if 'history' not in st.session_state:
    st.session_state['history'] = []

def main():
    # Input query
    query = st.text_input("Your Question:")
    hide_source = st.checkbox("Hide source documents")
    # print (hide_source)

    # List loaded documents
    if st.button("List Loaded Documents"):
        st.write("### Loaded Documents:")
        count=1
        for doc in get_all_docs():
            st.write(f"**Source:** {count}) {doc}")
            count = count + 1

    # Submit query
    if st.button("Submit"):
        if query.strip() == "":
            st.warning("Query cannot be empty")
        else:
            with st.spinner("Processing..."):
                start = time.time()
                res = qa(query)
                answer, docs = res['result'], [] if hide_source else res['source_documents']
                end = time.time()

            # Update history
            st.session_state['history'].append({"query": query, "answer": answer, "time_taken": end - start, "docs": docs})

            st.write(f"**Question:** {query}")
            st.write(f"**Answer:** {answer}")
            st.write(f"**Time Taken:** {end - start:.2f} seconds")

            if not hide_source:
                st.write("**Sources:**")
                for document in docs:
                    st.write(f"> **{document.metadata['source']}**:")
                    st.write(document.page_content)

    # Display query history
    st.write("### Query History:")
    for item in st.session_state['history']:
        st.write(f"**Question:** {item['query']}")
        st.write(f"**Answer:** {item['answer']}")
        st.write(f"**Time Taken:** {item['time_taken']:.2f} seconds")
        if not hide_source:
            st.write("**Sources:**")
            for document in item['docs']:
                st.write(f"> **{document.metadata['source']}**:")
                st.write(document.page_content)

if __name__ == "__main__":
    main()

