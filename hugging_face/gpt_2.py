from transformers import pipeline

generator = pipeline("text-generation", model="gpt2", device="mps")
output = generator("The future of AI is", max_new_tokens=30)

print(output[0]["generated_text"])


