import subprocess
import time

# Start the Ollama server in the background
subprocess.Popen(["ollama", "serve"]) # Runs on http://localhost:11434

# Give the server a few seconds to initialize
time.sleep(5)
print("Ollama server is running!")
