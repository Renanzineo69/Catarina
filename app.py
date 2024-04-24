import os
import webbrowser
import speech_recognition as sr
import pyttsx3
import re
import math
from datetime import datetime
import locale
import geocoder

# Configura o idioma local para português do Brasil
locale.setlocale(locale.LC_TIME, "pt_BR.UTF-8")

# Mapeamento de programas para suas funções correspondentes
program_commands = {
    "calculadora": "calc",
    "navegador": "webbrowser",
    "explorador de arquivos": "explorer",
    "loja": "ms-windows-store:",
    "bloco de notas": "notepad",
}

# Função para falar
def speak(text):
    engine = pyttsx3.init()
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
    expression = expression.replace("vezes", "*")
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

# Função principal
def main():
    speak("Olá! Estou ouvindo. Como posso ajudar?")

    while True:
        command = listen()

        if "catarina" in command:
            command = command.replace("catarina", "").strip()  # Remove "catarina" da frase

            if "parar" in command:
                speak("Até logo!")
                break
            elif "quem é você" in command:
                speak("Eu sou uma versão simplificada de um assistente de voz.")
            elif "que dia é hoje" in command:
                current_date = get_current_date()
                speak(f"Hoje é {current_date}")
                print("Data atual:", current_date)  # Mostra a data atual no console
            elif "que horas são" in command:
                current_time = get_current_time()
                speak(f"Agora são {current_time} horas")
                print("Hora atual:", current_time)  # Mostra a hora atual no console
            elif "onde estou" in command:
                current_location = get_current_location()
                speak(f"Você está em {current_location}")
                print("Local atual:", current_location)  # Mostra o local atual no console
            elif "abrir" in command:
                program_to_open = None
                for program, cmd in program_commands.items():
                    if program in command:
                        program_to_open = cmd
                        try:
                            if program_to_open == "webbrowser":
                                webbrowser.open_new_tab("https://www.google.com")  # Abre uma nova guia no navegador padrão
                                speak(f"Abrindo {program}")  # Diz o que está sendo aberto
                            else:
                                os.system(f"start {program_to_open}")  # Tenta executar o programa
                                speak(f"Abrindo {program}")  # Diz o que está sendo aberto
                        except Exception as e:
                            speak("Não foi possível executar essa tarefa.")
                        break
                if not program_to_open:
                    program_name = command.split("abrir", 1)[1].strip()  # Extrai o nome do programa após "abrir"
                    print("Comando para abrir:", program_name)
                    try:
                        os.system(f"start {program_name}")  # Tenta executar o programa
                        speak(f"Abrindo {program_name}")  # Diz o que está sendo aberto
                    except Exception as e:
                        speak("Não foi possível executar essa tarefa.")
            else:
                if "quanto é" in command:
                    expression = command.split("quanto é", 1)[1].strip()  # Extrai a expressão a ser calculada
                    result = calculate(expression)
                    if result is not None:
                        speak(f"O resultado é {result}")
                        print("Resultado:", result)  # Mostra o resultado no console
                    else:
                        speak("Não foi possível calcular a expressão.")
                else:
                    speak("Desculpe, não entendi seu comando. Você disse: " + command)
        else:
            # Verifica se o comando está no dicionário
            program_to_open = None
            for program, cmd in program_commands.items():
                if program in command:
                    program_to_open = cmd
                    try:
                        if program_to_open == "webbrowser":
                            webbrowser.open_new_tab("https://www.google.com")  # Abre uma nova guia no navegador padrão
                        else:
                            os.system(f"start {program_to_open}")  # Tenta executar o programa
                            speak(f"Abrindo {program}")  # Diz o que está sendo aberto
                    except Exception as e:
                        speak("Não foi possível executar essa tarefa.")
                    break
            if not program_to_open:
                if "quanto é" in command:
                    expression = command.split("quanto é", 1)[1].strip()  # Extrai a expressão a ser calculada
                    result = calculate(expression)
                    if result is not None:
                        speak(f"O resultado é {result}")
                        print("Resultado:", result)  # Mostra o resultado no console
                    else:
                        speak("Não foi possível calcular a expressão.")
                elif "que dia é hoje" in command:
                    current_date = get_current_date()
                    speak(f"Hoje é {current_date}")
                    print("Data atual:", current_date)  # Mostra a data atual no console
                elif "que horas são" in command:
                    current_time = get_current_time()
                    speak(f"Agora são {current_time} horas")
                    print("Hora atual:", current_time)  # Mostra a hora atual no console
                elif "onde estou" in command:
                    current_location = get_current_location()
                    speak(f"Você está em {current_location}")
                    print("Local atual:", current_location)  # Mostra o local atual no console
                else:
                    speak("Não foi possível executar essa tarefa.")

if __name__ == "__main__":
    main()
