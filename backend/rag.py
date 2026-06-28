from backend.search import retrieve_chunks
from backend.prompt_bulider import build_prompt
from backend.llm import generate_answer
from backend.chat_memory import add_message,get_history
from backend.system_prompt import SYSTEM_PROMPT
def ask_rag(question,filename):
    results=retrieve_chunks(question,filename)
    documents=results["documents"][0]
    if not documents:
        return "please upload a pdf first"
    add_message("User",question)
    history=get_history()
    prompt=build_prompt(history+"\nCurrent Question"+question,documents)
    answer=generate_answer(prompt)
    return answer
def bulid_prompt(question,documents):
    context="\n\n".join(documents)
    prompt=f""" {SYSTEM_PROMPT}
Use the document context below to answer the users questions.
if the answer is not present in the documnet,reply exactly:
    I couldn't find the information, conversation and current Question:{question}
Document context:{context} answer:  """
    return prompt