from sentence_transformers import CrossEncoder

class ReRanker:
    def __init__(self):
        self.model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

    def rerank(self, question: str, chunks: list, top_k: int = 5):
        pairs = [(question, c["text"]) for c in chunks]
        scores = self.model.predict(pairs)

        ranked = sorted(
            zip(chunks, scores),
            key=lambda x: x[1],
            reverse=True
        )

        return [item[0] for item in ranked[:top_k]]
