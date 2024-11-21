import ollama 


question = "What were the iPhone's best new features"
stream = ollama.chat(
  model="llama3.2", stream=True,
  messages = [
    { "role": "user", 'content': f"Question: {question}"}
  ]
)
for chunk in stream:
  print(chunk['message']['content'], end='', flush=True)


