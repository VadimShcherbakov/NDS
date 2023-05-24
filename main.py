import tkinter as tk
from tkinter import ttk, Frame, messagebox
from functools import partial
from lexicon.lexicon_ru import LEXICON_RU
from services.services import read_json
from services.word import Naryad
from services.calendar import create_calendar, date_dict, InputDataError


# функция для добавления членов бригады
set_brigade_members = set()
guide=read_json("data/guide.json")


def check_input(key_value, check_value):
    if len(check_value) > 0 and check_value[-1]:
        return check_value
    raise InputDataError(LEXICON_RU[key_value])


def append_brigade_members() -> list:
    try:
        check_input('manufacturer_works', combo_manufacturer_works.get())
        if combo_brigade_members.get():
            if len(set_brigade_members) >= 4:
                raise InputDataError(LEXICON_RU['error_full_brigade_members'])
            else:
                if combo_head_works.get() != combo_brigade_members.get() != combo_manufacturer_works.get():
                    set_brigade_members.add(combo_brigade_members.get())
                    tk.Label(frame, text=", ".join([w.split(',')[0] for w in list(set_brigade_members)]))\
                        .grid(row=6, column=1, columnspan=2, sticky='e')
                else:
                    raise InputDataError(LEXICON_RU['error_coincidence_brigade_members'])
        else:
            raise InputDataError(LEXICON_RU['error_empty_brigade_members'])
    except InputDataError as er:
        messagebox.showerror(LEXICON_RU['error'], er)


def delete_brigade_members() -> list:
        global  set_brigade_members
        set_brigade_members = set()
        tk.Label(frame, text=LEXICON_RU['space']).grid(row=6, column=1, columnspan=2, sticky='e')


def check_date():
    if date_dict['date_start'] >= date_dict['date_end']:
        raise InputDataError(LEXICON_RU["error_date_start"])
    elif date_dict['date_issued'] >= date_dict['date_start']:
        raise InputDataError(LEXICON_RU["error_date_issued"])


def user_input() -> None:
    format_date = '%d %m %y'
    format_time = '%H:%M'
    try:
        # append_brigade_members()
        type_naryad = combo_type.get()
        issuing = check_input('issuing', combo_issuing.get())
        if type_naryad == guide['type'][0] and issuing != guide['issuing_fire_naryad']: raise InputDataError(LEXICON_RU['error_issuing_fire_naryad'])
        head_works = combo_head_works.get()
        if head_works in set_brigade_members: raise InputDataError(LEXICON_RU['error_coincidence_brigade_members'])
        manufacturer_works = check_input('manufacturer_works', combo_manufacturer_works.get())
        if manufacturer_works in set_brigade_members: raise InputDataError(LEXICON_RU['error_coincidence_brigade_members'])
        brigade_members = check_input('brigade_members', list(set_brigade_members))
        date_start = date_dict['date_start'].strftime(format_date)
        time_start = date_dict['date_start'].strftime(format_time)
        date_end = check_input('date_end', date_dict['date_end'].strftime(format_date))
        time_end = date_dict['date_end'].strftime(format_time)
        date_issued = check_input('date_issued', date_dict['date_issued'].strftime(format_date))
        time_issued = date_dict['date_issued'].strftime(format_time)
        check_date()


        Naryad(type_naryad=type_naryad,
               issuing=issuing,
               head_works=head_works,
               manufacturer_works=manufacturer_works,
               brigade_members=brigade_members,
               date_start=date_start,
               time_start=time_start,
               date_end=date_end,
               time_end=time_end,
               date_issued=date_issued,
               time_issued=time_issued
              ).record_word()
        frame.destroy()
    except InputDataError as er:
        messagebox.showerror(LEXICON_RU['error'], er)
    except AttributeError as ker:
        messagebox.showerror(LEXICON_RU['error'], LEXICON_RU["all_date"])


# ----------Создаём окно приложения----------
frame = tk.Tk()
frame.title(LEXICON_RU['name_table'])  # добавляем название приложения.
frame.geometry('500x400')
for c in range(3): frame.columnconfigure(index=c, weight=1)
for r in range(11): frame.rowconfigure(index=r, weight=1)


# ----------Создаём 1 блок----------
tk.Label(frame, text=LEXICON_RU['type'], justify=tk.LEFT).grid(row=0, column=1, sticky='w')

combo_type = ttk.Combobox(frame, values=guide['type'])

combo_type.grid(row=0, column=2)
# combo_type.current(0)

# ----------Создаём 2 блок----------
tk.Label(frame, text=LEXICON_RU['issuing']).grid(row=1, column=1, sticky='w')

combo_issuing = ttk.Combobox(frame, values=sorted(guide['issuing']))

combo_issuing.grid(row=1, column=2)
# combo_issuing.current(1)
#
# ----------Создаём 3 блок----------
tk.Label(frame, text=LEXICON_RU['head_works']).grid(row=2, column=1, sticky='w')

combo_head_works = ttk.Combobox(frame, values=sorted(guide['head_works']))

combo_head_works.grid(row=2, column=2)
# combo_head_works.current(2)

# ----------Создаём 4 блок----------
tk.Label(frame, text=LEXICON_RU['manufacturer_works']).grid(row=3, column=1, sticky='w')

combo_manufacturer_works = ttk.Combobox(frame, values=sorted(guide['manufacturer_works']))

combo_manufacturer_works.grid(row=3, column=2)
# combo_manufacturer_works.current(3)

# ----------Создаём 5 блок----------
tk.Label(frame, text=LEXICON_RU['brigade_members']).grid(row=4, column=1, sticky='w')

combo_brigade_members = ttk.Combobox(frame, values=sorted(guide['brigade_members']))

combo_brigade_members.grid(row=4, column=2)
# combo_brigade_members.current(4)

# ----------добавим кнопку, которая будет добавлять членов бригады---------
cal_brigade_members = tk.Button(frame, text=LEXICON_RU['cal_brigade_members'], command=append_brigade_members)
cal_brigade_members.grid(row=5, column=2)

# ----------добавим кнопку, которая будет удалять всех членов бригады---------
cal_brigade_members = tk.Button(frame, text=LEXICON_RU['cal_del_brigade_members'], command=delete_brigade_members)
cal_brigade_members.grid(row=5, column=1, sticky='w')

# ----------добавим кнопку, которая вводить дату начала работы---------
cal_data_start = tk.Button(frame, text=LEXICON_RU['date_start'], command=partial(create_calendar, 'date_start', 7, 2))
cal_data_start.grid(row=7, column=1, sticky='w')

# ----------добавим кнопку, которая вводить дату окончания работ---------
cal_data_start = tk.Button(frame,text=LEXICON_RU['date_end'], command=partial(create_calendar, 'date_end', 8, 2))
cal_data_start.grid(row=8, column=1, sticky='w')
# ----------добавим кнопку, которая вводить дату выдачи наряда---------
cal_data_start = tk.Button(frame,text=LEXICON_RU['date_issued'], command=partial(create_calendar, 'date_issued', 9, 2))
cal_data_start.grid(row=9, column=1, sticky='w')
# ----------добавим кнопку, которая будет запускать заполнение наряда---------
cal_btn = tk.Button(frame, text=LEXICON_RU['cal_btn'], command=user_input)
cal_btn.grid(row=10, column=2)




# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    frame.mainloop()


