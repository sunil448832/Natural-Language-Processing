## Introduction

Welcome to the Retriever Augment Generator (RAG) - a simple implementation from scratch. RAG is designed to enhance your data retrieval and conversation experiences effortlessly.

## Installation
```bash
pip install -r requirements.txt
```

## Data Ingestion
To get started with RAG, use the following command to ingest your data:

```bash
python ingest.py --data_path 'data/71763-gale-encyclopedia-of-medicine.-vol.-1.-2nd-ed.pdf'\
                  --vector_database_path 'vector_db'
```

## Chat
Engage in interactive conversations with RAG using this command:

```bash
python chat.py --vector_database_path 'vector_db'
```

Enhance your data retrieval and conversation capabilities with RAG today!