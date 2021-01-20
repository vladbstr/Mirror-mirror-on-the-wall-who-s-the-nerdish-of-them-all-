# Mirror, mirror on the wall, who’s the fairest of them all?
[![GitHub license](https://img.shields.io/github/license/vladbstr/Smart-mirror-software-in-python?logo=MIT)](https://github.com/vladbstr/Smart-mirror-software-in-python/blob/main/LICENSE)
[![GitHub issues](https://img.shields.io/github/issues/vladbstr/Smart-mirror-software-in-python)](https://github.com/vladbstr/Smart-mirror-software-in-python/issues)
![GitHub Pipenv locked Python version](https://img.shields.io/github/pipenv/locked/python-version/metabolize/rq-dashboard-on-heroku)


# DESCRIPTION OF THE PROJECT:

   The project is based on the concept of smart mirror, which involves placing a monitor behind a glass with a high level of transparency. The monitor will display important data for the user such as: weather, current time and date, google calendar, latest news and emails. To protect the user's privacy, the google emails and calendar will only be displayed if the user is facial recognized.

The interface has 2 states:

•	the hibernation mode in which only the current time and date is displayed in a large format, to be visible from a distance.

•	 work mode in which the calendar, news, weather and emails are displayed when a person is nearby and is detected by the PIR motion sensor.

# INSTALL DEPENDENCIES:

Go to your project file and create a virtual environment with next command:

	python3 -m venv env
	
Activate your repository:

	source env/bin/activate
To install all dependencies in env:

	pip install -r requirements.txt

	
# Make project go on:

In order to start the project, fill with your data in the smart_mirror.py file and after run the take_photos.py file, which will take 20 pictures of you with the help of the Raspberry camera. Make sure that the light hits the front of your face and make sure that 20 clear pictures came out, by checking the images folder.
	
	python3 take_photos.py
	
After that you need to run the trainer.py file to train your facial detection algorithm, with the pictures taken previously.
	
	python3 trainer.py
	
Finally run the project:

	python3 smart_mirror.py
Finally product aspect can be found here: https://drive.google.com/file/d/19b1u7DHsgC6GgbKzuPK3BZpZsoT4GTve/view?usp=sharing

