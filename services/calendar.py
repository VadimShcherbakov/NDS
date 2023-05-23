import datetime
import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar
from datetime import date
from tkinter import messagebox
from lexicon.lexicon_ru import LEXICON_RU


date_dict = {"date_start": [],"date_end": [], "date_issued": [] }


class InputDataError(Exception):
    def __init__(self, data):
        self.data = data

    def __str__(self):
        return repr(self.data)


def create_calendar(name_date, cord_row, cord_col):
    global date_dict
    def grad_date():
        format = '%d.%m.%Y %H:%M'
        list_data = cal.get_date().split("/")
        date = list_data[1]
        month = list_data[0]
        year = '20'+list_data[2]
        try:
            hour = combo_hour.get()
            if not hour:
                raise InputDataError(LEXICON_RU["error_input_time"])
            minutes = combo_minutes.get()
            fin_date = datetime.datetime.strptime(f'{date}.{month}.{year} {hour}:{minutes}', format)
            date_dict[name_date] = fin_date
            lebel_data_start = tk.Label(text=fin_date.strftime('%d %m %y %H:%M'))
            lebel_data_start.grid(row=cord_row, column=cord_col, sticky='w')
            root.destroy()
        except InputDataError as er:
            messagebox.showerror(LEXICON_RU['error'], f"{er}")



    root = tk.Tk()
    root.geometry("400x300")
    for c in range(3): root.columnconfigure(index=c, weight=1)
    for r in range(3): root.rowconfigure(index=r, weight=1)

    current_date = date.today()

    cal = Calendar(root, selectmode='day',
                       year=current_date.year, month=current_date.month,
                       day=current_date.day)

    cal.grid(row=0, column=1)


    combo_hour = ttk.Combobox(root, values=[i for i in range(1, 25)])
    combo_hour.grid(row=1, column=1, sticky='w')
    combo_minutes = ttk.Combobox(root, values=[i for i in range(0, 70, 10)])
    combo_hour.current(0)
    combo_minutes.current(0)
    combo_minutes.grid(row=1, column=1, sticky='e')
    button_time = tk.Button(root,text="Выбрать дату и время", command=grad_date)
    button_time.grid(row=2, column=0, columnspan=3)
    root.mainloop()








