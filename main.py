import chainlit as cl
from llm_client.llm_client import LLMProxyChatOpenAI, LLMProxyOpenAIEmbeddings
from config import MODEL_EMBEDDINGS
from io import BytesIO
import os
import reconnaissance_vocale as rv
import wave


def load_system_prompt():
    prompt_path = os.path.join(os.path.dirname(__file__), "prompts", "system_prompt.txt")
    try:
        with open(prompt_path, "r", encoding="utf-8") as f:
            return f.read().strip()
    except FileNotFoundError:
        return "You are a helpful AI assistant."

# Initialize the LLM client
llm = LLMProxyChatOpenAI()
embeddings = LLMProxyOpenAIEmbeddings()
system_prompt = load_system_prompt()

@cl.on_message
async def main(message: cl.Message):
    # Get the conversation history and add system prompt
    messages = [{"role": "system", "content": system_prompt}]
    messages.extend(cl.chat_context.to_openai())
    
    # Call LLM with the full conversation history
    response = await llm.agenerate([messages])
    
    # Send the LLM's response
    await cl.Message(
        content=response.generations[0][0].text,
    ).send()


@cl.on_audio_end
async def on_audio_end(chunk: cl.AudioChunk):
    if chunk.isStart:
        buffer = BytesIO()
        # This is required for whisper to recognize the file type
        buffer.name = f"input_audio.{chunk.mimeType.split('/')[1]}"
        # Initialize the session for a new audio stream
        cl.user_session.set("audio_buffer", buffer)
        cl.user_session.set("audio_mime_type", chunk.mimeType)

    # Write the chunks to a buffer and transcribe the whole audio at the end
    cl.user_session.get("audio_buffer").write(chunk.data)
    with wave.open("fichier_vide.wav", "wb") as wf:
        wf.setnchannels(1)        # Mono (1 canal)
        wf.setsampwidth(2)        # Taille des échantillons : 2 octets (16 bits)
        wf.setframerate(16000)    # Fréquence d'échantillonnage : 16 kHz
        wf.writeframes(chunk.data)
    
    message =  rv.interPreteur("fichier_vide.wav")
    print(f"contenu : {message}")
    
    messages = [{"role": "system", "content": message}]
    messages.extend(cl.chat_context.to_openai())
    
    # Call LLM with the full conversation history
    response = await llm.agenerate([messages])
    
    # Send the LLM's response
    await cl.Message(
        content=response.generations[0][0].text,
    ).send()
    
    