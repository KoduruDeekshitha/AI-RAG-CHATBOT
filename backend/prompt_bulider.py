def build_prompt(question, documents):

    context = "\n\n----------------------------\n\n".join(documents)

    prompt = f"""
You are an AI Resume Assistant.

You are given information extracted from one or more resumes.

Answer ONLY using the information below.

If the question refers to multiple candidates, search ALL resumes before answering.

Never ignore information from later resumes.

If the answer does not exist, reply exactly:

I couldn't find the information.

====================

{context}

====================

Question:
{question}

Answer:
"""

    return prompt
     