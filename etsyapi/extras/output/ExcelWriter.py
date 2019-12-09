from etsyapi.extras.output.WriterAbstractClass import WriterAbstractClass
import xlsxwriter
from importlib import import_module


class ExcelWriter(WriterAbstractClass):
    def __init__(self, filename, model=None):
        WriterAbstractClass.__init__(self)
        # workbook initialization
        self.model = model
        if model is not None:
            modelname = "etsyapi.extras.output.models." + self.model
            self.model = import_module(modelname)

        self.xls = xlsxwriter.Workbook(filename)
        self.worksheets = {}
        self.col = 0
        self.row = 0

    def add_sheet(self, sheet_name=""):
        """Add sheet to workbook and make it the active sheet"""
        if sheet_name in self.worksheets.keys():
            return True
        self.worksheets[sheet_name] = {}
        self.worksheets[sheet_name]["ws"] = self.xls.add_worksheet(sheet_name)
        self.worksheets[sheet_name]["row"] = 0
        self.worksheets[sheet_name]["col"] = 0

    def write_headers(self, headers, sheet_name="", indent=0):
        # TODO Need bettern handing of writing cols
        # reset pointer at top of the file
        col = 0 + indent
        row = 0
        if self.model is not None:
            while col < len(self.model.fields) + indent:
                self.worksheets[sheet_name]["ws"].write(
                    row, col, self.model.fields[col]["field_name"]
                )
                col += 1
        else:
            while col < len(headers) + indent:
                self.worksheets[sheet_name]["ws"].write(row, col, headers[col])
                col += 1

        # set up the pointer for the first row to be writen
        self.worksheets[sheet_name]["row"] = self.worksheets[sheet_name]["row"] + 1
        self.worksheets[sheet_name]["col"] = 0

    def write_row(self, row_data, sheet_name="", indent=0):
        self.worksheets[sheet_name]["col"] = self.worksheets[sheet_name]["col"] + indent

        if isinstance(row_data, dict):
            keys = row_data.keys()
            if self.model is not None:
                for field in self.model.fields:
                    if field["etsy_field"] is None:
                        self.worksheets[sheet_name]["col"] += 1
                        continue
                    for key in keys:
                        if field["etsy_field"] == key:
                            self.worksheets[sheet_name]["ws"].write(
                                self.worksheets[sheet_name]["row"],
                                self.worksheets[sheet_name]["col"],
                                str(row_data[key]),
                            )
                            self.worksheets[sheet_name]["col"] += 1
                            break

                # Data is written, reset the typewriter
                # and move to the next row
                self.worksheets[sheet_name]["col"] = 0
                self.worksheets[sheet_name]["row"] += 1
            else:
                for key in keys:
                    self.worksheets[sheet_name]["ws"].write(
                        self.worksheets[sheet_name]["row"],
                        self.worksheets[sheet_name]["col"],
                        str(row_data[key]),
                    )
                    self.worksheets[sheet_name]["col"] += 1

                # Data is written, reset the typewriter
                # and move to the next row
                self.worksheets[sheet_name]["col"] = 0
                self.worksheets[sheet_name]["row"] += 1

    def __del__(self):
        self.xls.close()
