def build_prompt(question,documents):
    context="\n\n".join(documents)
    prompt=f"""
    You are an AI assistant.

Answer ONLY from the context provided below.

Rules:
1. Do not use your own knowledge.
2. If the answer is not present in the context, reply exactly:
I couldn't find the information.
3. Keep the answer short and precise."
    context:
    {context}
    question:
    {question}
    answer:
    """
    return prompt
     