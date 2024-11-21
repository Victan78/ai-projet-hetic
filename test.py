import ollama
import time
import requests
from colorama import Fore, init

init(autoreset=True)

def chat_with_model(question, use_rag=False, paragraphs=None):
    start_time = time.time() 

    if use_rag and paragraphs:
        relevant_passages = retrieve_relevant_passages(question, paragraphs)
        prompt = f"Passages: {relevant_passages}\nQuestion: {question}"
    else:
        prompt = f"Question: {question}"

    stream = ollama.chat(
        model="llama3.2", 
        stream=True,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    for chunk in stream:
        print(chunk['message']['content'], end='', flush=True)
    
    elapsed_time = time.time() - start_time
    print(f"\nTemps de réponse: {elapsed_time:.2f} secondes")

def fetch_file_content(url):
    """Fonction pour lire directement le contenu du fichier depuis l'URL."""
    response = requests.get(url)
    response.raise_for_status()  
    return response.text

def parse_document_from_text(text):
    """Convertit le texte brut en une liste de paragraphes."""
    paragraphs = []
    buffer = []
    for line in text.splitlines():
        line = line.strip()
        if line:
            buffer.append(line)
        else:
            if buffer:
                paragraphs.append(' '.join(buffer))
                buffer = []
    if len(buffer):
        paragraphs.append(' '.join(buffer))
    return paragraphs

def retrieve_relevant_passages(question, paragraphs):
    return paragraphs[:3]

file_url = "https://hetic-project.s3.us-east-1.amazonaws.com/contes.txt"

file_content = fetch_file_content(file_url)

paragraphs = parse_document_from_text(file_content)

question = "Qui est Mohamed Salamatao ?"

print(Fore.RED + "Réponse sans RAG:")
chat_with_model(question, use_rag=False)

print("\n" + Fore.GREEN + "Réponse avec RAG:")
chat_with_model(question, use_rag=True, paragraphs=paragraphs)
