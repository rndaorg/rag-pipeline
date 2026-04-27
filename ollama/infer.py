!pip install ollama
import ollama

response = ollama.chat(model='llama3.2', messages=[
  {'role': 'user', 'content': 'Explain quantum physics in one sentence.'},
])
print(response['message']['content'])
