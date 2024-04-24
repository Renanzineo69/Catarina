import os
import webbrowser
import speech_recognition as sr
import pyttsx3
import re
import math
from datetime import datetime
import locale
import geocoder
import platform
import psutil
import uuid

# Configura o idioma local para português do Brasil
locale.setlocale(locale.LC_TIME, "pt_BR.UTF-8")

# Mapeamento de programas para suas funções correspondentes
def open_web_browser():
    try:
        webbrowser.open("https://www.google.com")  # Abre o navegador padrão
        speak("Abrindo navegador.")
    except Exception as e:
        speak("Não foi possível abrir o navegador.")

program_commands = {
    "calculadora": "calc",
    "navegador": open_web_browser,
    "explorador de arquivos": "explorer",
    "loja": "ms-windows-store:",
    "bloco de notas": "notepad",
}

# Inicializa o mecanismo de texto para fala
engine = pyttsx3.init()

# Função para falar
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Função para ouvir
def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Ouvindo...")
        r.adjust_for_ambient_noise(source)  # Ajusta o nível de ruído do microfone
        
        try:
            audio = r.listen(source, phrase_time_limit=5)  # Limite de tempo para uma frase
            text = r.recognize_google(audio, language='pt-BR')
            print("Você disse:", text)
            return text.lower()  # Retorna o texto em minúsculas
        except sr.UnknownValueError:
            print("Não entendi o que você disse. Por favor, diga ou digite o comando.")
            return input("Comando: ").lower()  # Se não entender, pede para digitar o comando
        except sr.RequestError as e:
            print("Erro ao acessar o serviço de reconhecimento de fala; {0}".format(e))
            return ""

# Função para realizar cálculos matemáticos
def calculate(expression):
    expression = re.sub(r'(\d+)([xX])(\d+)', r'\1*\3', expression)
    # Substitui o texto pela operação correta lidar com conta
    expression = expression.replace("mais", "+")
    expression = expression.replace("menos", "-")
    expression = expression.replace("dividido por", "/")
    expression = expression.replace("vezes" and "x", "*")
    expression = expression.replace("elevado a", "**")

    if "a raiz quadrada de" in expression:
        expression = expression.replace("a raiz quadrada de", "math.sqrt(") + ")"  # Adiciona os parênteses para a função math.sqrt
    try:
        result = eval(expression)
        return result
    except Exception as e:
        print(f"Erro ao calcular a expressão: {str(e)}")
        return None

# Função para obter a data atual
def get_current_date():
    now = datetime.now()
    return now.strftime("%d de %B de %Y")  # Formato: dia/mês/ano 

# Função para obter a hora atual
def get_current_time():
    now = datetime.now()
    return now.strftime("%H:%M")  # Formato: hora:minuto 

# Função para obter o local atual
def get_current_location():
    location = geocoder.ip('me')
    return location.address

# Função para obter informações sobre o sistema
def get_system_info():
    # Nome do usuário
    username = os.getlogin()
    
    # Endereço IP da máquina
    ip = geocoder.ip('me').ip
    
    # Endereço MAC da máquina
    mac = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
    
    # Porcentagem de uso da CPU (que também pode conter a temperatura em alguns sistemas)
    cpu_percent = psutil.cpu_percent(interval=1)
    
    return username, ip, mac, cpu_percent

# Função para abrir programas utilizando o mapeamento ou diretamente
def open_program(program_name):
    if program_name in program_commands:
        command = program_commands[program_name]
        if callable(command):
            command()  # Chama a função correspondente
        else:
            try:
                os.system(f"start {command}")  # Tenta executar o programa do mapeamento
                speak(f"Abrindo {program_name}")  # Diz o que está sendo aberto
            except Exception as e:
                speak("Não foi possível executar essa tarefa.")
    else:
        try:
            os.system(f"start {program_name}")  # Tenta executar o programa diretamente
            speak(f"Abrindo {program_name}")  # Diz o que está sendo aberto
        except Exception as e:
            speak("Não foi possível executar essa tarefa.")

