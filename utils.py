# -- utils.py - source code description
# This file contains general functions that are repeatedly used in the project.
# Functions: ask_filepath, folder_path, changeStatText, changeTableOfVars, showTokens, clearTab, createScrollbar
# compileWithError
# --
import tkinter as tk
from tkinter import *
from tkinter import filedialog

# Opens a window to ask for the file the user wants to select and returns the filepath
def ask_filepath():
    filepath = filedialog.askopenfilename(title="Select File", filetypes=(("iol", "*.iol"), ("all files", "*.*")))
    return filepath

# Opens a window to ask for the folder the user wants to choose and returns the folder path
def folder_path():
    folder = filedialog.askdirectory()
    return folder

# Changes the text that is displayed in the 'Status' tab
# Gets the label widget and the text to be displayed as parameters
def changeStatText(stat_label, stat_text):
        text = tk.StringVar()
        text.set(stat_text)
        stat_label.config(textvariable=text)

# Changes the variables that are displayed in the table of variables
# Gets the label widget and the text to be displayed as parameters
def changeTableOfVars(table_of_vars_label, variables):
    temp = 'Variables Used:\n'
    for i in variables:
        temp = temp + i[0] + ' ' + i[1] + '\n'
        
    text = tk.StringVar()
    text.set(temp)
    table_of_vars_label.config(textvariable = text, justify=LEFT)

# Shows the tokenized code in the 'Tokenized Code' tab
# Gets the text widget and tokens to be displayed
def showTokens(tokenized_text, tokens):
    text = ''
    for i in tokens:
        text += i
    clearTab(text=tokenized_text, state='N') # Clears the tab
    tokenized_text.insert(INSERT, text) # Displays the tokenized code
    tokenized_text.configure(state=DISABLED) # Disables text area so that it can't be edited

# Clears a text area
# The first parameter gets the text widget and the state determines if the text area must be disabled after clearing the
# text area
def clearTab(text, state):
    # If state is 'N', it means that the text widget will not be disabled after clearing the text area
    if state == 'N':
        text.configure(state=NORMAL)
        text.delete('1.0', END)
    # If state is 'ND', it means that the text widget will be disabled after clearing the text area 
    # so that it can't be edited
    elif state == 'ND':
        text.configure(state=NORMAL)
        text.delete('1.0', END)
        text.configure(state=DISABLED)

# Creates a scrollbar for a text widget
# Gets the frame or window where the scrollbar will be placed and gets the text widget that the scrollbar will be 
# connected to
def createScrollbar(text_tab, textarea):
    scroll = Scrollbar(
            text_tab, orient='vertical', command=textarea.yview)
    scroll.grid(column=1, row=0, sticky=NS)
    textarea['yscrollcommand'] = scroll.set

# If the tokenized lexemes contains an error, it will display a message and all the error lexemes.
# It gets the text widget and the list of error lexemes to display.
def compileWithError(compile_text, errors, saved_code, input):
    text = ''
    clearTab(compile_text, 'N')
    if saved_code != input:
        compile_text.insert(INSERT, "COMPILATION CANNOT PROCEED DUE TO ERROR LEXEMES. WARNING: YOU HAVE NOT SAVED YOUR CODE\n===========\n")
    compile_text.insert(INSERT, "Input file has been successfully tokenized, but it contains error lexemes.Please see the lines with errors below:\n\n")
    for i in errors:
        text = text + 'Line ' + str(i[2]) + ' ' + str(i[1]) + '\n' # gets the line number and error
    compile_text.insert(INSERT, text) # Displays the line number and error
    compile_text.configure(state=DISABLED)