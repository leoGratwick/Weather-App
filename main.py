import pandas as pd
import kivymd
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivy.uix.screenmanager import Screen
from kivymd.uix.list import MDList, OneLineListItem
from kivymd.uix.button import MDRectangleFlatButton
from enum import Enum
from kivy.lang import Builder
from kivymd.uix.boxlayout import MDBoxLayout
import scraper
import helper

locations = [
    "Bristol",
    "London",
    "Singapore",
    "Los Angeles",
    "New York",
    "Glasgow"
             ]


class MainProps(Enum):
    NAME = 0
    OVERALL = 1
    MAXTEMP = 2
    MINTEMP = 3
    DETAILS = 4


class Props(Enum):
    PRECIPITATION = 0
    TEMP = 1
    WEATHER = 2


class DaysScreen(Screen):

    def add_data(self, data):
        self.leftSection = MDBoxLayout(orientation='vertical', size_hint=(0.6,1))
        self.rightSection = MDBoxLayout(orientation='horizontal')
        # today
        self.leftSection.add_widget(MDLabel(text='Today', halign='center'))
        self.leftSection.add_widget(MDLabel(text= data["TODAY"][MainProps.OVERALL.value], halign='center'))
        self.leftSection.add_widget(MDLabel(text= data["TODAY"][MainProps.MAXTEMP.value], halign='center'))
        self.leftSection.add_widget(MDLabel(text=data["TODAY"][MainProps.MINTEMP.value], halign='center'))

        #other days
        num_days = len(data.columns) -1
        for i in range(num_days):
            container = MDBoxLayout(orientation='vertical')
            container.add_widget(MDLabel(text=data[f"DAY{i+1}"][MainProps.NAME.value], halign='center'))
            container.add_widget(MDLabel(text=data[f"DAY{i+1}"][MainProps.OVERALL.value], halign='center'))
            container.add_widget(MDLabel(text=data[f"DAY{i+1}"][MainProps.MAXTEMP.value], halign='center'))
            container.add_widget(MDLabel(text=data[f"DAY{i+1}"][MainProps.MINTEMP.value], halign='center'))

            self.rightSection.add_widget(container)


        self.mainLayout = MDBoxLayout(orientation='horizontal')
        self.mainLayout.add_widget(self.leftSection)
        self.mainLayout.add_widget(self.rightSection)
        self.add_widget(self.mainLayout)

        print("Data added")





class DetailsScreen(Screen):
    pass

class LocationList(MDList):
    def add_location(self, name):
        self.add_widget(OneLineListItem(
            text=name
        ))

class MyApp(MDApp):
    def build(self):
        self.location = "Bristol"
        self.data = scraper.scrape(self.location)
        self.title = "Weather App"
        self.theme_cls.theme_style = "Dark"

        return Builder.load_string(helper.helper)

    def on_start(self):

        for city in locations:
            listItem = OneLineListItem(
                text=city,
                on_press=lambda x: self.changeLocation(x.text)
            )
            self.root.ids.locationNav.add_widget(listItem)

        self.createDayScreen()


    def changeLocation(self, city):
        self.changeTitle(city)
        self.data = scraper.scrape(self.location)
        self.root.ids.body.remove_widget(self.root.ids.body.children[0])
        self.createDayScreen()


    def changeTitle(self,city):
        self.root.ids.headerBar.title = city
        self.location = city
        self.root.ids.nav_drawer.set_state("closed")

    def createDayScreen(self):
        screen = DaysScreen(name='dayScreen')
        screen.add_data(self.data)
        print(screen)
        # self.root.ids.body.add_widget(MDLabel(text='bello'))
        # self.root.ids.body.add_widget(MDLabel(text='bello2'))
        self.root.ids.body.add_widget(screen)
        print("added day screen")


if __name__ == '__main__':
    MyApp().run()

