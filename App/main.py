from kivy.clock import Clock
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.core.audio import SoundLoader
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
import socket
import threading
from time import strftime
import time
import datetime

Window.keyboard_anim_args = {'d': .2, 't': 'in_out_expo'}
Window.softinput_mode = "below_target"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

class MainScreen(Screen):
    pass

class SecondScreen(Screen):
    pass

class WindowManager(ScreenManager):
    pass

sm = ScreenManager()

sm.add_widget(MainScreen(name='main'))

sm.add_widget(SecondScreen(name='second'))

class MainApp(MDApp):
    
    
    sound = SoundLoader.load('../Assets/Sounds/alarm.ogg')
    
    sound.loop = True
    
    volume = 0
    
    def connect_to_server(self):
        
        if self.root.get_screen("main").ids.ip_text.text != "":
            
            client.connect((self.root.get_screen("main").ids.ip_text.text, 6666))
            
            message = client.recv(1024).decode('utf-8')
            
            if message == "NICK":
                
                client.send(self.root.get_screen("main").ids.ip_text.text.encode('utf-8'))
                
                thread = threading.Thread(target=self.receive)
                
                thread.start()
    
    def receive(self):
        
        stop = False
        
        while not stop:
            
            try:
                
                message = client.recv(1024).decode('utf-8')
                
                self.root.get_screen("second").ids.alarm_time.text = message
                
                self.schedule()
            
            except:
                
                print("ERROR")
                
                client.close()
                
                stop = True
    
    def build(self):
        
        
        self.theme_cls.theme_style = "Light"
        
        self.theme_cls.primary_palette = "Red"
        
        self.theme_cls.primary_hue = "50"
        
        self.title = 'Clock'
        
        self.icon = '../Assets/Images/clock.png'
        
        Clock.schedule_interval(self.hour, 1)
        
        Clock.schedule_interval(self.hourpunctuation, 1)
        
        return Builder.load_file('../Interface/main.kv')
    
    def schedule(self, *args):
        Clock.schedule_once(self.alarm, 1)
    
    def alarm(self, *args):
        def run():
            
            while True:
                
                time.sleep(1)
                
                current_time = datetime.datetime.now().strftime("%H:%M:%S")
                
                if self.root.get_screen("second").ids.alarm_time.text == str(current_time):
                    
                    self.root.get_screen("second").ids.add_time.text = 'ALARME TOCANDO'
                    self.root.get_screen("second").ids.alarm_time.text = 'ALARME TOCANDO'
                    
                    self.start()
                    
                    break
        
        thread = threading.Thread(target=run)
        
        thread.start()
    
    def hour(self, *args):
        self.root.get_screen("second").ids.time.text = strftime("%H:%M:%S")
    
    def get_time(self, instance, time):
        self.root.get_screen("second").ids.alarm_time.text = str(time)
    
    def submit(self, *args):
        
        client.send(f"{self.root.get_screen('second').ids.alarm_time.text}".encode("utf-8"))
        
        self.root.get_screen("second").ids.alarm_time.text = self.root.get_screen("second").ids.add_time.text
        
        self.schedule()
    
    def clear(self):
        
        self.root.get_screen("second").ids.add_time.text = ''
    
    def stop(self):
        
        self.sound.stop()
        
        self.sound.loop = False
        
        self.volume = 0
        
        self.root.get_screen("second").ids.add_time.text = ''
        self.root.get_screen("second").ids.alarm_time.text = ''
    
    def start(self, *args):
        
        self.sound.play()
        
        self.volume = 1
    
    def hourpunctuation(self, *args):
        
        if len(self.root.get_screen("second").ids.add_time.text) == 6 and self.root.get_screen("second").ids.add_time.text.isnumeric():
                self.root.get_screen("second").ids.add_time.text = self.root.get_screen("second").ids.add_time.text[:2] + ":" + \
                    self.root.get_screen("second").ids.add_time.text[2:4] + ':' + self.root.get_screen("second").ids.add_time.text[4:6]
        
        else:
            pass

MainApp().run()
