import os
import numpy as np
import requests
import pickle
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

load_dotenv()

# ======================
# 1. INIT EMBEDDING MODEL
# ======================
print("Loading embedding model...")
embed_model = SentenceTransformer("all-MiniLM-L6-v2")
print("Model loaded!\n")

# ======================
# 2. KNOWLEDGE BASE
# ======================
text = """
Machine learning is a subset of artificial intelligence that learns from data.
Python is widely used in AI, data science, and machine learning.
Neural networks are inspired by the human brain.
RAG systems combine retrieval and generation for better AI answers.
"""

# ======================
# 3. SPLIT INTO PARAGRAPHS
# ======================
paragraphs = [p.strip() for p in text.strip().split("\n") if p.strip()]

print(f"📚 Loaded {len(paragraphs)} paragraphs:")
for i, p in enumerate(paragraphs):
    print(f"   {i}: {p[:60]}...")

# ======================
# 4. CREATE EMBEDDINGS (LOOP METHOD - ACCURATE)
# ======================
print("\n🔢 Creating embeddings (one by one for accuracy)...")
paragraph_embeddings = [embed_model.encode(p, normalize_embeddings=True) for p in paragraphs]
print(f"✅ Created {len(paragraph_embeddings)} embeddings")
print(f"   Embedding dimension: {paragraph_embeddings[0].shape[0]}\n")

# ======================
# 5. COSINE SIMILARITY (Optimized for normalized vectors)
# ======================
def cosine_similarity(a, b):
    # Since we used normalize_embeddings=True, dot product = cosine similarity
    return np.dot(a, b)

# ======================
# 6. CACHE EMBEDDINGS (Optional - for faster future runs)
# ======================
CACHE_FILE = "paragraph_embeddings_cache.pkl"

# Save to cache
with open(CACHE_FILE, 'wb') as f:
    pickle.dump({
        'paragraphs': paragraphs,
        'embeddings': paragraph_embeddings
    }, f)
print(f"💾 Cached embeddings to {CACHE_FILE}\n")

# ======================
# 7. MAIN CHAT LOOP
# ======================
api_key = os.getenv("OPENROUTER_API_KEY")

if not api_key:
    print("⚠️  OPENROUTER_API_KEY not found in .env file")
    api_key = input("Enter your OpenRouter API key: ")

print("\n" + "="*50)
print("💬 RAG CHATBOT READY")
print("="*50)

while True:
    # Get user query
    query = input("\n❓ Ask a question (or 'quit' to exit): ").strip()
    
    if query.lower() in ['quit', 'exit', 'q']:
        print("Goodbye! 👋")
        break
    
    if not query:
        print("Please enter a question.")
        continue
    
    # Encode query (normalize for cosine similarity)
    print("🔍 Finding relevant context...")
    query_embedding = embed_model.encode(query, normalize_embeddings=True)
    
    # Calculate similarities with all paragraphs
    scores = []
    for i, emb in enumerate(paragraph_embeddings):
        score = cosine_similarity(query_embedding, emb)
        scores.append(score)
        print(f"   Paragraph {i}: {score:.4f} - {paragraphs[i][:40]}...")
    
    # Get best matching paragraph
    best_index = np.argmax(scores)
    best_score = scores[best_index]
    best_context = paragraphs[best_index]
    
    print(f"\n📖 Best match (score: {best_score:.4f}):")
    print(f"   {best_context}")
    
    # Prepare prompt for LLM
    prompt = f"""Use ONLY the context below to answer the question.

Context: {best_context}

Question: {query}

Answer clearly and concisely based ONLY on the context above. If the context doesn't contain the answer, say so."""

    print("\n🤖 Generating answer...")
    
    try:
        # Call OpenRouter API
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "openrouter/free",
                "messages": [
                    {"role": "system", "content": "You are a helpful assistant that answers questions based only on the provided context."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.3,
                "max_tokens": 500
            },
            timeout=30
        )
        
        if response.status_code == 200:
            answer = response.json()["choices"][0]["message"]["content"]
            print(f"\n✨ ANSWER:\n{answer}")
        else:
            print(f"\n❌ API Error: {response.status_code}")
            print(response.text)
            
    except requests.exceptions.Timeout:
        print("\n❌ Request timed out. Please try again.")
    except Exception as e:
        print(f"\n❌ Error: {e}")

print("\n🎉 Session ended!")




















# import os
# import numpy as np
# import requests
# import pickle
# import torch
# from dotenv import load_dotenv
# from sentence_transformers import SentenceTransformer

# load_dotenv()

