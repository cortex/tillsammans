import kivy
kivy.require('1.0.5')

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from kivy.properties import ObjectProperty, StringProperty, NumericProperty
from kivy.uix.listview import ListView
from kivy.network.urlrequest import UrlRequest
from kivy.uix.label import Label
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.image import AsyncImage
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
users = []
import json
from kivy.uix.behaviors import ButtonBehavior
import hashlib

current_user = None
tasks = []

class Task(BoxLayout):
    name = StringProperty()
    points = NumericProperty()
class User(BoxLayout):
    score = NumericProperty()
    name = ObjectProperty()
    email = StringProperty()
    bgcolor = ObjectProperty()
    layout = ObjectProperty()
    avatar = ObjectProperty()

    def on_touch_down(self, ev):
        if self.collide_point(*ev.pos):
            global current_user
            current_user = self
            self.layout.bgcolor = (0.2, 0.2, 0.2, 0.2) 
        else:
            self.layout.bgcolor = (1, 1, 1, 0.2)

    def got_image(self, req, result):
        print result
    def get_image(self):
        m = hashlib.md5()
        m.update(self.email)
        url = "http://www.gravatar.com/avatar/" + m.hexdigest() + ".jpg"
        self.avatar.source = url
 
class Controller(FloatLayout):

    pelle_score = ObjectProperty()
    jocke_score = ObjectProperty()

    tasks = ObjectProperty()
    users = ObjectProperty()

    scores = {"jocke": 0, "pelle": 0}
    current_user = None

    def __init__(self, **kwargs):
        super(Controller, self).__init__(**kwargs)
        UrlRequest(
            'https://glowing-fire-7748.firebaseio.com/users/.json',
            self.got_users)
        UrlRequest(
            'https://glowing-fire-7748.firebaseio.com/tasks/.json',
            self.got_tasks)

    def check_in(self):
        global tasks

        print tasks
        popup = Popup(title='Test popup',
            size_hint=(None, None), size=(400, 400))

        layout = GridLayout(cols=2)
        for task in tasks:
            b = Button(text=task.name)
            b.bind(on_press=popup.dismiss)
            b.bind(on_press=lambda x: self.did_task(task))

            layout.add_widget(b)
        popup.content = layout

        popup.open()



    def did_task(self, task):
        global current_user
        if current_user:
            self.tasks.adapter.data.append("%s %s %s" % (current_user.name, task.name, task.points))
            self.tasks._trigger_reset_populate()
            current_user.score += task.points


    def got_users(self, req, results):
        for key, user in results.items(): 
            u = User(name=user["name"], score=user["score"], email=user["email"])
            u.get_image()
            self.users.add_widget(u)

    def got_tasks(self, req, results):
        global tasks
        for key, task in results.items():
            t = Task(name=task["name"], points=task["points"])
            tasks.append(t)

class ControllerApp(App):

    def build(self):
        return Controller()

if __name__ == '__main__':
    ControllerApp().run()
