def build_context(search_results: list, max_chunks: int = 5) -> str:
    context_parts = []

    for result in search_results[:max_chunks]:
        context_parts.append(result["text"])

    return "\n\n---\n\n".join(context_parts)