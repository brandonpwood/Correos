from openpyxl import Workbook

import email
import imaplib
import time

from bs4 import BeautifulSoup as bs4

class Emailer():
    '''Parent class for intern containing all the methods for logging in and
    scraping data from emails. Requires the class has an email and a password
    property to login.
    '''

    def scrape_attributes(self, attributes, subject_title):
        '''
        Scrapes emails for each attribute in an array.
        :param attributes:
        Array of strings, and string with subject title of email.
        :return:
        array of groups of fields from attributes for each email.
        '''
        # Resolve login errors
        if self.email is None or self.password is None:
            print("Requires Email and password")
            return None
        # Login and get ready to store data.
        server = self.login()
        data = []

        # Scrape email ids.
        print('Processing...')
        status, data = server.search(None, 'ALL' )
        emails  = data[0].split()
        print('This may take a moment as I have found', len(emails), 'emails.')

        # Scrape emails from ids.
        msgs = []

        for num in emails:
            typ, data = server.fetch(num, '(RFC822)')
            msgs.append(email.message_from_bytes(data[0][1]))

        for msg in msgs:
            for part in msg.walk():
                if part.get_content_type() == 'text/html':
                    soup = bs4(str(part), 'lxml')
                    title = soup.find('title')
                    if title:
                        if title.get_text() ==  subject_title:
                            point = []
                            for attribute in attributes:
                                if self.get_attr(attribute, soup):
                                    point.append(self.get_attr(attribute, soup))
                            data.append(point)
        print('Finished scraping.')
        return data

    def assign_account(self, email, password):
        '''Assigns email and password. Separate function so email can be used
        only when needed.
        '''
        self.email = email
        self.password = password

    def login(self):
        '''Create and instance of an IMAP4_SSL connection.
        Cleanup is handled by any function that uses it.
        Requires the class has an email and a password property.
        '''
        # Require email and password
        if self.email is None or self.password is None:
            print("Requires Email and password")
            return None

        server = imaplib.IMAP4_SSL('imap.gmail.com')

        server.login(self.email, self.password)
        server.select('INBOX', readonly =  1)

        return server

    def get_attr(self, attr, soup):
        '''Find attribute in form from wordpress email response.
        Pass in the name of the attribute, returns text from that attribute.
        '''

        header = soup.find(text = attr + ':')
        if(header):
            return header.parent.parent.span.get_text()
        return "NOT FOUND"

    def scrape_times(self, month):
        '''Finds and returns times for a particular month.
        Month must by uppercase
        '''
        # Init server.
        server = self.login()

        # Make sure no login error
        if server is None:
            print('Scraping aborted', '\n')
            return

        user_list = []

        print("Processing...")
        status, data = server.search(None, 'ALL')
        emails = data[0].split()
        print('This may take a moment as I have found', len(emails),'emails!')

        msgs = []

        # Scrape Mail
        for num in emails:
            typ, data = server.fetch(num, '(RFC822)')
            msgs.append(email.message_from_bytes(data[0][1]))
        print("Done scraping emails. Begining Parsing...")
        # Scraperino
        for msg in msgs:
            for part in msg.walk():
                if part.get_content_type() == 'text/html':
                    soup = bs4(str(part), 'lxml')
                    title = soup.find('title')
                    if(title):
                        if title.get_text() == 'Form Submission - Time Sheet':
                            found_month = self.get_attr('Month', soup)
                            if month in found_month:
                                user_list.append([self.get_attr('Name', soup), int(self.get_attr('Days Worked', soup)) ])

        print('I found', len(user_list),'employees')
        server.close()

        return user_list
    def scrape_times_with_time(self, month):
        time1 = time.time()
        self.scrape_times(month)
        time2 = time.time()
        print(time1-time2)

    def dump_fields(self, fields, data):
        wb = Workbook()
        ws = wb.active

        data.insert(0, fields)

        row_number = 1
        for point in data:
            for num, cell in enumerate(point):
                ws.cell(row = row_number, column = num + 1, value = cell)
            row_number += 1
        wb.save('Dump.xlsx')
