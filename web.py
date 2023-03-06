import gradio as gr
import openai
import config
import subprocess

openai.api_key = config.OPENAI_API_KEY

messages = [
    {"role": "system", "content": "あなたは、ロック・ミュージックの音楽評論家です"}
]

def transcribe(audio):
    global messages

    audio_file= open(audio, "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)

    messages.append({"role": "user", "content": transcript["text"]})
    response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=messages
    )

    system_message = response["choices"][0]["message"]["content"]
    subprocess.call(["say", system_message])

    messages.append({"role": "assistant", "content": system_message})
    print(response)

    chat_transcript = ""
    for message in messages:
        if message['role'] != 'system':
            chat_transcript += message['role'] + ": " + message['content'] + "\n\n"

    return chat_transcript

ui = gr.Interface(fn=transcribe, inputs=gr.Audio(source="microphone", type="filepath"), outputs="text").launch()

ui.launch()
