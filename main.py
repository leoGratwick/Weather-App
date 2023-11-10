from datetime import datetime
import pytz
import kivy
import kivy.factory
import kivy.properties
import kivy.uix.boxlayout
import kivy.uix.popup
import kivymd.uix.dialog
import kivymd.uix.list
import pandas as pd
import kivymd
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivy.uix.screenmanager import Screen
from kivymd.uix.list import MDList, OneLineListItem, OneLineAvatarListItem, OneLineAvatarIconListItem, CheckboxLeftWidget
from kivymd.uix.button import MDRectangleFlatButton, MDRaisedButton
from enum import Enum
from kivy.lang import Builder
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.image import Image
from kivymd.uix.gridlayout import MDGridLayout
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.anchorlayout import MDAnchorLayout
from kivy.graphics.svg import Svg
from kivymd.uix.card import MDCard
from kivy.core.window import Window
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivymd.uix.dialog import MDDialog
from kivy.uix.scrollview import ScrollView
import scraper
import helper

Window.size = (1000, 500)

locations = [
    "Bristol",
    "London",
    "Singapore",
    "Los Angeles",
    "New York",
    "Glasgow",

]

timezones = {
    "Bristol": "GMT",
    "London": "",
    "Singapore": "",
    "Los Angeles": "",
    "New York": "",
    "Glasgow": ""

}

# weather images
# https://www.metoffice.gov.uk/weather/guides/what-does-this-forecast-mean
# IMAGE CREDIT : https://www.iconfinder.com/weather-icons?category=weather&price=free&style=filled-outline&license=gte__2

overallImg = {
    "Clear night": "Weather_Icons_L/moon_moonlight_night_icon.png",
    "Sunny day": "Weather_Icons_L/sun_sunny_temperature_icon.png",
    "Partly cloudy (night)": "Weather_Icons_L/moon_moonrise_night_icon.png",
    "Sunny intervals": "Weather_Icons_L/clouds_sun_sunny_icon.png",
    "Mist": "Weather_Icons_L/clouds_cloudy_fog_foggy_icon.png",
    "Fog": "Weather_Icons_L/clouds_cloudy_fog_foggy_icon.png",
    "Cloudy": "Weather_Icons_L/cloud_clouds_cloudy_icon.png",
    "Overcast": "Weather_Icons_L/overcast.png",
    "Light shower (night)": "Weather_Icons_L/clouds_moon_night_rain_icon.png",
    "Light shower (day)": "Weather_Icons_L/cloud_drizzel_rain_icon.png",
    "Drizzle": "Weather_Icons_L/cloud_drizzel_rain_icon.png",
    "Light rain": "Weather_Icons_L/rain_shower_storm_icon.png",
    "Heavy shower (night)": "Weather_Icons_L/clouds_moon_night_rain_icon.png",
    "Heavy shower (day)": "Weather_Icons_L/clouds_cloudy_forecast_rain_icon.png",
    "Heavy rain": "Weather_Icons_L/clouds_cloudy_forecast_rain_icon.png",
    "Sleet shower (night)": "Weather_Icons_L/clouds_hail_hailstone_snow_icon.png",
    "Sleet shower (day)": "Weather_Icons_L/clouds_hail_hailstone_snow_icon.png",
    "Sleet": "Weather_Icons_L/clouds_hail_hailstone_snow_icon.png",
    "Hail shower (night)": "Weather_Icons_L/clouds_hail_hailstone_snow_icon.png",
    "Hail shower (day)": "Weather_Icons_L/clouds_hail_hailstone_snow_icon.png",
    "Hail": "Weather_Icons_L/clouds_hail_hailstone_snow_icon.png",
    "Light snow shower (night)": "Weather_Icons_L/moon_night_snow_icon.png",
    "Light snow shower (day)": "Weather_Icons_L/clouds_snow_winter_icon.png",
    "Light snow": "Weather_Icons_L/clouds_snow_winter_icon.png",
    "Heavy snow shower (night)": "Weather_Icons_L/moon_night_snow_icon.png",
    "Heavy snow shower (day)": "Weather_Icons_L/clouds_snow_winter_icon.png",
    "Heavy snow": "Weather_Icons_L/clouds_snow_winter_icon.png",
    "Thunder shower (night)": "Weather_Icons_L/night_rain_storm_icon.png",
    "Thunder shower (day)": "Weather_Icons_L/clouds_night_storm_icon.png",
    "Thunder": "Weather_Icons_L/clouds_night_storm_icon.png",
    "No Icon": "Weather_Icons_L/NoIcon.png"

}


