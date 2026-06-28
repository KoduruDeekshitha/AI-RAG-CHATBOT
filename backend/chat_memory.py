conversation_history=[]
def add_message(role,message):
    conversation_history.append({
        "role":role,
        "message":message
    })
def get_history():
    history=""
    for item in conversation_history:
        history+=f"{item['role']}:{item['message']}\n"
    return history
def clear_history():
    conversation_history.clear()