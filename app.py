from tkinter import *
from intern.intern import Intern

class App(Tk):
    def greetings(self):
        ''' Test button clicks.
        '''
        print('mic check, 1, 2, and three')

    def clear_view(self):
        try:
            self.active.destroy()
        except:
            pass

    def init_intern(self):
        ''' Add intern to root to be accessed later.
        '''
        self.intern = Intern()

    def remove_attribute(self, label, item):
        self.labels.remove(label)
        item.destroy()

    def add_attribute_label(self, frame, text):
        item = Frame(frame)
        Label(item, text = text).pack(side = LEFT)
        Button(item, text = 'x', command = lambda: self.remove_attribute(text, item)).pack(side = LEFT)
        item.pack()


    def add_attribute(self, auto, attribute):
        self.labels.append(attribute)
        item = Frame(auto)
        Label(item, text = attribute).pack(side = LEFT)
        Button(item, text = 'x', command = lambda: self.remove_attribute(attribute, item)).pack(side = LEFT)
        item.pack()
    
    def add_title(self, label, title):
        self.subject_title = title
        label.config(text = 'Subject title: ' + title)

    def get_data(self):
        data = self.intern.scrape_attributes(self.labels, self.subject_title)
        self.intern.dump_fields(self.labels, data)

    def login(self, login_pannel, un, pw):
        self.intern.assign_account(un, pw)
        self.login_status = True
        Label(login_pannel, text = "Logged in!").grid(row = 0, column = 1)

    def load_home_frame(self):
        self.clear_view()
        home = Frame(self)
        Label(home, text = "Welcome! I promise I'll add something interesting here eventually.").grid(row = 1, column = 1)

        home.grid(row = 0, column = 0)
        self.active = home

    def load_login_frame(self):
        self.clear_view()
        # Login Pannel and components.
        login_pannel = Frame(self)

        login_label = Label(login_pannel, text = 'Login Here!').grid(row = 2, column = 1)
        usernameLabel = Label(login_pannel)

        username = Entry(login_pannel)
        username.grid(row = 3, column = 1)

        password = Entry(login_pannel, show = '*')
        password.grid(row = 3, column = 2)

        login_button = Button(login_pannel, text = 'Login', command = lambda: self.login(login_pannel, username.get(), password.get())).grid(row = 4, column = 1)
        login_pannel.grid(column = 0, row = 0)

        self.active = login_pannel

    def load_automation_frame(self):
        ''' Load frame with automation functionalities.
        '''
        auto = Frame(self)
        self.clear_view()

        if self.login_status:
            Label(auto, text = "You're logged in!").pack()

        cmd = Frame(auto)
        Label(cmd, text="Input attributes here").pack()
        attribute = Entry(cmd)
        attribute.pack(side = LEFT)
        Button(cmd, text = "Add", command = lambda: self.add_attribute(auto, attribute.get())).pack(side = LEFT)
        cmd.pack()

        subjectivo = Frame(auto)
        holder = Label(subjectivo, text='Subject title: ' + self.subject_title)
        Button(subjectivo, text = "Subject title of emails", command = lambda: self.add_title(holder, title.get())).pack(side = LEFT)
        title = Entry(subjectivo)
        title.pack(side = LEFT)
        holder.pack(side = LEFT)
        subjectivo.pack()

        bang = Frame(auto)
        Button(bang, text = "Scrape", command = lambda: self.get_data()).pack()
        bang.pack()

        for label in self.labels:
            self.add_attribute_label(auto, label)

        auto.pack()
        self.active = auto

    def run(self):
        '''Open and run app.
        '''
        # Initialize object.
        self.iconbitmap('favicon.ico')
        self.wm_title(' GIBC Digital Automation Suite')
        self.minsize(width = 100, height = 100)
        self.init_intern()
        self.load_home_frame()
        self.login_status  = False
        self.labels = []
        self.subject_title = ''
        self.intern.email = ''
        self.intern.password = ''

        # Initialize main menu
        MainMenu = Menu(self)
        MainMenu.add_command(label = 'Automation', command = self.load_automation_frame)
        MainMenu.add_command(label = 'Home', command = self.load_home_frame)
        MainMenu.add_command(label = 'Login', command = self.load_login_frame)


        self.config(menu = MainMenu)
        self.mainloop()


if __name__ == '__main__':
    app = App()
    app.run()
