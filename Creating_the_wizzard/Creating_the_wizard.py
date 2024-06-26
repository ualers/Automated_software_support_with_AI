
from openai import OpenAI
import os
import time
from telegram.ext import Updater, CommandHandler, JobQueue
from telegram.ext import Updater, CommandHandler, Job
from firebase_admin import credentials, initialize_app, storage
from keys_def import chaves

bot_token, CANAL_ID = chaves.keys_bot_telegram()
key_api = chaves.chaves_open_ai()
client = OpenAI(
    api_key=key_api,
)

### Module creating new assistant ###    
def creating_new_assistant():
    file = client.files.create(
        file=open("doc.csv", "rb"),
        purpose='assistants'
    )
    assistant = client.beta.assistants.create(
        name="Suporte do software", 
        instructions="responda as perguntas feitas com base nas respostas do arquivo  responda somente oque foi perguntado pelos clientes e nao todas as perguntas do arquivo  se o cliente perguntar algo que nao está no arquivo peça desculpas e diga que ainda nao temos respostas.",
        tools=[{"type": "retrieval"}],
        model="gpt-3.5-turbo-1106",
        file_ids=[file.id]
    )
    print([file.id])
    thread = client.beta.threads.create()
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content='''oi''',
        file_ids=[file.id]
    )
    print(thread.id)
    print(assistant.id)
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id,
        instructions="responda as perguntas feitas com base nas respostas do arquivo  responda somente oque foi perguntado pelos clientes e nao todas as perguntas do arquivo  se o cliente perguntar algo que nao está no arquivo peça desculpas e diga que ainda nao temos respostas.",
        tools=[{"type": "retrieval"}],
        model="gpt-3.5-turbo-1106"
    )

    while True:
        run_status = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )
        if run_status.status == 'completed': 
            break
        else:
            print("Aguardando a execução ser completada...")
        time.sleep(2)  
    messages = client.beta.threads.messages.list(
        thread_id=thread.id
    )
    for message in messages:
        for mensagem_contexto in message.content:  
            valor_texto = mensagem_contexto.text.value
            print(valor_texto)
            thread_id = thread.id
            assistant_id = assistant.id
            run_id = run.id
            name = "Assistente"
            diretorio_script = os.path.dirname(os.path.abspath(__file__))
            nome_arquivo_gerenciador = os.path.join(diretorio_script, 'gerenciador_agente_1.txt')
            with open('gerenciador_agente_1.txt', 'a') as arquivo:
                arquivo.write(f'Nome: {name} \n')
                arquivo.write(f'thread_id:{thread_id}\n')
                arquivo.write(f'assistant_id:{assistant_id}\n')
                arquivo.write(f'------------------------\n')
        break






