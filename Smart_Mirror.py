from tkinter import *
import locale
import threading
import arrow
import time
import requests
import json
import traceback
import feedparser
from ics import Calendar,Event
from datetime import datetime
import requests,dateutil.parser
import pytz
import feedparser
import io
import PIL
import tzlocal
import Adafruit_DHT
import RPi.GPIO as GPIO
import imaplib,email,webbrowser,os
from email.header import decode_header
from PIL import Image, ImageTk
from contextlib import contextmanager
import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera
import numpy as np 
import pickle

LOCALE_LOCK = threading.Lock()
var=0
ui_locale = '' # e.g. 'fr_FR' fro French, '' as default
time_format = 24 # 12 or 24
date_format = "%d %B %Y" # check python doc for strftime() for options
news_country_code = 'us'
xlarge_text_size = 94
large_text_size = 48
medium_text_size = 28
small_text_size = 18
camera = PiCamera()


@contextmanager
def setlocale(name): #thread proof function to work with locale
    with LOCALE_LOCK:
        saved = locale.setlocale(locale.LC_ALL)
        try:
            yield locale.setlocale(locale.LC_ALL, name)
        finally:
            locale.setlocale(locale.LC_ALL, saved)

class Motion(Frame):

    def __init__(self):
        Frame.__init__(self)
        
        self.motion()
        
    def motion(self):
            GPIO.setmode(GPIO.BCM)
            PIR_PIN = 4
            GPIO.setup(PIR_PIN, GPIO.IN)
            if GPIO.input(4): # if port 4 == 1  
                return 1
            else:
                return 0
        
