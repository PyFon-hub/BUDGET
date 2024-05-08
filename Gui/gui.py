import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from datetime import datetime, timedelta
import csv
import pandas as pd
import os


class bank_gui():
    def __init__(self, root) -> None:

        root.geometry("977x350+104+104")
        root.resizable(False, False)
        self.style = ttk.Style(root)
        

        dir_path = os.path.dirname(os.path.realpath(__file__))
        root.tk.call('source', os.path.join(dir_path, 'forest-light.tcl'))
        root.tk.call('source', os.path.join(dir_path, 'forest-dark.tcl'))

        self.style.theme_use("forest-dark")

        self.frame = ttk.Frame(root)
        self.frame.pack(fill= "both")

        self.frame.columnconfigure(0, weight= 1)
        self.frame.columnconfigure(1, weight= 3)

        self.widgets_frame = ttk.LabelFrame(self.frame, text="", height= 420)
        self.widgets_frame.grid(row=0, column=0, sticky="nswe", pady= 10, padx= 10)

        """
        name_entry = ttk.Entry(widgets_frame)
        name_entry.insert(0, "Name") #Inserts string on index 0 of entry widget
        name_entry.bind("<FocusIn>", lambda e: name_entry.delete("0", "end")) #bind action with function, FocusIn <- when clicked, delete inside form index 0 to the end
        name_entry.grid(row=0, column=0, padx = (5, 30), columnspan= 4, sticky= "we")
        """ 

        #* DATA RANGE
        self.style.configure('my.DateEntry', fieldbackground='red')

        self.date_start_str = ""
        self.date_stop_str = ""

        self.date_range_text = ttk.Label(self.widgets_frame, text= "Date range", font=("Arial", 15))
        self.date_range_text.grid(row = 0, column = 0, columnspan = 2, sticky= "w", padx= 10)

        self.date_range__text_from = ttk.Label(self.widgets_frame, text= "From: ", font=("Arial", 12), width= 5)
        self.date_range__text_from.grid(row = 1, column = 0, sticky= "w", padx= (10, 0), pady= (0,10))

        self.date_range_start = DateEntry(self.widgets_frame, selectmode = "day", style='my.DateEntry')        
        self.date_range_start.grid(row = 1, column = 1, sticky = "w", padx= (0, 20), pady= (0,10))
        self._associate_start_date()
        self.date_range_start.bind("<<DateEntrySelected>>", self._associate_start_date)        

        self.date_range__text_to = ttk.Label(self.widgets_frame, text= "To: ", font=("Arial", 12), width= 5)
        self.date_range__text_to.grid(row = 2, column = 0, sticky= "w", padx= (10, 0), pady= (0,10))

        self.date_stop_str = self.date_start_str + timedelta(days= 30)

        self.date_range_stop = DateEntry(self.widgets_frame, selectmode = "day", style='my.DateEntry')
        self.date_range_stop.set_date(self.date_stop_str)
        self.date_range_stop.grid(row = 2, column = 1, sticky = "w", padx= (0, 20), pady= (0,10))
        self._associate_stop_date()
        self.date_range_stop.bind("<<DateEntrySelected>>", self._associate_stop_date)

        #* GROUP BY
        self.group_by_text = ttk.Label(self.widgets_frame, text= "Group by", font=("Arial", 15))
        self.group_by_text.grid(row = 3, column = 0, columnspan = 2, sticky= "w", padx= 10, pady= (0,10))

        group_by_list = ["None", "Pewnis 1", "Pewnis 2"]
        self.group_by = ttk.Combobox(self.widgets_frame,  values= group_by_list, state= "readonly", width= 15)
        self.group_by.current(0)
        self.group_by.grid(row= 4, column= 0, padx= 20, columnspan= 2, sticky= "w")

        #* Preview button
        self.preview_button = ttk.Button(self.widgets_frame, text= "Preview", width= 10,
                                         command= self._preview_button_func)
        self.preview_button.grid(row= 5, column=0, columnspan= 2, pady= (10,10))

        #* Separator
        separator = ttk.Separator(self.widgets_frame)
        separator.grid(row = 6, column= 0, columnspan= 2, sticky= "we", padx=(10,10), pady= (0,10))

        #* Analysis button
        #analysis_button = ttk.Button()

        #* Format <- theme
        self.theme_toggle = ttk.Checkbutton(self.widgets_frame, style= "Switch", text= "Theme", command= self._toggle_theme)
        self.theme_toggle.grid(row= 7, column= 0, sticky= "w", padx= (10,0), pady= (0, 10))

        #* Korki/Bank
        self.mode_toggle = ttk.Checkbutton(self.widgets_frame, style= "Switch", text= "Bank")
        self.mode_toggle.grid(row= 7, column= 1, sticky= "w", padx= (10,0), pady= (0, 10))

        #* Drag and Drop

        #* EXCEL 
        self.style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Arial', 11))
        self.style.configure("mystyle.Treeview.Heading", font=('Arial', 13,'bold'))

        self.excel_frame = ttk.Frame(self.frame, height= 420)
        self.excel_frame.grid(row= 0, column= 1, padx= (0, 10), pady= (19, 10), sticky= "wens")

        self.excel_scrollbar = ttk.Scrollbar(self.excel_frame)
        self.excel_scrollbar.pack(side= "right", fill= "y")

        cols = ["Data operacji","Opis operacji","Kategoria","Kwota"]

        self.excel_view = ttk.Treeview(self.excel_frame, show= "headings", columns= cols, height= 13,
                                       yscrollcommand= self.excel_scrollbar.set, style= "mystyle.Treeview")
        
        self.excel_view.column(cols[0], width= 100)
        self.excel_view.column(cols[1], width= 200)
        self.excel_view.column(cols[2], width= 200)
        self.excel_view.column(cols[3], width= 100)
        self.excel_view.pack()

        self.excel_scrollbar.config(command= self.excel_view.yview)

    def _toggle_theme(self):
        if self.theme_toggle.instate(["selected"]):
            self.style.theme_use("forest-light")
        else:
            self.style.theme_use("forest-dark")

    def _load_data(self):
        
        path = "../Data/BankData_for_app.csv"
        df = pd.read_csv(path)
        
        df["Data operacji"] = pd.to_datetime(df["Data operacji"]).dt.date
        try:
            mask = (df["Data operacji"] >= self.date_start_str) & (df["Data operacji"] <= self.date_stop_str)
        except Exception as e:
            print(e)
            mask = False

        df = df.loc[mask]

        df = df[["Data operacji","Opis operacji","Kategoria","Kwota", "Waluta"]]

        for col_name in df.columns[:-1]:
            self.excel_view.heading(col_name, text=col_name)

        
        for i in range(df.shape[0]):
            row = df.iloc[i].to_list()
            self.excel_view.insert( '', tk.END, values= row[:-2] + [' '.join(map(str, row[-2:]))] )

    def _preview_button_func(self, event=None) -> None:
        for item in self.excel_view.get_children():
            self.excel_view.delete(item)

        self._load_data()

    def _associate_start_date(self, event=None) -> None:
        self.date_start_str = self.date_range_start.get_date()

    def _associate_stop_date(self, event=None) -> None:
        self.date_stop_str = self.date_range_stop.get_date()


if __name__ == "__main__":
    root = tk.Tk()
    bank_gui(root)
    root.mainloop()

    

