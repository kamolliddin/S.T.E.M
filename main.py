import speech_recognition as sr

recognizer = sr.Recognizer()


def record_audio(ask=False):
	with sr.Microphone() as source:
		if ask:
			print(ask)

		while True:
			try:
				audio = recognizer.listen(source)
				voice_data = None
				voice_data = recognizer.recognize_google(audio)
				break
			except sr.UnknownValueError:
				print("Try again! I cannot understand you!")
				continue
			except sr.RequestError:
				print("Service is down!")
				continue

		return voice_data

result = record_audio("Speak! ...")
print(result)
