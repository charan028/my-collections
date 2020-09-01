from translate import Translator
import pyttsx3
speaker=pyttsx3.init()
source=input("enter the word to translate:")
destination=input("enter the language to translate:")
translator=Translator(to_lang=destination)
translation=translator.translate(source)
print(translation)
speaker.say(translation)
speaker.runAndWait()