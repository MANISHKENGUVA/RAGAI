import torch
import torch.nn.functional as F
from sentence_transformers import SentenceTransformer

# Load model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Get tokenizer and embedding layer
tokenizer = model.tokenizer
underlying_model = model[0].auto_model
embedding_layer = underlying_model.get_input_embeddings()


def vector_to_word(vector):
    """
    Find the closest vocabulary word to an embedding vector.
    """

    if not isinstance(vector, torch.Tensor):
        vector = torch.tensor(vector, dtype=torch.float32)

    vocab_embeddings = embedding_layer.weight

    similarities = F.cosine_similarity(
        vector.unsqueeze(0),
        vocab_embeddings,
        dim=1
    )

    best_id = torch.argmax(similarities).item()

    word = tokenizer.convert_ids_to_tokens(best_id)

    return word, best_id


def Vis(single_token, single_id, single_vector):
    print("\n" + "=" * 60)
    print(f"Original Token : {single_token}")
    print(f"Original ID    : {single_id}")

    word, word_id = vector_to_word(single_vector)

    print(f"Nearest Word   : {word}")
    print(f"Nearest Word ID: {word_id}")

    print("\nTop 10 closest words:")

    vector = torch.tensor(single_vector, dtype=torch.float32)

    similarities = F.cosine_similarity(
        vector.unsqueeze(0),
        embedding_layer.weight,
        dim=1
    )

    topk = torch.topk(similarities, 10)

    for rank, (idx, score) in enumerate(
        zip(topk.indices, topk.values),
        start=1
    ):
        token = tokenizer.convert_ids_to_tokens(idx.item())
        print(
            f"{rank:2d}. {token:<20} "
            f"(id={idx.item():<6}) "
            f"score={score.item():.4f}"
        )

