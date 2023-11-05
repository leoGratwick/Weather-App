
import kivymd
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel

import scraper


class MyApp(MDApp):
    def build(self):
        return MDLabel(text="Hello World", halign="center")

if __name__ == '__main__':
    # MyApp().run()
    scraper.scrape()

