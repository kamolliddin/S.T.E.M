import speech_recognition as sr

recognizer = sr.Recognizer()


def record_audio(ask=False):
	with sr.Microphone() as source:
		if ask:
			print(ask)

		while True:
			try:
				audio = recognizer.listen(source,timeout=5,phrase_time_limit=5)
				print("Command received")
				voice_data = None
				voice_data = recognizer.recognize_google(audio)
				break
			except sr.UnknownValueError:
				print("Try again. I cannot understand you")
				continue
			except sr.RequestError:
				print("The service is down.")
				continue
		print(">>", voice_data.lower())
		return voice_data.lower()

result = record_audio("Speak! ...")
print(result)
