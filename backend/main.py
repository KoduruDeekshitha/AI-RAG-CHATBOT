from fastapi import FastAPI,UploadFile,File,Form
import shutil
import os
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
    file_path=os.path.join(Upload_folder,file.filename)
    with open(file_path,"wb") as buffer:
        shutil.copyfileobj(file.file,buffer)
    text=extract_text(file_path)
    chunks=split_text(text)
    embeddings=create_embeddings(chunks)
    stored=store_embeddings(chunks,embeddings,file.filename)
    return {
        "filename":file.filename,
        "number_of_chunks":len(chunks),
        "embedding_dimension":len(embeddings[0]),
        "stored_vectors":stored,
        "message":"embeddings stored successfully."
    }
@app.post("/ask")
async def ask(question:str=Form(...),filename:str=Form(...)):
    answer=ask_rag(question,filename)
    return{
        "question":question,
        "answer":answer
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
def sent_ai_email(receiver:str=Form(...),prompt:str=Form(...)):
    email=generate_email(prompt)
    send_email(receiver,"AI Generated Email",email)
    return {
        "receiver":receiver,
        "email":email,
        "message":"email sent successfully."
    }