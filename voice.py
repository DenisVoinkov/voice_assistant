import pyttsx3

engine = pyttsx3.init()
engine.setProperty('rate', 150)  # скорость речи


def speaker(text):
    '''
    озвучка текста
    '''
    engine.say(text)
    engine.runAndWait()
