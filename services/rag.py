import ollama

from services.database import search_chunks
from utils.prompts import PROMPT_TEMPLATE

def ask_question(
    question,
    chat_history,
    selected_file,
    threshold
):

    docs, metadata, distances = search_chunks(
        question,
        chat_history,
        selected_file,
        threshold
    )


    if not docs:

        return (
            "No relevant information found.",
            [],
            [],
            [],
            999,
            "Unknown"
        )
        
    best_distance = min(distances)

    # THRESHOLD = threshold

    if best_distance > threshold:

        return (
            "No relevant information found.",
            [],
            [],
            [],
            best_distance,
            "Unknown"
        )

    context = "\n".join(docs)

    prompt = PROMPT_TEMPLATE.format(
        history=chat_history,
        context=context,
        question=question
    )

    response = ollama.chat(
        model="phi3:mini",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    
    best_distance = min(distances)
    source = metadata[0]["source"]

    return (
        response["message"]["content"],
        docs,
        metadata,
        distances,
        best_distance,
        source
    )