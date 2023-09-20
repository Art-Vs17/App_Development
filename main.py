from kivyauth.google_auth import initialize_google,login_google,logout_google
from kivy.core.window import Window
from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
Window.size = (350,600)
import csv
import bcrypt

class HMDApp(MDApp):
    def build(self):
        client_id=open("client_id.txt")
        client_secret=open("client_secret.txt")
        initialize_google(self.after_login ,self.error_listener ,client_id.read() ,client_secret.read())
        scrn = ScreenManager()
        scrn.add_widget(Builder.load_file('Your.kv'))
        scrn.add_widget(Builder.load_file('login.kv'))
        scrn.add_widget(Builder.load_file('signup.kv'))
        scrn.add_widget(Builder.load_file('home.kv'))
        return scrn

    def after_login(self,name):
        self.root.ids.label.text=f"Logged in as {name}"
        self.root.transition.direction = "left"
        self.root.current = "home"
    def error_listener(self):
        print("Login Failed")

    def login(self):
        login_google()

    def logout(self):
        logout_google(self.after_logout())

    def after_logout(self):
        self.root.ids.label.text = ""
        self.root.transition.direction = "right"
        self.root.current = "home"

    def add_todo(self):
        print("Button Clicked!")

    def signup(self):
        new_email = self.root.get_screen('signup').ids.em.text
        new_password = self.root.get_screen('signup').ids.pswd.text
        hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        with open('users.csv', 'a', newline='') as csvfile:
            fieldnames = ['Email', 'Password']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow({'Email': new_email, 'Password': hashed_password})
        self.root.transition.direction = "left"
        self.root.current = "home"
        print('Sign-up successful!')


    def signin(self):
        entered_email = self.root.get_screen('login').ids.email_field.text
        entered_password = self.root.get_screen('login').ids.password_field.text

        with open('users.csv', newline='') as csvfile:
            csv_reader = csv.DictReader(csvfile)
            for row in csv_reader:
                if entered_email == row['Email']:
                    hashed_password = row['Password']

                    if bcrypt.checkpw(entered_password.encode('utf-8'), hashed_password.encode('utf-8')):
                        self.root.transition.direction = "left"
                        self.root.current = "home"
                        print('Sign-in successful!')
                        return

        print('Sign-in failed. Please check your credentials.')

if __name__ == '__main__':
    HMDApp().run()
        