class CalendarMirror(Frame):
        def __init__(self, parent, *args, **kwargs):
            Frame.__init__(self, parent, bg='black')
            motion1=Motion()
            self.calendar_ro = Label(self, text='', font=('Helvetica', 25), fg="white", bg="black")
            self.calendar_ro.pack(side=TOP,anchor=E)
            self.next()
            
        def next(self):
            self.today = datetime.utcnow().replace(tzinfo=pytz.utc)
            self.eventContentLbl=[]
            self.eventcalendar_ro=[]
            for i in range(5):
                vec_calendar_ro = Label(self, text='',font=('Times', 15), fg="white", bg="black")
                vec_calendar_ro.pack(side=TOP,anchor=E)
                self.eventcalendar_ro.append(vec_calendar_ro)
            self.calendarLbl = Label(self, text='', font=('Helvetica', 25), fg="white", bg="black")
            self.calendarLbl.pack(side=TOP,anchor=E)
            for i in range(3):
                vec = Label(self, text='',font=('Times', 15), fg="white", bg="black")
                vec.pack(side=TOP,anchor=E)
                self.eventContentLbl.append(vec)
            
            self.email_titleLbl = Label(self, text='', font=('Helvetica', 20,'bold'), fg="white", bg="black")
            self.email_titleLbl.pack(side=TOP,anchor=E)
            self.emailscontentLbl=[]
            for a in range(11):
                vec_emails=Label(self, text='',font=('Times', 15), fg="white", bg="black")
                vec_emails.pack(side=TOP,anchor=W)
                self.emailscontentLbl.append(vec_emails)
            self.update_events1()
            self.update_emails1()
            self.update_emails()
            
        def update_events1(self):
            time.sleep(1)
            self.url2="https://www.officeholidays.com/ics-clean/romania"
            self.url = ""# here I put my google calendar url 
            self.c = Calendar(requests.get(self.url).text)
            self.c2 = Calendar(requests.get(self.url2).text)
            self.after(60000*10,self.update_events1)
            
        def update_emails1(self):
            username = ""# email address
            password = "" 
            self.imap = imaplib.IMAP4_SSL("imap.gmail.com")

            self.imap.login(username, password)
            self.status, self.messages = self.imap.select("INBOX")
            self.secons_status, self.unseen_messages= self.imap.search(None, 'UnSeen')
                #count =len(mail_ids[0].split(" "))
            self.air_message=self.unseen_messages[0].decode("utf-8")
            if len(self.air_message)>0:
                self.count = len(self.air_message.split(" "))
            else:
                self.count=len(self.air_message)
                # number of top emails to fetch
            self.N = 5
                # total number of emails
            self.counter=0
            self.messages = int(self.messages[0])
            self.after(6000*10,self.update_emails1)
            
        def update_emails(self):
            motion1=Motion()
            num_to_stop = 0
            if motion1.motion()== 1:
                a,b=video_recognizer()
                self.calendar_ro.config(text='Calendar Events')
                for event in self.c2.timeline:
                    if event.end > self.today:
            
                        if num_to_stop == 5:
                            break
                        
                        begin_event=arrow.get(event.begin)
                        self.eventContent2 = event.name + '  ' + begin_event.format('DD.MM')
                        self.eventcalendar_ro[num_to_stop].config(text='')   
                        self.eventcalendar_ro[num_to_stop].config(text= self.eventContent2)
                        num_to_stop =num_to_stop + 1
                num_to_stop = 0
                if a==3:
                    self.calendarLbl.config(text='Calendar Google')
                    for event in self.c.timeline:
                        if event.end > self.today:
            
                            if num_to_stop == 5:
                                break
                        
                            begin_event=arrow.get(event.begin)
                            self.eventContent = event.name + '  ' + begin_event.format('DD.MM')
                            self.eventContentLbl[num_to_stop].config(text='')   
                            self.eventContentLbl[num_to_stop].config(text= self.eventContent)
                            num_to_stop =num_to_stop + 1
                    self.email_titleLbl.config(text='HELLO MR.**********! Here is your emails:',wraplength=350)
                    for i in range(self.messages, self.messages-self.N, -1):
                    # fetch the email message by ID
                        res, msg = self.imap.fetch(str(i), "(RFC822)")
                        for response in msg:
                            if isinstance(response, tuple):
                            # parse a bytes email into a message object
                                msg = email.message_from_bytes(response[1])
                            # decode the email subject
                                subject = decode_header(msg["Subject"])[0][0]
                                if isinstance(subject, bytes):
                                # if it's a bytes, decode to str
                                    subject = subject.decode()
                            # email sender
                                if len(subject) > 22:
                                    subject=subject[0:21]
                                from_ = msg.get("From")
                                for var in range(len(from_)):
                                    if from_[var] == '<':
                                        from_=from_[0:var]
                                        break
                                self.emailscontentLbl[self.counter].config(text='FROM: '+from_,wraplength=350)
                                self.emailscontentLbl[self.counter+1].config(text='Subject: '+subject,wraplength=350)
                                self.counter+=2
                            # print("Subject:", subject)
                            # print("From:", from_)
                    self.counter=0
                    if self.count==0:
                        self.emailscontentLbl[10].config(text='You have no new emails!',font=('Times', 17,'bold'))
                    elif self.count==1:
                        self.emailscontentLbl[10].config(text='You have a new email!',font=('Times', 17,'bold'))
                    else:
                        self.emailscontentLbl[10].config(text='You have '+str(self.count)+' new emails!',font=('Times', 17,'bold'))
                    
            else:
                self.calendar_ro.config(text='')
                for y in range(5):
                    self.eventcalendar_ro[y].config(text='')
                self.email_titleLbl.config(text='')
                for a in range(11):
                    self.emailscontentLbl[a].config(text='')
                self.calendarLbl.config(text='')
                for x in range(3):
                    self.eventContentLbl[x].config(text='')
            self.after(700, self.update_emails)    
