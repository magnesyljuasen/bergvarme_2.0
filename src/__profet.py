import pandas as pd
import numpy as np
import xlwings as xw
import pythoncom

class Profet:
    def __init__ (self):
        self.filplassering = "profet.xlsm"
        self.air_temperature = np.zeros(8760)
        self.area = int
        
    def start_calculation(self):
        pythoncom.CoInitialize()
        app = xw.App(visible=False)
        workBook = xw.Book(self.filplassering)
        sht = workBook.sheets[1]
        sht.range ('E4').value = [[self.air_temperature[i]] for i in range(0, len(self.air_temperature))]
        sht.range ('W4').value = self.area
        makro = workBook.macro ("module1.main")
        makro()
        df = sht.range('A3').expand().options(pd.DataFrame).value
        workBook.close()
        self.space_heating_h = df['Space heating hourly [kW]'].to_numpy()
        self.dhw_h = df['DHW hourly [kW]'].to_numpy()
