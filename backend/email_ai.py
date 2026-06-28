from backend.llm import generate_answer
def generate_email(prompt):
    email_prompt=f""" You are a professional email writer. GEnerate ONly the email. Keep it professional
     you have to write an email to the candidates for interview to be prepared  . 
    User Request:{prompt} Email:"""
    return generate_answer(email_prompt)