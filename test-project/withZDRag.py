
import os
import numpy as np
import requests
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

load_dotenv()

# ======================
# 1. INIT EMBEDDING MODEL (FREE LOCAL)
# ======================
embed_model = SentenceTransformer("all-MiniLM-L6-v2")

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

# ======================
# 4. GET EMBEDDING
# ======================
def get_embedding(text):
    return embed_model.encode(text)

# ======================
# 5. COSINE SIMILARITY
# ======================
def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# ======================
# 6. PARAGRAPH EMBEDDINGS
# ======================
paragraph_embeddings = [get_embedding(p) for p in paragraphs]

# ======================
# 7. USER QUERY
# ======================
query = input("Ask a question: ")
query_embedding = get_embedding(query)

# ======================
# 8. RETRIEVAL
# ======================
scores = []

for i, emb in enumerate(paragraph_embeddings):
    score = cosine_similarity(query_embedding, emb)
    scores.append(score)
    print(f"Paragraph {i} similarity: {score:.4f}")

best_index = int(np.argmax(scores))
best_context = paragraphs[best_index]

print("\nBest match:\n", best_context)

# ======================
# 9. OPENROUTER LLM (ONLY LLM)
# ======================
api_key = os.getenv("OPENROUTER_API_KEY")


prompt = f"""
Use the context below to answer the question.

Context:
{best_context}

Question:
{query}

Answer clearly and simply.
"""

print(prompt)

response = requests.post(
    "https://openrouter.ai/api/v1/chat/completions",
    headers={
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    },
    json={
        "model": "openrouter/free",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }
)

print("\nFINAL ANSWER:\n")
print(response.json())
print(response.json()["choices"][0]["message"]["content"])














































































































# from dotenv import load_dotenv
# import numpy as np
# from openai import OpenAI
# import os


# load_dotenv()



# # ======================
# # 1. INIT CLIENT
# # ======================
# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# # ======================
# # 2. KNOWLEDGE BASE
# # ======================
# text = """
# Machine learning is a subset of artificial intelligence that learns from data.
# Python is widely used in AI, data science, and machine learning.
# Neural networks are inspired by the human brain.
# RAG systems combine retrieval and generation for better AI answers.
# """

# # ======================
# # 3. SPLIT INTO PARAGRAPHS
# # ======================
# paragraphs = [p.strip() for p in text.strip().split("\n") if p.strip()]

# # ======================
# # 4. GET EMBEDDING
# # ======================
# def get_embedding(text):
#     response = client.embeddings.create(
#         model="text-embedding-3-small",
#         input=text
#     )
#     return np.array(response.data[0].embedding)

# # ======================
# # 5. COSINE SIMILARITY
# # ======================
# def cosine_similarity(a, b):
#     return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# # ======================
# # 6. EMBEDDINGS FOR PARAGRAPHS
# # ======================
# paragraph_embeddings = [get_embedding(p) for p in paragraphs]

# # ======================
# # 7. USER QUERY
# # ======================
# query = input("Ask a question: ")
# query_embedding = get_embedding(query)

# # ======================
# # 8. FIND BEST MATCH
# # ======================
# scores = []

# for i, emb in enumerate(paragraph_embeddings):
#     score = cosine_similarity(query_embedding, emb)
#     scores.append(score)
#     print(f"Paragraph {i} similarity: {score:.4f}")

# best_index = int(np.argmax(scores))
# best_context = paragraphs[best_index]

# print("\nBest match:\n", best_context)

# # ======================
# # 9. SEND TO GPT MODEL
# # ======================
# prompt = f"""
# Use the context below to answer the question.

# Context:
# {best_context}

# Question:
# {query}

# Answer clearly and simply.
# """

# response = client.chat.completions.create(
#     model="gpt-4o-mini",
#     messages=[
#         {"role": "user", "content": prompt}
#     ]
# )

# print("\nFINAL ANSWER:\n")
# print(response.choices[0].message.content)