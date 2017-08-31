from tkinter import *
from intern.intern import Intern
# from PIL import Image, ImageTK

class App(Tk):
    def greetings(self):
        ''' Test function.
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
        ''' Check users credentials and load login response into frame.
        '''
        self.intern.assign_account(un, pw)
        self.login_status = True

        if self.intern.check_credentials(un, pw):
            Label(login_pannel, text = "Logged in!").grid(row = 0, column = 1)
        else:
            Label(login_pannel, text = "Try again!").grid(row = 0, column = 1)            

    def blind_run(self, template, tracker, invoice, month, date):
        ''' Generates invoice for a particular month.
        '''
        self.intern.blind_run( template, tracker, invoice, month, date, self.intern.email, self.intern.password)


    def load_home_frame(self):
        self.clear_view()
        home = Frame(self)
        Label(home, text = "Welcome! Login above to run payroll or scrape emails.").grid(row = 1, column = 1)

        # image = Image.open("GIBC.jpg")
        # photo = ImageTk.PhotoImage(image)        
        # label = Label(home, image = photo)
        # label.image = photo
        # label.grid(row = 0, column = 1)

        home.grid(row = 0, column = 0)
        # Button(self, text = 'TEST', command = lambda: print(self.intern.check_credentials('intelligence@gibcdigital.com', 'virginia97')) ).grid(row = 5, column = 12)

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

    def load_scraping_frame(self):
        ''' Load frame with scraping functionalities.
        '''
        auto = Frame(self)
        self.clear_view()

        if self.intern.check_credentials(self.intern.email, self.intern.password):
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
        bang.pack()

        for label in self.labels:
            self.add_attribute_label(auto, label)

        Button(auto, text = "Scrape!", command = self.get_data).pack()

        auto.pack()
        self.active = auto

    def load_automation_frame(self):
        ''' Load frame for running full-cycle automation.
        '''
        self.clear_view()
        auto_frame = Frame(self)

        # ADD INPUTS AND BUTTON TO RUN BLIND_RUN AND EVERY OTHER RUN CYCLE
        template = Entry(auto_frame, text = "template")
        tracker = Entry(auto_frame, text = "tracker")
        invoice = Entry(auto_frame, text = "invoice")
        month = Entry(auto_frame, text = "month")
        date = Entry(auto_frame, text = "date")

        blam = Button(auto_frame, text = "Blind_Run", command = lambda: self.blind_run(template.get(), tracker.get(), invoice.get(), month.get(), date.get()))

        Label(auto_frame, text = "template").grid(row = 1, column = 0) 
        template.grid(row = 1, column = 1) 

        Label(auto_frame, text = "tracker").grid(row = 2, column = 0)
        tracker.grid(row = 2, column = 1)

        Label(auto_frame, text = "invoice").grid(row = 3, column = 0)
        invoice.grid(row = 3, column = 1)

        Label(auto_frame, text = "month").grid(row = 4, column = 0) 
        month.grid(row = 4, column = 1) 

        Label(auto_frame, text = "date").grid(row = 5, column = 0)
        date.grid(row = 5, column = 1)
        
        blam.grid(row = 6, column = 1)

        auto_frame.pack()
        self.active = auto_frame

    def run(self):
        '''Open and run app.
        '''
        # Initialize object.
        self.iconbitmap('favicon.ico')
        self.wm_title('GIBC Digital Automation Suite')
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
        MainMenu.add_command(label = 'Scraping', command = self.load_scraping_frame)
        MainMenu.add_command(label = 'Automation', command = self.load_automation_frame)
        MainMenu.add_command(label = 'Home', command = self.load_home_frame)
        MainMenu.add_command(label = 'Login', command = self.load_login_frame)

        self.config(menu = MainMenu)
        self.mainloop()


if __name__ == '__main__':
    app = App()
    app.run()
