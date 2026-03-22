memory_store = {}

def save_memory(user_id, job_role, result):
    if user_id not in memory_store:
        memory_store[user_id] = []

    memory_store[user_id].append({
        "job_role": job_role,
        "result": result
    })


def get_memory(user_id):
    return memory_store.get(user_id, [])