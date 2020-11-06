import speech_recognition as sr  # speech recognition
from time import ctime  # get current time
import webbrowser  # open browser
import os  # os interface
import pyautogui #screenshot
import urllib.request
import bs4 as bs


recognizer = sr.Recognizer()

name = 'Kamoliddin'
status = 'free'


def record_audio(ask=False):
	with sr.Microphone() as source:
		if ask:
			print(ask)

		while True:
			try:
				audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
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


def there_exists(terms, voice_data):
	for term in terms:
		if term in voice_data:
			return True


def respond(voice_data, name='Kamoliddin'):
	# activate stem
	if there_exists(['STEM'], voice_data):
		greet = f'I am listening {name}. How can I help you?'
		print(greet)

	# get info
	if there_exists(["what is your name", "what's your name", "tell me your name", "who are you"], voice_data):
		print("My name is STEM. I am your personal Artificial assistant. I was developed by Nabijonov Kamoliddin")

	# set status
	if there_exists(["my status"], voice_data):
		owner_status = voice_data.split("is")[-1].strip()
		print("Your status changed to " + owner_status)
		global status
		status = owner_status

	# get status
	if there_exists(["what is my status", "my status", "tell my current status"]):
		global status
		print("Your status is " + status)

	# STEM condition
	if there_exists(["how are you", "how are you doing"], voice_data):
		print("I am well, thanks for asking " + name)

	# current time
	if there_exists(["what's the time", "tell me the time", "what time is it", "what is the time", "time"], voice_data):
		time = ctime().split(" ")[3].split(":")[0:2]
		if time[0] == "00":
			hours = '12'
		else:
			hours = time[0]
		minutes = time[1]
		time = hours + " hours and " + minutes + "minutes"
		print(time)

	# search google
	if there_exists(["search for"], voice_data):
		search_term = voice_data.split("for")[-1]
		url = "https://google.com/search?q=" + search_term
		webbrowser.get().open(url)
		print("Here is what I found for" + search_term + "on google")

	# search youtube
	if there_exists(["youtube search"], voice_data):
		search_term = voice_data.split("search")[-1]
		url = "https://www.youtube.com/results?search_query=" + search_term
		webbrowser.get().open(url)
		print("Here is what I found for " + search_term + "on youtube")

	# show timetable
	if there_exists(["show my timetable"], voice_data):
		path = "/Applications/Reminders.app"
		os.system(f"open {path}")
		print("Here is your timetable for today")

	# weather
	if there_exists(["What is the weather today", "weather"], voice_data):
		url = "https://www.google.com/search?q=weather+today"
		webbrowser.get().open(url)
		print("Here is the weather for today")

	# calc
	if there_exists(["plus", "minus", "multiply", "divide", "power", "+", "-", "*", "/"], voice_data):
		opr = voice_data.split()[1]
		if opr == '+' or opr == 'plus':
			print(int(voice_data.split()[0]) + int(voice_data.split()[2]))
		elif opr == '-' or opr == 'minus':
			print(int(voice_data.split()[0]) - int(voice_data.split()[2]))
		elif opr == 'multiply' or opr == '*':
			print(int(voice_data.split()[0]) * int(voice_data.split()[2]))
		elif opr == 'divide' or opr == '/':
			try:
				print(int(voice_data.split()[0]) / int(voice_data.split()[2]))
			except ZeroDivisionError:
				print("Cannot divide by zero")
		elif opr == 'power':
			print(int(voice_data.split()[0]) ** int(voice_data.split()[2]))
		else:
			print("Wrong operation")

	# screenshot
	if there_exists(["capture", "my screen", "screenshot","take screenshot"]):
		my_screenshot = pyautogui.screenshot()
		my_screenshot.save('screen.png')
		print("Screenshot was taken")

	# search wikipedia
	if there_exists(["definition of"],voice_data):
		definition = record_audio("What do you need the definition of")
		url = urllib.request.urlopen('https://en.wikipedia.org/wiki/' + definition)
		soup = bs.BeautifulSoup(url, 'lxml')
		definitions = []
		for paragraph in soup.find_all('p'):
			definitions.append(str(paragraph.text))
		if definitions:
			if definitions[0]:
				print('im sorry i could not find that definition, please try a web search')
			elif definitions[1]:
				print('here is what i found ' + definitions[1])
			else:
				print('Here is what i found ' + definitions[2])
		else:
			print("im sorry i could not find the definition for " + definition)

	# Current location Google maps
	if there_exists(["what is my exact location"],voice_data):
		url = "https://www.google.com/maps/search/Where+am+I+?/"
		webbrowser.get().open(url)
		print("You must be somewhere near here, as per Google maps")

	# stop taking commands
	if there_exists(["exit", "quit", "sleep"]):
		print("OK")
		exit()


result = record_audio("Speak! ...")
print(result)
