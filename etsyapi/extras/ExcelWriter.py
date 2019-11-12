from extras.WriterAbstractClass import WriterAbstractClass
import xlsxwriter


class ExcelWriter(WriterAbstractClass):
    def __init__(self, filename):
        super.__init__()
        # workbook initialization 
        self.xls = xlswriter.workbook(filename)
        self.ws = self.xls.add_worksheet('export')
        self.col = 0
        self.row = 0

    def write_headers(self, headers):
        # reset pointer at top of the file
        col = 0
        row = 0
        while col < len(headers):
            self.ws.write(row, col, header)
            col += 1
        
        # set up the pointer for the first row to be writen 
        self.row = 1
        self.col = 0

    def write_row(self, row_data):
        if isinstance(row_data, dict):
            keys = row_data.keys()
            for key in keys:
                self.ws.write(self.row, self.col, row_data[key])
                self.col += 1

            # Data is written, reset the typewriter
            # and move to the next row
            self.col = 0
            self.row += 1