class News(Frame):

    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, bg='black')
        self.title = ''
        self.newsLbl = Label(self, text=self.title, font=('Helvetica', 25), fg="white", bg="black")
        self.newsLbl.pack(side=TOP, anchor=N)


        self.pi_max=6
        self.newscontentLbl=[]
        for m in range(0,self.pi_max):
            tmp = Label(self, text='',font=('Times', 15), fg="white", bg="black")
            tmp.pack(side=TOP,anchor=W)
            self.newscontentLbl.append(tmp)
        self.update_news1()
        self.update_news()
        
    def update_news1(self):
        self.NewsFeed = feedparser.parse("https://www.biziday.ro/feed/")
        self.after(60000*6,self.update_news1)
    def update_news(self):
        motion1=Motion()
        if motion1.motion() == 1:
            self.newsLbl.config(text='News')
            for k in range(0,5):
                entry=self.NewsFeed.entries[k]
                newscontent=entry.title
                self.newscontentLbl[k].config(text='*'+newscontent,wraplength=1200)
        else:
            self.newsLbl.config(text='')
            for x in range(5):
                self.newscontentLbl[x].config(text='')
        self.after(500, self.update_news) 


class Weather(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, bg='black')
        self.time1 = ''
        self.timeLbl = Label(self, font=('Times', 40), fg="white", bg="black")
        self.timeLbl.pack(side=TOP, anchor=W)
        # initialize day of week
        self.day_of_week1 = ''
        self.dayOWLbl = Label(self, text=self.day_of_week1, font=('Times', 18), fg="white", bg="black")
        self.dayOWLbl.pack(side=TOP, anchor=W)
        # initialize date label
        self.date1 = ''
        self.dateLbl = Label(self, text=self.date1, font=('Times', 18), fg="white", bg="black")
        self.dateLbl.pack(side=TOP, anchor=W)
        
        self.temperature = ''
        self.forecast = ''
        self.location = ''
        self.currently = ''
        self.icon = ''
        self.feels_like=''
        self.sunrise=''
        self.sunset=''
        self.day_forecast_initial2=''
        self.day_forecast_initial=''
        self.degreeFrm = Frame(self, bg="black")
        self.degreeFrm.pack(side=TOP, anchor=W)
        self.degreeFrm2 = Frame(self, bg="black")
        self.degreeFrm2.pack(side=TOP, anchor=W)
        
        self.temperatureLbl = Label(self.degreeFrm, font=('Helvetica', 75), fg="white", bg="black")
        self.temperatureLbl.pack(side=LEFT, anchor=N)
        self.iconLbl = Label(self.degreeFrm, bg="black")
        self.iconLbl.pack(side=LEFT, anchor=N, padx=20)
        
       

        self.icon_sunriseLbl = Label(self.degreeFrm2,bg="black")
        self.icon_sunriseLbl.pack(side=LEFT, anchor=N, padx=0,pady=0)
        self.sunriseLbl =Label(self.degreeFrm2, font=('Helvetica', 15), fg="white", bg="black")
        self.sunriseLbl.pack(side=LEFT, anchor=N)

        self.icon_sunsetLbl = Label(self.degreeFrm2,bg="black")
        self.icon_sunsetLbl.pack(side=LEFT, anchor=N, padx=0,pady=0)
        self.sunsetLbl =Label(self.degreeFrm2, font=('Helvetica', 15), fg="white", bg="black")
        self.sunsetLbl.pack(side=LEFT, anchor=N)
        

        self.currentlyLbl = Label(self, font=('Helvetica', 15), fg="white", bg="black")
        self.currentlyLbl.pack(side=TOP, anchor=W)
        self.feels_likeLbl = Label(self, font=('Helvetica', 15), fg="white", bg="black")
        self.feels_likeLbl.pack(side=TOP, anchor=W)
        self.roomLbl = Label(self, font=('Helvetica', 15), fg="white", bg="black")
        self.roomLbl.pack(side=TOP, anchor=W)
        
        self.degreeFrm3 = Frame(self, bg="black")
        self.degreeFrm3.pack(side=TOP, anchor=W)
        self.forecast_day1Lbl =Label(self.degreeFrm3, font=('Helvetica', 15), fg="white", bg="black")
        self.forecast_day1Lbl.pack(side=LEFT, anchor=W,pady=0)
        self.icon_forecast1Lbl = Label(self.degreeFrm3,bg="black")
        self.icon_forecast1Lbl.pack(side=LEFT, anchor=W, padx=0,pady=0)
        self.degreeFrm4 = Frame(self, bg="black")
        self.degreeFrm4.pack(side=TOP, anchor=W)
        self.forecast_day2Lbl =Label(self.degreeFrm4, font=('Helvetica', 15), fg="white", bg="black")
        self.forecast_day2Lbl.pack(side=LEFT, anchor=W,pady=0)
        self.icon_forecast2Lbl = Label(self.degreeFrm4,bg="black")
        self.icon_forecast2Lbl.pack(side=LEFT, anchor=W, padx=0,pady=0)


        self.locationLbl = Label(self, font=('Helvetica', 15), fg="white", bg="black")
        self.locationLbl.pack(side=TOP, anchor=W)
        self.tick()
        self.get_weather1()
        self.get_weather()
        
    def tick(self):
        motion1=Motion()
        if motion1.motion() == 1:
            self.timeLbl.config(font=('Times',35,'bold'))
            self.timeLbl.pack(side=TOP, anchor=W)
            self.dayOWLbl.config(font=('Times',25))
            self.dayOWLbl.pack(side=TOP, anchor=W)
            self.dateLbl.config(font=('Times',25))
            self.dateLbl.pack(side=TOP, anchor=W)
            with setlocale(ui_locale):
                if time_format == 12:
                    time2 = time.strftime('%I:%M %p') #hour in 12h format
                else:
                    time2 = time.strftime('%H:%M') #hour in 24h format

                day_of_week2 = time.strftime('%A')
                date2 = time.strftime(date_format)
                self.time1 = time2
                self.timeLbl.config(text=time2)
                self.dayOWLbl.config(text=day_of_week2)
                self.dateLbl.config(text=date2)
        else:
            self.dateLbl.config(font=('Times',70))
            self.dateLbl.pack(side=BOTTOM, anchor=SE)
            self.timeLbl.config(font=('Times',70))
            self.timeLbl.pack(side=BOTTOM, anchor=SE)
            self.dayOWLbl.config(font=('Times',70))
            self.dayOWLbl.pack(side=BOTTOM, anchor=SE)
            
            with setlocale(ui_locale):
                if time_format == 12:
                    time2 = time.strftime('%I:%M %p') #hour in 12h format
                else:
                    time2 = time.strftime('%H:%M') #hour in 24h format

                day_of_week2 = time.strftime('%A')
                date2 = time.strftime(date_format)
                self.time1 = time2
                self.timeLbl.config(text=time2)
                self.dayOWLbl.config(text=day_of_week2)
                self.dateLbl.config(text=date2)
        
        self.after(200, self.tick)
        
    def get_weather1(self):
        self.get_url_weather=""#add weather api url
        self.get_url_forecast=""#add forecast api url
        self.r2=requests.get(self.get_url_forecast)
        self.forecast_obj=json.loads(self.r2.text)
        self.r=requests.get(self.get_url_weather)
        self.weather_obj = json.loads(self.r.text)
        self.degree_sign= u'\N{DEGREE SIGN}'
        self.temperature2=str(int(self.weather_obj['main']['temp']-273))+str(self.degree_sign)
        self.feels_like2=str(int(self.weather_obj['main']['feels_like']-273))
        self.currently2=self.weather_obj['weather'][0]['description']
        self.location=self.weather_obj['name']
        self.country_code=self.weather_obj['sys']['country']
        self.weather_icon_id = self.weather_obj['weather'][0]['icon']
        self.weather_url_icon='http://openweathermap.org/img/wn/'+str(self.weather_icon_id)+'@2x.png'
        self.response = requests.get(self.weather_url_icon)
        self.image_bytes = io.BytesIO(self.response.content)
        self.image = PIL.Image.open(self.image_bytes)
        self.image = self.image.resize((100, 100), Image.ANTIALIAS)
        self.photo = ImageTk.PhotoImage(self.image)
        self.sunrise_format = float(self.weather_obj['sys']['sunrise'])
        self.sunset_format=float(self.weather_obj['sys']['sunset'])
        self.local_timezone = tzlocal.get_localzone() # get pytz timezone
        self.sunrise = datetime.fromtimestamp(self.sunrise_format,self.local_timezone)
        self.sunset = datetime.fromtimestamp(self.sunset_format,self.local_timezone)
        self.sunrise2=self.sunrise.strftime("%H:%M")
        self.sunset2=self.sunset.strftime("%H:%M")
        self.image_sunrise = Image.open("icons/sunrise.png")
        self.image_sunrise = self.image_sunrise.resize((25, 25), Image.ANTIALIAS)
        self.photo2 = ImageTk.PhotoImage(self.image_sunrise)
        
        self.image_sunset = Image.open("icons/sunset.png")
        self.image_sunset = self.image_sunset.resize((25, 25), Image.ANTIALIAS)
        self.photo3 = ImageTk.PhotoImage(self.image_sunset)
        
        self.urlforecast=self.forecast_obj['data'][1]['weather']['icon']
        self.url_forecast_icon="https://www.weatherbit.io/static/img/icons/"+str(self.urlforecast)+".png"
        self.vreme_prima_zi=str(self.forecast_obj['data'][1]['temp'])+str(self.degree_sign)
        self.description1=self.forecast_obj['data'][1]['weather']['description'] 
        self.ts_prima_zi=float(self.forecast_obj['data'][1]['ts'])
        self.day1_forecast=datetime.fromtimestamp(self.ts_prima_zi, self.local_timezone)
        self.day1_forecast2=str(self.day1_forecast.strftime("%a"))
        self.image_req=requests.get(self.url_forecast_icon)
        self.image_bytes2 = io.BytesIO(self.image_req.content)
        self.image_day1=PIL.Image.open(self.image_bytes2)
        self.image_day1 = self.image_day1.resize((35, 35), Image.ANTIALIAS)
        self.photo4 = ImageTk.PhotoImage(self.image_day1)
        self.precipit1=self.forecast_obj['data'][1]['pop']
        self.precipit2=self.forecast_obj['data'][2]['pop']
        
        self.urlforecast2=self.forecast_obj['data'][2]['weather']['icon']
        self.url_forecast_icon2="https://www.weatherbit.io/static/img/icons/"+str(self.urlforecast2)+".png"
        self.vreme_adoua_zi=str(self.forecast_obj['data'][2]['temp'])+str(self.degree_sign)
        self.description2=self.forecast_obj['data'][2]['weather']['description']
        self.ts_adoua_zi=float(self.forecast_obj['data'][2]['ts'])
        self.day2_forecast=datetime.fromtimestamp(self.ts_adoua_zi, self.local_timezone)
        self.day2_forecast3=str(self.day2_forecast.strftime("%a"))
        self.image_req2=requests.get(self.url_forecast_icon2)
        self.image_bytes3 = io.BytesIO(self.image_req2.content)
        self.image_day2=PIL.Image.open(self.image_bytes3)
        self.image_day2 = self.image_day2.resize((35, 35), Image.ANTIALIAS)
        self.photo5 = ImageTk.PhotoImage(self.image_day2)

        
    def get_weather(self):
        motion1=Motion()
        if motion1.motion() == 1:
            self.locationLbl.config(text=self.location+", "+self.country_code)
            self.iconLbl.config(image=self.photo)
            self.iconLbl.image = self.photo
            
            self.icon_sunriseLbl.config(image=self.photo2)
            self.icon_sunriseLbl.image =self.photo2
            self.sunrise=self.sunrise2
            self.sunriseLbl.config(text=str(self.sunrise))
            
            self.icon_sunsetLbl.config(image=self.photo3)
            self.icon_sunsetLbl.image = self.photo3
           

            
            
            
            self.icon_forecast1Lbl.config(image=self.photo4)
            self.icon_forecast1Lbl.image= self.photo4
            
            self.day_forecast_initial=self.vreme_prima_zi
            self.forecast_day1Lbl.config(text=self.day1_forecast2+": "+str(self.precipit1)+'% '+self.description1+" "+self.vreme_prima_zi)
            
            
            
            
            self.icon_forecast2Lbl.config(image=self.photo5)
            self.icon_forecast2Lbl.image= self.photo5
            
            
            self.day_forecast_initial2=self.vreme_adoua_zi
            self.forecast_day2Lbl.config(text=self.day2_forecast3+": "+str(self.precipit2)+'% '+self.description2+" "+self.vreme_adoua_zi)

            
            self.sunset=self.sunset2
            self.sunsetLbl.config(text=str(self.sunset))

            
            self.temperature = self.temperature2
            self.temperatureLbl.config(text=self.temperature2)

            
            self.feels_like=self.feels_like2
            self.feels_likeLbl.config(text='Feels like '+self.feels_like2+str(self.degree_sign)+'C')

            
            self.currently = self.currently2
            self.currentlyLbl.config(text=self.currently2)
             
        else:
            self.locationLbl.config(text='')
            self.iconLbl.config(image='')
            self.icon_sunriseLbl.config(image='')
            self.icon_sunsetLbl.config(image='')
            self.sunriseLbl.config(text='')
            self.icon_forecast1Lbl.config(image='')
            self.forecast_day1Lbl.config(text='')
            self.icon_forecast2Lbl.config(image='')
            self.forecast_day2Lbl.config(text='')
            self.sunsetLbl.config(text='')
            self.temperatureLbl.config(text='')
            self.feels_likeLbl.config(text='')
            self.currentlyLbl.config(text='')
            
            
        self.after(1200, self.get_weather)

