import requests
import time

# Set the model to ping (update if needed)
model_name = "llama3.1:70b"

# The Ollama API endpoint for generating queries
ollama_url = f"http://localhost:11434/api/generate"

# Define a simple prompt to keep the model warm
prompt = "Just keeping you warm."

# Interval between pings (in seconds)
ping_interval = 600  # 10 minutes

# Function to ping Ollama
def keep_ollama_warm():
    while True:
        try:
            # Send a POST request to the Ollama API
            response = requests.post(
                ollama_url,
                json={
                    "model": model_name,
                    "prompt": prompt
                }
            )
            
            # Check if the response was successful
            if response.status_code == 200:
                print(f"Ping successful: {response.json()['response']}")
            else:
                print(f"Ping failed with status code: {response.status_code}")
        
        except requests.RequestException as e:
            print(f"Failed to ping Ollama: {e}")
        
        # Sleep for the defined interval before the next ping
        time.sleep(ping_interval)

if __name__ == "__main__":
    print(f"Starting to keep {model_name} warm by pinging every {ping_interval} seconds...")
    keep_ollama_warm()

