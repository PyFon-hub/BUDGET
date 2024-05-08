from excel_for_app.marged_and_imported_data import data_for_app
from gui.gui import bank_gui
import tkinter as tk
# Define the input file
input_file = "lista_operacji_240401_240418_202404181243325270.csv"

# Call the data_for_app function
if __name__ == "__main__":
    root = tk.Tk()
    bank_gui(root)
    root.mainloop()
