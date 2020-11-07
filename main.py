import speech_recognition as sr  # speech recognition
from time import ctime  # get current time
import webbrowser  # open browser
import os  # os interface
import pyautogui  # screenshot
import urllib.request
import bs4 as bs
import pyttsx3
import time

recognizer = sr.Recognizer()
engine = pyttsx3.init()





def stem_speak(text):
	text = str(text)
	engine.say(text)
	engine.runAndWait()


def record_audio(ask=False):
	with sr.Microphone() as source:
		if ask:
			print(ask)
			stem_speak(ask)

		while True:
			try:
				audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
				print("Command received")
				voice_data = None
				voice_data = recognizer.recognize_google(audio)
				break
			except sr.UnknownValueError:
				print("Try again. I cannot understand you")
				stem_speak("Try again. I cannot understand you")
				continue
			except sr.RequestError:
				print("The service is down.")
				stem_speak("The service is down.")
				continue
			except sr.WaitTimeoutError:
				continue
		print(">>", voice_data.lower())
		return voice_data.lower()


def there_exists(terms, voice_data):
	for term in terms:
		if term in voice_data:
			return True


def respond(voice_data, name='Kamoliddin'):
	# activate stem
	if there_exists(['STEM'], voice_data):
		greet = f'I am listening {name}. How can I help you?'
		print(greet)
		stem_speak(greet)

	# get info
	if there_exists(["what is your name", "what's your name", "tell me your name", "who are you"], voice_data):
		print("My name is STEM. I am your personal Artificial assistant. I was developed by Nabijonov Kamoliddin")
		stem_speak("My name is STEM. I am your personal Artificial assistant. I was developed by Nabijonov Kamoliddin")

	# set status
	if there_exists(["change status"], voice_data):
		owner_status = record_audio("What is your status")
		print("Your status changed to " + owner_status)
		stem_speak("Your status changed to " + owner_status)
		global status
		status = owner_status

	# get status
	if there_exists(["what is my status", "my status", "tell my current status"], voice_data):
		print("Your status is " + status)
		stem_speak("Your status is " + status)

	# STEM condition
	if there_exists(["how are you", "how are you doing"], voice_data):
		print("I am well, thanks for asking ")
		stem_speak("I am well, thanks for asking ")

	# current time
	if there_exists(["what is the time", "tell me the time", "what time is it", "what is the time", "time"],
					voice_data):
		stem_speak(ctime())

	# search google
	if there_exists(["search for"], voice_data):
		search_term = voice_data.split("for")[-1]
		url = "https://google.com/search?q=" + search_term
		webbrowser.get().open(url)
		print("Here is what I found for" + search_term + "on google")
		stem_speak("Here is what I found for" + search_term + "on google")

	# 	elif 'search' in voice_data:
	# search = record_audio("What do you want to search for")
	# url = 'https://google.com/search?q=' + search

	# search youtube
	if there_exists(["youtube search"], voice_data):
		search_term = voice_data.split("search")[-1]
		url = "https://www.youtube.com/results?search_query=" + search_term
		webbrowser.get().open(url)
		print("Here is what I found for " + search_term + "on youtube")
		stem_speak("Here is what I found for " + search_term + "on youtube")

	# show timetable
	if there_exists(["show my tasks","tasks"], voice_data):
		import subprocess
		subprocess.call(
		["/usr/bin/open", "-W", "-n", "-a", "/Applications/Reminders.app"]
		)
		print("Here is your tasks for today")
		stem_speak("Here is your tasks for today")

	# weather
	if there_exists(["What is the weather today", "weather"], voice_data):
		url = "https://www.google.com/search?q=weather+today"
		webbrowser.get().open(url)
		print("Here is the weather for today")
		stem_speak("Here is the weather for today")

	# calc
	if there_exists(["plus", "minus", "multiply", "divide", "power", "+", "-", "*", "/"], voice_data):
		opr = voice_data.split()[1]
		if opr == '+' or opr == 'plus':
			print(int(voice_data.split()[0]) + int(voice_data.split()[2]))
			stem_speak(int(voice_data.split()[0]) + int(voice_data.split()[2]))
		elif opr == '-' or opr == 'minus':
			print(int(voice_data.split()[0]) - int(voice_data.split()[2]))
			stem_speak(int(voice_data.split()[0]) - int(voice_data.split()[2]))
		elif opr == 'multiply' or opr == '*':
			print(int(voice_data.split()[0]) * int(voice_data.split()[2]))
			stem_speak(int(voice_data.split()[0]) * int(voice_data.split()[2]))
		elif opr == 'divide' or opr == '/':
			try:
				print(int(voice_data.split()[0]) / int(voice_data.split()[2]))
				stem_speak(int(voice_data.split()[0]) / int(voice_data.split()[2]))
			except ZeroDivisionError:
				print("Cannot divide by zero")
				stem_speak("Cannot divide by zero")
		elif opr == 'power':
			print(int(voice_data.split()[0]) ** int(voice_data.split()[2]))
			stem_speak(int(voice_data.split()[0]) ** int(voice_data.split()[2]))
		else:
			print("Wrong operation")
			stem_speak("Wrong operation")

	# screenshot
	if there_exists(["capture", "my screen", "screenshot", "take screenshot"], voice_data):
		my_screenshot = pyautogui.screenshot()
		my_screenshot.save('screen.png')
		print("Screenshot was taken")
		stem_speak("Screenshot was taken")

	# search wikipedia
	if there_exists(["definition of"], voice_data):
		definition = record_audio("What do you need the definition of")
		url = urllib.request.urlopen('https://en.wikipedia.org/wiki/' + definition)
		soup = bs.BeautifulSoup(url, "lxml")
		definitions = []
		for paragraph in soup.find_all('p'):
			definitions.append(str(paragraph.text))
		if definitions:
			if definitions[0]:
				print('im sorry i could not find that definition, please try a web search')
				stem_speak('im sorry i could not find that definition, please try a web search')
			elif definitions[1]:
				print('here is what i found ' + definitions[1])
				stem_speak('here is what i found ' + definitions[1])
			else:
				print('Here is what i found ' + definitions[2])
				stem_speak('Here is what i found ' + definitions[2])
		else:
			print("im sorry i could not find the definition for " + definition)
			stem_speak("im sorry i could not find the definition for " + definition)

	# Current location Google maps
	if there_exists(["what is my location"], voice_data):
		url = "https://www.google.com/maps/search/Where+am+I+?/"
		webbrowser.get().open(url)
		print("You must be somewhere near here, as per Google maps")
		stem_speak("You must be somewhere near here, as per Google maps")

	# Find location on map
	if there_exists(["find location"], voice_data):
		location = record_audio("What is the location")
		url = 'https://google.nl/maps/place/' + location + '/&amp;'
		webbrowser.get().open(url)
		print("Here is the location of " + location)
		stem_speak("Here is the location of " + location)

	# stop taking commands
	if there_exists(["exit", "quit", "sleep"], voice_data):
		print("OK")
		stem_speak("OK")
		exit()

status = ''
time.sleep(1)
print("How can I help you?")
stem_speak("How can I help you?")
while (1):
	voice_data = record_audio()  # get the voice input
	print("Done")
	print("Q:", voice_data)
	respond(voice_data,status)  # respond
