class Utils:
    def num_from_month(self, month):
        return{
        'January' : 1,
        'February' : 2,
        'March' : 3,
        'April' : 4,
        'May' : 5,
        'June' : 6,
        'July' : 7,
        'August' : 8,
        'September' : 9,
        'October' : 10,
        'November' : 11,
        'December' : 12
        }[month]

    def period_from_month(self, month):
        return{
        'January' : 0,
        'February' : 0,
        'March' : 0,
        'April' : 0,
        'May' : 1,
        'June' : 1,
        'July' : 2,
        'August' : 2,
        'September' : 2,
        'October' : 2,
        'November' : 2,
        'December' : 2
        }[month]
    def tax_returns(self):
        '''Print off all projects in class.
        '''
        for project in self.projects:
            print(project.profit, '\n')
