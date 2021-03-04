# from nsetools import Nse
# nse = Nse()
# print(nse.get_stock_codes())

class nseClass:
    def __init__(self):
        from nsetools import Nse
        self.nse = Nse()
    def createStockCodeNameCSV(self):
        '''
            Creates a csv with 3 columns
            sl no, stock code name with stock name
        '''
        self.all_stocks = self.nse.get_stock_codes()
        import csv
        with open('nse_code_name.csv', 'w', newline='') as file:
            self.writer = csv.writer(file)
            self.writer.writerow(["SN", "Code", "Name"])
            for i,j in enumerate(self.all_stocks):
              if(i > 0):
                self.writer.writerow([i,j,self.all_stocks[j]])

nse = nseClass()
nse.createStockCodeNameCSV()