# Função para lidar com comandos especiais
def handle_special_commands(command):
    if "que dia é hoje" in command:
        current_date = get_current_date()
        print("Data atual:", current_date)  # Mostra a data atual no console
        speak(f"Hoje é {current_date}")
    elif "que horas são" in command:
        current_time = get_current_time()
        print("Hora atual:", current_time)  # Mostra a hora atual no console
        speak(f"Agora são {current_time} horas")
    elif "onde estou" in command:
        current_location = get_current_location()
        print("Local atual:", current_location)  # Mostra o local atual no console
        speak(f"Você está em {current_location}")
    elif "desligar" in command:
        speak("Até logo!")
        exit()  # Sai do programa
    elif "quem é você" in command:
        speak("Eu sou uma versão simplificada de um assistente de voz, feita por ninguém mais ninguém menos que o grande e admirável Renan.")
        print("Eu sou uma versão simplificada de um assistente de voz, feita por ninguém mais ninguém menos que o grande e admirável Renan")
    elif "informações sobre o sistema" in command:
        username, ip, mac, cpu_temp = get_system_info()
        print(f"Nome do usuário: {username}")
        speak(f"Nome do usuário: {username}")
        print(f"Endereço IP: {ip}")
        speak(f"Endereço IP: {ip}")
        print(f"Endereço MAC: {mac}")
        speak(f"Endereço MAC: {mac}")
        print(f"Porcentagem de uso da CPU: {cpu_temp}%")
        speak(f"Porcentagem de uso da CPU: {cpu_temp}%")
    else:
        speak("Desculpe, não entendi seu comando.")

# Função para abrir um link no YouTube (José)
def open_youtube_link():
    youtube_link = "https://youtu.be/TsG1KnXUtVA"  # Link do YouTube
    try:
        webbrowser.open(youtube_link)
        speak("Executando modo José")
    except Exception as e:
        speak("Não foi possível abrir o link no YouTube.")

# Função para abrir um link no Google (João)
def open_google_link():
    google_link = "https://shopee.com.br/search?keyword=roupas%20de%20homem%20basico"  # Link do Google
    try:
        webbrowser.open(google_link)
        speak("Executando modo João")
    except Exception as e:
        speak("Não foi possível abrir o link no Google.")
        
# Função para abrir o outro link no Google (Matheus)
def open_google_link2():
    google_link = "https://www.drogaraia.com.br/search?w=tadalafila"  # Link do Google
    try:
        webbrowser.open(google_link)
        speak("Executando modo Matheus")
    except Exception as e:
        speak("Não foi possível abrir o link no Google.")
        
# Função para abrir o link de divulgação
def open_divulgation_link():
    google_link = "https://github.com/Renanzineo69/Catarina"  # Link do Google
    try:
        webbrowser.open(google_link)
        speak("Executando modo Matheus")
    except Exception as e:
        speak("Não foi possível abrir o link no Google.")

# Função para realizar uma pesquisa no Google
def search_google(query):
    try:
        google_search_url = f"https://www.google.com/search?q={query}"
        webbrowser.open(google_search_url)
        speak(f"Realizando uma pesquisa no Google sobre {query}")
    except Exception as e:
        speak("Não foi possível realizar a pesquisa no Google.")

# Variável para armazenar o nome da assistente
assistant_name = "catarina"

# Função para configurar o nome da assistente
def set_assistant_name():
    global assistant_name
    new_name = input("Qual nome você gostaria de atribuir à assistente? (Deixe em branco para manter o nome padrão 'catarina'): ")
    if new_name.strip():
        assistant_name = new_name.strip()
        speak(f"Olá! Meu novo nome é {assistant_name}. Estou ouvindo, Como posso ajudar?")
    else:
        speak(f"Olá! Meu nome continua sendo {assistant_name}. Estou ouvindo, Como posso ajudar?")

# Função principal
def main():
    while True:
        command = listen()

        if assistant_name in command:
            command = command.replace(assistant_name, "").strip()  # Remove o nome da assistente da frase

            if "executar modo josé" in command:
                open_youtube_link()  # Abre o link do YouTube
            elif "executar modo joão" in command:
                open_google_link()  # Abre o link do Google
            elif "executar modo matheus" in command:
                open_google_link2() #Abre o outro link do Google
            elif "executar modo divulgação" in command:
                open_divulgation_link() #Abre o link de divulgação da assistente virtual
            elif "pesquisar" in command:
                query = command.split("pesquisar", 1)[1].strip()  # Extrai a consulta após "pesquisar"
                search_google(query)  # Realiza a pesquisa no Google
            elif "abrir" in command:
                program_name = command.split("abrir", 1)[1].strip()  # Extrai o nome do programa após "abrir"
                open_program(program_name)  # Chama a função para abrir o programa
            else:
                if "quanto é" in command:
                    expression = command.split("quanto é", 1)[1].strip()  # Extrai a expressão a ser calculada
                    result = calculate(expression)
                    
                    if result is not None:
                        print("Resultado:", result)  # Mostra o resultado no console
                        speak(f"O resultado é {result}")
                    else:
                        speak("Não foi possível calcular a expressão.")
                else:
                    handle_special_commands(command)
        else:
            speak(f"Por favor, me chame pelo meu nome '{assistant_name}' para executar comandos.")

# Seção para configurar o nome da assistente
set_assistant_name()

# Inicia a função principal
if __name__ == "__main__":
    main()
