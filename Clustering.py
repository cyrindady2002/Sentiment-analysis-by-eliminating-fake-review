import requests

API_URL = "https://api-inference.huggingface.co/models/dima806/ai-generated-essay-detection-distilbert"
headers = {"Authorization": f"Bearer {"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"}"}

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()
	
output = query({
	"inputs": "It is a nice day.",
})

print(output[0][0])