class MainProps(Enum):
    NAME = 0
    OVERALL = 1
    MAXTEMP = 2
    MINTEMP = 3
    UV = 4
    DETAILS = 5


class Props(Enum):
    PRECIPITATION = 1
    TEMP = 2
    WEATHER = 0


class DaysScreen(Screen):

    def add_data(self, data):

        # initialise sections
        self.leftSection = MDBoxLayout(orientation='vertical', size_hint=(0.6, 1))
        self.rightSection = MDBoxLayout(orientation='horizontal', spacing=10, padding=10)

        # today section
        self.leftSection.add_widget(MDLabel(text='Today', halign='center', font_style="H3", size_hint_y=0.5))

        # atempt to find photo for weather conditions
        if data["TODAY"][MainProps.OVERALL.value] in overallImg:
            self.leftSection.add_widget(
                Image(source=overallImg[data["TODAY"][MainProps.OVERALL.value]], fit_mode='contain'))
        else:
            self.leftSection.add_widget(Image(source=overallImg["No Icon"]))

        # current temprature in location
        self.leftSection.add_widget(MDLabel(
            text=data["TODAY"][MainProps.DETAILS.value][data["TODAY"][MainProps.DETAILS.value].columns[0]][
                Props.TEMP.value],
            halign='center', valign='top', font_style="H3", size_hint_y=0.6))

        # other days
        num_days = len(data.columns) - 1
        for i in range(num_days):
            container = MDBoxLayout(orientation='vertical', padding=3)
            container.add_widget(MDLabel(text=data[f"DAY{i + 1}"][MainProps.NAME.value], halign='center'))

            # finds image for weather contidions
            if data["TODAY"][MainProps.OVERALL.value] in overallImg:
                container.add_widget(Image(source=overallImg[data[f"DAY{i + 1}"][MainProps.OVERALL.value]]))
            else:
                container.add_widget(Image(source=overallImg["No Icon"]))

            container.add_widget(
                MDLabel(text=remove_day_night(data[f"DAY{i + 1}"][MainProps.OVERALL.value]), halign='center'))

            # max and min temratures
            tempContainer2 = MDBoxLayout(
                MDLabel(text=data[f"DAY{i + 1}"][MainProps.MAXTEMP.value], halign='right', font_style="H5"),
                MDLabel(text=data[f"DAY{i + 1}"][MainProps.MINTEMP.value], halign='left'),
                size_hint_x=1.2,
                pos_hint={'center_x': 0.6, 'center_y': 0.5},
                spacing=10
            )

            # Add section to right section
            container.add_widget(tempContainer2)
            card = MDCard(size_hint_y=0.95,
                          pos_hint={'center_x': 0.5, 'center_y': 0.5},
                          shadow_softness=7, shadow_offset=(0, 1.3), focus_behavior=True, elevation=2
                          )
            card.add_widget(container)
            self.rightSection.add_widget(card)

        # puts both left and right screens together and then adds to the screen
        self.mainLayout = MDBoxLayout(self.leftSection, self.rightSection, orientation='horizontal')
        self.add_widget(self.mainLayout)


class DetailsScreen(Screen):
    pass


class PopupBox(Popup):
    pass


class LocationList(MDList):
    def add_location(self, name):
        self.add_widget(OneLineListItem(
            text=name
        ))


class ItemConfirm(OneLineAvatarIconListItem):
    divider = None

    def set_icon(self, instance_check):
        instance_check.active = True
        check_list = instance_check.get_widgets(instance_check.group)
        for check in check_list:
            if check != instance_check:
                check.active = False