# # ======================
# # CONFIGURATION
# # ======================
# CACHE_DIR = "rag_cache"
# os.makedirs(CACHE_DIR, exist_ok=True)

# EMBEDDINGS_CACHE = os.path.join(CACHE_DIR, "embeddings.npy")
# PARAGRAPHS_CACHE = os.path.join(CACHE_DIR, "paragraphs.pkl")
# MODEL_CACHE = os.path.join(CACHE_DIR, "model.pkl")

# # Knowledge base
# text = """
# Machine learning is a subset of artificial intelligence that learns from data.
# Python is widely used in AI, data science, and machine learning.
# Neural networks are inspired by the human brain.
# RAG systems combine retrieval and generation for better AI answers.
# """

# paragraphs = [p.strip() for p in text.strip().split("\n") if p.strip()]

# # ======================
# # PRE-CACHE ALL EMBEDDINGS
# # ======================
# def precompute_everything():
#     """Pre-compute and cache everything on first run"""
    
#     # Check if everything is cached
#     if os.path.exists(EMBEDDINGS_CACHE) and os.path.exists(PARAGRAPHS_CACHE):
#         print("✅ ALL CACHED DATA FOUND! Loading instantly...")
        
#         # Load cached embeddings
#         paragraph_embeddings = np.load(EMBEDDINGS_CACHE)
        
#         # Load cached paragraphs
#         with open(PARAGRAPHS_CACHE, 'rb') as f:
#             cached_paragraphs = pickle.load(f)
        
#         # Load cached model (if using GPU)
#         if os.path.exists(MODEL_CACHE):
#             with open(MODEL_CACHE, 'rb') as f:
#                 model_state = pickle.load(f)
        
#         return paragraph_embeddings, cached_paragraphs, True
    
#     # First run - compute everything
#     print("🔄 FIRST RUN - Pre-computing and caching everything...")
    
#     # Load model
#     model = SentenceTransformer("all-MiniLM-L6-v2")
    
#     # Compute embeddings
#     paragraph_embeddings = model.encode(paragraphs)
    
#     # Save to cache
#     np.save(EMBEDDINGS_CACHE, paragraph_embeddings)
    
#     with open(PARAGRAPHS_CACHE, 'wb') as f:
#         pickle.dump(paragraphs, f)
    
#     # Cache model state (optional)
#     with open(MODEL_CACHE, 'wb') as f:
#         pickle.dump(model, f)
    
#     print(f"✅ Cached {len(paragraph_embeddings)} embeddings")
#     print(f"💾 Cache location: {CACHE_DIR}")
    
#     return paragraph_embeddings, paragraphs, False

# # Load everything
# paragraph_embeddings, paragraphs, from_cache = precompute_everything()

# # ======================
# # LOAD MODEL ONCE (for queries)
# # ======================
# print("🔄 Loading model into memory...")
# model = SentenceTransformer("all-MiniLM-L6-v2")
# print("✅ Model ready!\n")

# # ======================
# # UTILITY FUNCTIONS
# # ======================
# def cosine_similarity(a, b):
#     return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# def retrieve_context(query):
#     query_embedding = model.encode(query)
#     scores = [cosine_similarity(query_embedding, emb) for emb in paragraph_embeddings]
#     best_idx = np.argmax(scores)
#     return paragraphs[best_idx], scores[best_idx]

# # ======================
# # API SETUP
# # ======================
# api_key = os.getenv("OPENROUTER_API_KEY")

# # ======================
# # CHAT LOOP (ULTRA FAST)
# # ======================
# print("="*50)
# print("🚀 ULTRA-FAST RAG CHATBOT READY")
# print(f"📦 Cache status: {'INSTANT LOAD' if from_cache else 'FRESH CACHE'}")
# print("="*50)

# while True:
#     query = input("\n💬 You: ").strip()
    
#     if query.lower() in ['quit', 'exit', 'q']:
#         print("Goodbye! 👋")
#         break
    
#     if not query:
#         continue
    
#     # Retrieve context (uses cached embeddings!)
#     context, score = retrieve_context(query)
    
#     print(f"📚 Found context (score: {score:.3f}): {context[:80]}...")
    
#     # Generate response
#     response = requests.post(
#         "https://openrouter.ai/api/v1/chat/completions",
#         headers={
#             "Authorization": f"Bearer {api_key}",
#             "Content-Type": "application/json"
#         },
#         json={
#             "model": "openrouter/free",
#             "messages": [{"role": "user", "content": f"Context: {context}\n\nQuestion: {query}\n\nAnswer concisely:"}]
#         }
#     )
    
#     answer = response.json()["choices"][0]["message"]["content"]
#     print(f"🤖 Bot: {answer}\n")