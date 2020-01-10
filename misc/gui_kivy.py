from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

class LoginScreen(GridLayout):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.cols = 2
        self.add_widget(Label(text='Input image'))
        self.username = TextInput(multiline=False)
        self.add_widget(self.username)

        self.add_widget(Label(text='Templates folder'))
        self.password = TextInput(password=True, multiline=False)
        self.add_widget(self.password)

        self.add_widget(Label())
        self.run = Button(text="Run")
        self.add_widget(self.run)
        self.run.join(on_press=)

class TemplateMatcherGUI(App):
    def build(self):
        return LoginScreen()

if __name__ == '__main__':
    TemplateMatcherGUI().run()