#!/usr/bin/python2
# -*- coding: utf-8 -*-

import Tkinter as tk
import tkFileDialog
import courses

global srcfiledir
srcfiledir = ''

def selectSource():
    global l12
    global srcfiledir
    srcfiledir = tkFileDialog.askopenfilename()
    if srcfiledir:
        l12.config(text=srcfiledir)

def selectTarget():
    global l22
    global tgtfiledir
    tgtfiledir = tkFileDialog.asksaveasfilename(defaultextension='.cvs')
    if tgtfiledir:
        l22.config(text=tgtfiledir)

def validate(self, action, index, value_if_allowed,
                   prior_value, text, validation_type, trigger_type, widgev_name):
    if text in '0123456789.-+':
        try:
            float(value_if_allowed)
            return True
        except ValueError:
            return False
    else:
        return False

def checkDateStr(title, var):
    global l_state
    try:
        v = int(var)
    except ValueError:
        l_state.config(text='Please input an integer for %s.' % title)
        return None
    return v

def translate():
    global v_year
    global v_month
    global v_day
    global v_weekinfo
    global l_state
    global srcfiledir
    global tgtfiledir
    year = checkDateStr('year', v_year.get())
    month = checkDateStr('month', v_month.get())
    day = checkDateStr('day', v_day.get())
    if not year or not month or not day:
        return
    weekinfo = v_weekinfo.get() != 0
    if not srcfiledir.strip() or not tgtfiledir.strip():
        l_state.config(text='Please select source and target files.')
        return
        
    try:
        courses.translate(srcfiledir, tgtfiledir, (year, month, day), weekinfo)
    except courses.CoursesException as e:
        l_state.config(text=e.msg)
        return

    l_state.config(text='Done.')
    

def main():
    global v_year
    global v_month
    global v_day
    global v_weekinfo
    global l_state
    global l12
    global l22

    top = tk.Tk()
    top.title('THU course xls to calendar converter')

    row = 0
    l11 = tk.Label(text='Source file:')
    l11.grid(row=row, column=0, padx=5, pady=5, sticky=tk.W)
    l12 = tk.Label(text='<Please select a file>')
    l12.grid(row=row, column=1, columnspan=5, padx=5, pady=5, sticky=tk.W)
    b1 = tk.Button(text='Select', command=selectSource )
    b1.grid(row=row, column=6, padx=5, pady=5)

    row = row + 1
    l11 = tk.Label(text='Target file:')
    l11.grid(row=row, column=0, padx=5, pady=5, sticky=tk.W)
    l22 = tk.Label(text='<Please select a file>')
    l22.grid(row=row, column=1, columnspan=5, padx=5, pady=5, sticky=tk.W)
    b2 = tk.Button(text='Select', command=selectTarget )
    b2.grid(row=row, column=6, padx=5, pady=5)

    row = row + 1
    l_date0 = tk.Label(text='Start date:')
    l_date0.grid(row=row, column=0, padx=5, pady=5, sticky=tk.W)
    
    l_year = tk.Label(text='year')
    l_year.grid(row=row, column=1, padx=5, pady=5)
    v_year = tk.StringVar(value='2012')
    e_year = tk.Entry(exportselection=0, width=5, textvariable=v_year)
    e_year.grid(row=row, column=2, padx=5, pady=5)
    
    l_month = tk.Label(text='month', width=5)
    l_month.grid(row=row, column=3, padx=5, pady=5)
    v_month = tk.StringVar(value='9')
    e_month = tk.Entry(exportselection=0, width=3, textvariable=v_month)
    e_month.grid(row=row, column=4, padx=5, pady=5)
    
    l_day = tk.Label(text='day', width=3)
    l_day.grid(row=row, column=5, padx=5, pady=5)
    v_day = tk.StringVar(value='10')
    e_day = tk.Entry(exportselection=0, width=3, textvariable=v_day)
    e_day.grid(row=row, column=6, padx=5, pady=5)
    
    row = row + 1
    v_weekinfo = tk.IntVar()
    v_weekinfo.set(1)
    c_weekinfo = tk.Checkbutton(text="Add week info (events of week-number on every Monday)", variable=v_weekinfo)
    c_weekinfo.grid(row=row, column=0, columnspan=7, padx=5, pady=5)

    row = row + 1
    b_trans = tk.Button(text='Translate!', command=translate )
    b_trans.grid(row=row, column=0, padx=5, pady=5)

    l_state = tk.Label(text='', bd=3)
    l_state.grid(row=row, column=1, columnspan=6, padx=5, pady=5, sticky=tk.W)

    top.mainloop()


main()
