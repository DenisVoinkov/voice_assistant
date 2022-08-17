from numpy import vectorize
from sklearn.feature_extraction.text import CountVectorizer  # нейросеть векторов
from sklearn.linear_model import LogisticRegression  # нейросеть регрессии
import sounddevice as sd  # модуль sounddevice
import vosk
import json
import queue
import words
from skills import *
import voice
from termcolor import colored


q = queue.Queue()

model = vosk.Model('/Users/unknown1/Documents/Python/Morgana/vosk_small')

device = sd.default.device
samplerate = int(sd.query_devices(device[0], 'input')['default_samplerate'])


def callback(indata, frames, time, status):
    q.put(bytes(indata))


def recognize(data, vectorizer, clf):
    '''
    Анализ распознанной речи
    '''

    # проверяет есть ли имя бота в data, если нет, то return
    trg = words.TRIGGERS.intersection(data.split())
    if not trg:
        return

    # удалить имя бота из текста
    data.replace(list(trg)[0], '')

    # получить вектор распознанного текста
    # сравнить варианты, получая наиболее подходящий ответ
    text_vector = vectorizer.transform([data]).toarray()[0]
    answer = clf.predict([text_vector])[0]
    print(colored('Пользователь: ' + (data), 'green'))
    print(colored('Моргана: ' + (answer), 'magenta'))
    # получение имени функции из ответа из data_set
    func_name = answer.split()[0]

    # озвучка ответа из модели data_set
    voice.speaker(answer.replace(func_name, ''))

    # запись функции из skills
    exec(func_name +'()')


def main():
    '''
    Обучаем матрицу ИИ,
    и постоянно слушаем микрофон
    '''
    print('Моргана работает...')
    # обучение матрицы на data_set
    vectorizer = CountVectorizer()
    vectors = vectorizer.fit_transform(list(words.data_set.keys()))

    clf = LogisticRegression()
    clf.fit(vectors, list(words.data_set.values()))

    del words.data_set

    # постоянная прослушка микрофона
    with sd.RawInputStream(samplerate=samplerate, blocksize = 16000, device=device[0], dtype='int16',
                           channels=1, callback=callback):
        rec = vosk.KaldiRecognizer(model, samplerate)
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                data = json.loads(rec.Result())['text']
                recognize(data, vectorizer, clf)


if __name__ == '__main__':
    main()