def remove_day_night(s):
    s = s.replace("(day)", "").replace("(night)", "").strip()
    return s

def get_date_time(location):
    return datetime.now(pytz.timezone(timezones[location]))

class MyApp(MDApp):
    location = ObjectProperty()

    def build(self):
        try:
            f = open("default_locatiion.txt", "r")
            self.location = f.read().strip()
        except:
            self.location = "Singapore"

        self.data = scraper.scrape(self.location)
        self.loadedData = {}
        self.loadedData[self.location] = self.data
        self.mode = "Days"
        self.title = "Weather App"
        self.theme_cls.primary_palette = "DeepPurple"
        self.theme_cls.primary_hue = '400'
        # self.theme_cls.theme_style = "Dark"

        return Builder.load_string(helper.helper)

    def on_start(self):
        #  adds all locations to nav drawer
        for city in locations:
            listItem = OneLineListItem(
                text=city,
                on_press=lambda x: self.changeLocation(x.text)
            )
            self.root.ids.locationNav.add_widget(listItem)

        # creates day screen
        if self.mode == "Days":
            self.createDayScreen()

        # refreshes the page every 5 mins
        Clock.schedule_interval(lambda dt: self.refresh(), 300)

    def changeLocation(self, city):

        # changes location, scrapes new location
        self.changeTitle(city)
        if city in self.loadedData:
            self.data = self.loadedData[self.location]
        else:
            self.data = scraper.scrape(self.location)
            self.loadedData[self.location] = self.data

        # deleted old day sceen and add new one
        self.root.ids.body.remove_widget(self.root.ids.body.children[0])
        self.createDayScreen()

    def changeTitle(self, city):
        # changes navbar title
        self.root.ids.headerBar.title = city
        self.location = city
        self.root.ids.nav_drawer.set_state("closed")

    def createDayScreen(self):

        # create screen
        screen = DaysScreen(name='dayScreen')
        # add data to screen
        screen.add_data(self.data)
        # add screen to the body of app
        self.root.ids.body.add_widget(screen)

    def refresh(self):
        print("reshereshing")

        self.data = scraper.scrape(self.location)
        self.loadedData[self.location] = self.data
        self.root.ids.body.children[0].clear_widgets()
        self.root.ids.body.children[0].add_data(self.data)
        # self.show_popup()
        # close_button = MDRectangleFlatButton(text="Close", on_release=self.close_dialog)
        # self.dialog = kivymd.uix.dialog.MDDialog(title='Weather Updated', text='yippee!',
        #                                          buttons=[close_button]
        #                                          )
        # self.dialog.open()

        # self.pop_up.dismiss()

    def show_popup(self):
        self.pop_up = kivy.factory.Factory.PopupBox()
        self.pop_up.open()

    def close_dialog(self, obj):
        self.dialog.dismiss()

    def set_default_location(self):
        close_button = MDRaisedButton(text="Cancel", on_release=self.close_dialog)
        save_button = MDRectangleFlatButton(text="Save", on_release=self.close_dialog)
        save_button.bind(on_release=lambda x: self.save_default_location())

        location_list = MDList()
        List = []

        for city in locations:
            listItem = ItemConfirm(
                text=city,
            )

            List.append(listItem)

        self.dialog = None
        if not self.dialog:
            self.dialog = MDDialog(title='Select A Default Location',
                                   type="simple",
                                   items=List,
                                   buttons=[save_button, close_button],
                                   auto_dismiss=False
                                   )

        self.root.ids.nav_drawer.set_state("closed")
        self.dialog.open()

    def on_checkbox_active(self, checkbox, value, text):

        if value:
            self.default_location = text
        else:
            self.default_location = None


        print(self.default_location)

    def save_default_location(self):
        print("here")
        if self.default_location:
            f = open("default_locatiion.txt", "w")
            f.write(self.default_location)
            f.close()



if __name__ == '__main__':
    MyApp().run()
