import ollama
import time
def chat_with_model(question):
    stream = ollama.chat(
        model="llama3.2", stream=True,
        messages=[
            {"role": "user", 'content': f"Question: {question}"}
        ]
    )
    for chunk in stream:
        print(chunk['message']['content'], end='', flush=True)

def parse_document(file_path):
    with open(file_path, encoding='utf-8') as file:
        paragraphs= []
        buffer = []
        for line in file.readlines():
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
        
def get_embeddings(chunks):
   return [ 
       ollama.embeddings(
            model="llama3.2",
            prompt=chunk
        )["embedding"]
        for chunk in chunks
    ]

    
    
    

question = "What were the iPhone's best new features"
paragraph =parse_document("contes.txt")
start = time.perf_counter()
print(time.perf_counter()-start)
embeddings = get_embeddings(paragraph[0])
print(len(embeddings))

