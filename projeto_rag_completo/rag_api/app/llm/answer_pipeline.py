from app.search.hybrid_search import hybrid_search
from app.llm.prompts import CORPORATE_PROMPT_TEMPLATE
from app.llm.context_builder import build_context
from app.llm.llama_client import LlamaClient
from app.reranking.reranking import ReRanker


CONFIDENCE_THRESHOLD = 0.70


def answer_question(question: str) -> dict:
    results = hybrid_search(question)

    if not results:
        return _no_answer()

    

    best_score = results[0]["score"]

    if best_score < CONFIDENCE_THRESHOLD:
        return _no_answer(best_score)

    reranker = ReRanker()

    reranked = reranker.rerank(question, results, top_k=5)


    context = build_context(results)

    prompt = CORPORATE_PROMPT_TEMPLATE.format(
        context=context,
        question=question
    )

    llm = LlamaClient(
        model="llama-3.3-70b-versatile",
        temperature=0.0
    )

    answer = llm.generate(prompt)

    return {
        "answer": answer,
        "confidence": results[0].get("score", 0.0),
        "sources": results
    }

def _no_answer(score: float = 0.0) -> dict:
    return {
        "answer": "Não há informações suficientes nos documentos para responder a essa pergunta.",
        "confidence": round(score, 2),
        "sources": []
    }