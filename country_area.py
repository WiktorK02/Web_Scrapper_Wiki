from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from bs4 import BeautifulSoup
import re
import requests

class CountryArea(App):
    def build(self):
        # Create a window object with all its widgets
        self.window = GridLayout()
        self.window.cols = 1
        self.window.size_hint = (0.6, 0.7)
        self.window.pos_hint = {"center_x": 0.5, "center_y":0.5}

        # Label
        self.country_name = Label(
                        text= "Enter the name of a country",
                        font_size= 25,
                        color= '#957DAD',
                        bold= True
                        )
        self.window.add_widget(self.country_name)

        # Text input
        self.user = TextInput(
                    multiline= False,
                    padding_y= (20,20),
                    size_hint= (1, 0.5),
                    font_size=30
                    )
        self.window.add_widget(self.user)

        # Button
        self.button = Button(
                      text= "Click",
                      size_hint= (1,0.5),
                      bold= True,
                      background_color ='#957DAD',
                      color="#FFDFD3",
                      font_size = 40
                      )
        
        self.button.bind(on_press=self.callback)
        self.window.add_widget(self.button)

        return self.window

    def callback(self, introduce):
        country = self.user.text
        country_replace = country.replace(' ', '_')
        country_minimalize = country_replace.lower()
        country_upper = re.sub("(^|[_])\s*([a-zA-Z])", lambda p: p.group(0).upper(),country_minimalize)

        if country == "":
            self.country_name.text = 'Invalid country name'
        else:       
            url = "https://pl.wikipedia.org/wiki/" + country_upper
            result = requests.get(url)
            doc = BeautifulSoup(result.text, "html.parser")
            area = doc.find_all(text='Powierzchnia ')
            try:
                parent_area = area[0].parent

                grandparent = parent_area.parent
                paragraph = grandparent.find_all('p')
                text = paragraph[0].text
                text_clean = str(text)
                split_string = text_clean.split('[')
                area_string = split_string[0]
                area_substring = area_string.split('k')
                area_substring_2 = area_substring[0]
                self.country_name.text = "The area of " + str(country_upper.replace('_', ' ')) + " is: " + str(area_substring_2) + " km2"
                self.user.text = ""
            except IndexError:
                self.country_name.text = 'Invalid country name'
                self.user.text = ""

if __name__ == "__main__":
    CountryArea().run()
