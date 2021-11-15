import pyttsx3
engine = pyttsx3.init()
#engine = pyttsx3.init("sapi5")
engine.setProperty('volume', 1.0)


def text_to_file(text):
    tmp_file_name = "reply"
    engine.save_to_file(text, f"data/{tmp_file_name}.mp3")
    engine.runAndWait()
    return f"data/{tmp_file_name}.mp3"


voices = engine.getProperty('voices')


def print_voices():
    for voice in voices:
        print("Voice: %s" % voice.name)
        print(" - ID: %s" % voice.id)
        print(" - Languages: %s" % voice.languages)
        print(" - Gender: %s" % voice.gender)
        print(" - Age: %s" % voice.age)
        print("\n")


# Отображаем в терминале список голосов робота.
print_voices()
# Здесь можно выбрать голос из списка, выведенного функцией print_voices() в терминал.
engine.setProperty("voice", voices[1].id)