import numpy as np
from sentence_transformers import SentenceTransformer
import torch

# CORRECT PYTHON IMPORT: from filename (without .py) import function_name
from visulizing_embeddings import Vis

# 1. Initialize our model and its internal tokenizer
print("Initializing pipeline...")
model = SentenceTransformer("all-MiniLM-L6-v2")
tokenizer = model.tokenizer

# Let's use your text!
text = "I love tokenization!"
print(f'\nOriginal Text: "{text}"')
print("=" * 50)

# --- STEP 1: TOKENIZATION ---
tokens = tokenizer.tokenize(text)
print(f"Step 1 (Tokens):   {tokens}")

# --- STEP 2: TOKEN TO ID CONVERSION ---
token_ids = tokenizer.convert_tokens_to_ids(tokens)
print(f"Step 2 (Token IDs): {token_ids}")

# --- STEP 3: EMBEDDING EXTRACTION ---
print("=" * 50)
print("Step 3: Extracting vectors from the Matrix...")

with torch.no_grad():
    underlying_model = model[0].auto_model
    embeddings_matrix = underlying_model.get_input_embeddings()
    raw_vectors = embeddings_matrix(torch.tensor([token_ids])).numpy()[0]

# --- STEP 4: VISUALIZE THE RESULT ---
for token, token_id, vector in zip(tokens, token_ids, raw_vectors):
    print(f"\nProcessing Token: '{token}'")
    print(f"  -> Vector Shape: {vector.shape[0]} dimensions")

    # This calls the function imported from visulizing_embeddings.py!
    Vis(token, token_id, vector)

print("=" * 50)
final_sentence_vector = model.encode(text)
print(
    f"Final sentence vector shape: {final_sentence_vector.shape[0]} (Ready for Cosine Similarity!)"
)