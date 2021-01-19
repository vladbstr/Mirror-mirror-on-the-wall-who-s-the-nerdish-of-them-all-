# Smart-mirror-software-in-python
DESCRIPTION OF THE PROJECT:
The project is based on the concept of smart mirror, which involves placing a monitor behind a glass with a high level of transparency. The monitor will display important data for the user such as: weather, current time and date, google calendar, latest news and emails. To protect the user's privacy, the google emails and calendar will only be displayed if the user is facial recognized.
The interface has 2 states:
•	the hibernation mode in which only the current time and date is displayed in a large format, to be visible from a distance.
•	 work mode in which the calendar, news, weather and emails are displayed when a person is nearby and is detected by the PIR motion sensor.
INSTALL DEPENDENCIES:
	You must install manually all dependencies, with pip install, because I don't have a file to install them automatically. You find all the libraries you need at the beginning of the file smart_mirror.py
Make project go on:
	In order to start the project, you must first fill in your data in the smart_mirror.py file and after running the take_photos.py file, which will take 20 pictures of you with the help of the Raspberry camera. After that you need to run the trainer.py file to train your facial detection algorithm, with the pictures taken previously.