def video_recognizer():
    
    with open('labels', 'rb') as f:
        dicti = pickle.load(f)
        f.close()

    camera.resolution = (640, 480)
    camera.framerate = 30
    rawCapture = PiRGBArray(camera, size=(640, 480))
    faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read("trainer.yml")
    font = cv2.FONT_HERSHEY_SIMPLEX

    p=0
    a=0
    q=0
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        frame = frame.array
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, scaleFactor = 1.5, minNeighbors = 5)
    
        for (x, y, w, h) in faces:
            roiGray = gray[y:y+h, x:x+w]

            id_, conf = recognizer.predict(roiGray)
    
            name=''#add your name firstly

            if conf <= 70:
                p=p+1
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.putText(frame, name + str(conf), (x, y),font, 2, (0, 0 ,255), 2,cv2.LINE_AA)

            else:
                q=q+1

        #cv2.imshow('frame', frame)
        key = cv2.waitKey(1)
        a=a+1
        print(a)
        rawCapture.truncate(0)
        print(key)
        if key == 27 or a==10 or p==3 or q==3:
            break

    cv2.destroyAllWindows()
    return p,q
    

    

class FullscreenWindow:

    def __init__(self):
        self.tk = Tk()
        self.tk.attributes('-fullscreen', True)
        self.tk.configure(background='black')
        self.topFrame = Frame(self.tk, background = 'black')
        self.bottomFrame = Frame(self.tk, background = 'black')
        self.topFrame.pack(side = TOP, fill=BOTH, expand = YES)
        self.bottomFrame.pack(side = BOTTOM, fill=BOTH, expand = YES)
        self.state = False
            
        # calender
        self.calender = CalendarMirror(self.topFrame)
        self.calender.pack(side=RIGHT, anchor=NE, padx=0, pady=0)
            
        #vreme
        self.weather = Weather(self.topFrame)
        self.weather.pack(side=LEFT, anchor=NW, padx=0, pady=0)
        
        #news
        self.news = News(self.bottomFrame)
        self.news.pack(side=LEFT,anchor=SE,padx=0,pady=0)
        
if __name__ == '__main__':

    w = FullscreenWindow()
    w.tk.mainloop()
    
    