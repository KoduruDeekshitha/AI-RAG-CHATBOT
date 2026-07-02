from backend.search import retrieve_chunks
from backend.prompt_bulider import build_prompt
from backend.gemini import generate_answer
from backend.agent import run_agent
from backend.chat_memory import add_message,get_history
from backend.system_prompt import SYSTEM_PROMPT
def ask_rag(question, filenames):

    results = retrieve_chunks(question, filenames)

    print("RESULTS:", results)

    if not results:
        return "No results."

    if "documents" not in results:
        return "No documents key."

    documents = results["documents"][0]

    if not documents:
        return "Please upload a PDF first."

    add_message("User", question)

    history = get_history()

    prompt = build_prompt(
        history + "\nCurrent Question: " + question,
        documents
    )

    answer = run_agent(prompt)

    return answer
def build_prompt(question,documents):
    context="\n\n".join(documents)
    prompt=f""" {SYSTEM_PROMPT}
Use the document context below to answer the users questions.
if the answer is not present in the documnet,reply exactly:
    I couldn't find the information, conversation and current Question:{question}
Document context:{context} answer:  """
    return prompt