from intern.emailer import Emailer
from intern.invoice import Invoicer
from intern.utils import Utils

class Intern(Emailer, Invoicer, Utils):
    '''Inheritor class for GIBC digital in-house automation.
    Author: Brandon Wood
    Start Date: 7/10/17
    '''
    def __init__(self):
        self.projects = []

    def blind_run(self, template, tracker, invoice, month, date, email, password):
        '''Automatic payroll and invoice cycle for the month.
        '''
        self.read_projects(template)
        self.assign_account(email, password)
        print('Account Assigned!')
        self.get_employee_days(month)

        for project in self.projects:
            self.generate_invoices(invoice, project, date)

        self.update_budget_tracker(tracker, month)


    def get_employee_days(self, month):
        '''Scrape emails and assign times to each employee object if found.
        '''
        users = self.scrape_times(month)
        # Login errors
        if users is None:
            return
        # Populate days_worked
        for project in self.projects:
            for employee in project.employees:
                check = True
                for user in users:
                    if employee.name == user[0]:
                        employee.data['days_worked'] = user[1]
                        check = False
                        break
                if check:
                    employee.data['days_worked'] = 0

        # Update
        for project in self.projects:
            project.update_expenses()
