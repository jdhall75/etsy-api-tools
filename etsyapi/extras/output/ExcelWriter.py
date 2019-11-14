from etsyapi.extras.output.WriterAbstractClass import WriterAbstractClass
import xlsxwriter
from importlib import import_module


class ExcelWriter(WriterAbstractClass):

    def __init__(self, filename, model=None):
        WriterAbstractClass.__init__(self)
        # workbook initialization
        self.model = model
        if model is not None:
            modelname = 'etsyapi.extras.output.models.' + self.model
            self.model =  import_module(modelname)

        self.xls = xlsxwriter.Workbook(filename)
        self.ws = self.xls.add_worksheet('export')
        self.col = 0
        self.row = 0

    def write_headers(self, headers):
        ## TODO Need bettern handing of writing cols
        # reset pointer at top of the file
        col = 0
        row = 0
        if self.model is not None:
            while col < len(self.model.fields):
                self.ws.write(row, col, self.model.fields[col]['field_name'])
                col += 1
        else:
            while col < len(headers):
                self.ws.write(row, col, headers[col])
                col += 1
        
        # set up the pointer for the first row to be writen 
        self.row = 1
        self.col = 0

    def write_row(self, row_data):
        if isinstance(row_data, dict):
            keys = row_data.keys()
            if self.model is not None:
                for field in self.model.fields:
                    if field['etsy_field'] is None:
                        self.col += 1
                        continue
                    for key in keys:
                        if field['etsy_field'] == key:
                            self.ws.write(self.row, self.col, str(row_data[key]))
                            self.col += 1
                            break

                # Data is written, reset the typewriter
                # and move to the next row
                self.col = 0
                self.row += 1
            else:
                for key in keys:
                    self.ws.write(self.row, self.col, str(row_data[key]))
                    self.col += 1

                # Data is written, reset the typewriter
                # and move to the next row
                self.col = 0
                self.row += 1

    def __del__(self):
        self.xls.close()
