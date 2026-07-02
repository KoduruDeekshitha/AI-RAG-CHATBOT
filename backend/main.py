from fastapi import FastAPI,UploadFile,File,Form
import shutil
import os
from typing import Optional
import json
from backend.email_extractor import extract_emails
from fastapi import HTTPException
from backend.email_ai import generate_email
from backend.email_service import send_email
from fastapi.middleware.cors import CORSMiddleware
from backend.vector_store import client
from backend.vector_store import delete_file,collection
from backend.rag import ask_rag
from backend.search import retrieve_chunks
from backend.vector_store import store_embeddings
from backend.embedding import create_embeddings
from backend.pdf_reader import extract_text
from backend.chunker import split_text
app=FastAPI()
app.add_middleware(
    CORSMiddleware,allow_origins=["*"],allow_credentials=True,allow_methods=["*"],allow_headers=["*"],
)
Upload_folder="uploads"
os.makedirs(Upload_folder,exist_ok=True)
@app.get("/")
def home():
    return{
        "message":"Welcome to AI RAG Chatbot"
    }
@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    print("Upload started")

    file_path = os.path.join(Upload_folder, file.filename)
    print(file_path)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    print("File saved")

    text = extract_text(file_path)
    print("Text extracted")

    chunks = split_text(text)
    print("Chunks:", len(chunks))

    embeddings = create_embeddings(chunks)
    print("Embeddings created")

    stored = store_embeddings(chunks, embeddings, file.filename)
    print("Stored")
@app.post("/ask")
async def ask(
    question: str = Form(...),
    filenames: str = Form(...)
):
    try:
        files = json.loads(filenames)

        answer = ask_rag(question, files)
        return {
            "question": question,
            "answer": answer
        }

    except Exception as e:
        import traceback
        traceback.print_exc()

        return {
            "error": str(e)
        }
@app.get("/files")
def get_uploaded_files():
    files=os.listdir(Upload_folder)
    return{
        "total_files":len(files),
        "files":files
    }
@app.delete("/delete")
def delete_uploaded_file(filename:str):
    file_path=os.path.join(Upload_folder,filename)
    deleted_chunks=delete_file(filename)
    if os.path.exists(file_path):
        os.remove(file_path)
    return{
        "message":"file deleted successfully.",
        "deleted_chunks":deleted_chunks
    }
@app.get("/database")
def database():
    data=collection.get()
    return {
        "ids":data.get("ids",[]),
        "documnets":data.get("documents",[]),
        "metadatas":data.get("metadatas",[])
    }
@app.delete("/clear")
def clear_database():
    global collection
    client.delete_collection("documents")
    client.get_or_create_collection(name="documents")
    return{"message":"Database cleared"}
@app.post("/send-email-ai")
def send_ai_email(
    receiver: str = Form(...),
    prompt: str = Form(...)
):
    try:
        email = generate_email(prompt)
        result = send_email(
            receiver,
            "AI Generated Email",
            email
        )
        return {
            "message": "Email accepted by Resend.",
            "id": result["id"]
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
@app.post("/bulk-email")
async def bulk_email(
    file: UploadFile = File(...),
    prompt: str = Form(...)
):
    try:
        file_path = os.path.join(Upload_folder, file.filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        emails = extract_emails(file_path)

        print("Emails:", emails)

        email_body = generate_email(prompt)

        sent = []
        failed = []

        for email in emails:
            try:
                result = send_email(
                    email,
                    "AI GENERATED EMAIL",
                    email_body
                )
                print(result)
                sent.append(email)

            except Exception as e:
                print("Send Error:", e)
                failed.append(email)

        return {
            "total": len(emails),
            "sent": sent,
            "failed": failed
        }

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))