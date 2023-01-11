from tkinter import *
from time import strftime
import time
import datetime as d
from tkinter import messagebox
from tkinter import filedialog
from tkinter import font
import os, webbrowser
import os
from tkinter.colorchooser import *
import calendar as c
class TextEditor():
	def __init__(self, root):
		self.root = root
		self.TITLE = "TkInter 편집기"
		self.file_path = None
		self.set_title()
		frame = Frame(root)
		self.xscrollbar = Scrollbar(frame, orient='horizontal')
		self.xscrollbar.pack(side='bottom', fill='x')
		self.yscrollbar = Scrollbar(frame)
		self.yscrollbar.pack(side='right', fill='y')
		self.editor = Text(frame, xscrollcommand=self.xscrollbar.set)
		self.xscrollbar.config(command=self.editor.xview)
		self.editor = Text(frame, yscrollcommand=self.yscrollbar.set)
		self.yscrollbar.config(command=self.editor.yview)
		self.editor.pack(side= "left", expand=1, fill="both")
		self.editor.config(wrap="none", undo=True, width=80, font=("Helvetica", 14))
		self.editor.focus()
		wp = 5
		frame.pack(fill="both", expand=1)
		root.protocol("WM_DELETE_WINDOW", self.file_quit)
		self.make_menu()
		self.bind_events()

	def make_menu(self):
		self.menubar = Menu(root)
		fmenu = Menu(self.menubar, tearoff=0)
		fmenu.add_command(label="New", command=self.file_new, accelerator="Ctrl+N")
		fmenu.add_command(label="Open...", command=self.file_new, accelerator="Ctrl+O")
		fmenu.add_separator()
		fmenu.add_command(label="Save", command=self.file_new, accelerator="Ctrl+S")
		fmenu.add_command(label="Save As", command=self.file_new, accelerator="Ctrl+Alt+S")
		fmenu.add_command(label="Exit", command=self.file_new, accelerator="Ctrl+Q")
		self.menubar.add_cascade(label="File", menu=fmenu)
		emenu = Menu(self.menubar, tearoff = 0)
		emenu.add_command(label="Undo", command=self.edit_undo)
		emenu.add_command(label="Redo", command=self.edit_redo)
		emenu.add_separator()
		emenu.add_command(label="Cut", command=self.edit_cut)
		emenu.add_command(label="Copy", command=self.edit_copy)
		emenu.add_command(label="Paste", command=self.edit_paste)
		emenu.add_command(label="Delete", command=self.edit_delete)
		emenu.add_command(label="Select All", command=self.edit_select_all)
		emenu.add_separator()
		emenu.add_command(label="Clock", command=self.edit_clock)
		emenu.add_command(label="Time", command=self.edit_time)
		self.menubar.add_cascade(label="Edit", menu=emenu)

		smenu = Menu(self.menubar, tearoff = 0)
		smenu.add_command(label="Background", command = self.tools_background)
		smenu.add_command(label="Foreground", command = self.tools_foreground)
		smenu.add_separator()
		smenu.add_command(label="Algerian", command = self.tools_algerian)
		smenu.add_command(label="Arial", command = self.tools_arial)
		smenu.add_command(label="Courier", command = self.tools_courier)
		smenu.add_command(label="Cambria", command = self.tools_cambria)
		smenu.add_command(label="BoldDoc", command = self.tools_bolddoc)
		smenu.add_separator()
		smenu.add_command(label="Reset", command=self.tools_reset)
		smenu.add_command(label="Calculator", command=self.tools_calculator)
		self.menubar.add_cascade(label="Tools", menu=smenu)

		tmenu = Menu(self.menubar, tearoff = 0)
		self.word_wrap = BooleanVar()
		self.bar = BooleanVar()
		tmenu.add_checkbutton(label="Word Wrap", onvalue=True, offvalue=False, variable=self.word_wrap, command=self.format_word_wrap)
		self.menubar.add_cascade(label="Format", menu=tmenu)



		hmenu = Menu(self.menubar, tearoff=0)
		hmenu.add_command(label="TkEditor 편집기", command=self.help_showabout)
		hmenu.add_command(label="Homepage", command=self.help_homepage)
		self.menubar.add_cascade(label="Help", menu=hmenu)


                
                


		root.config(menu=self.menubar)


	def save_if_modified(self):
		if self.editor.edit_modified():
			caption = "저장 확인"
			msg = "이 파일은 수정됐습니다. 저장하시겠습니까?"
			response = messagebox.askyesnocancel(caption, msg)
			if response:
				result = self.file_save()
				if result == "saved":
					return True
				else:
					return None
			else:
				return response
		else:
			return True
	def file_new(self, event= None):
		result = self. save_if_modified()
		if result != None:
			self.editor.delete(1.0, "end")
			self.editor.edit_modified(False)
			self.editor.edit_reset()
			self.file_path = None
			self.set_title()
	def file_open(self, event=None, filepath=None):
		def readfile(filepath):
			try:
				with open(filepath, encoding="utf-8") as f:
					fileContents = f.read()
			except FileNotFoundError as e:
				print(e)
				print(" 파일 읽기 실패! ".center(30, '*'))
			else:
				self.editor.delete(1.0, "end")
				self.editor.insert(1.0, fileContents)
				self.editor.edit_modified(False)
				self.file_path = filepath
				print(" 파일 읽기 완료:".center(30, "*"))
				result = self.save_if_modified()
				if result != None:
					if filepath == None:
						filepath = filedialog.askopenfilename()
						if filepath != None and filepath != '':
							readfile(filepath)
							self.set_title()
	def file_save(self, event=None):
		if self.file_path == None:
			result = self.file_save_as()
		else:
			result = self.file_save_as(filepath=self.file_path)
		return result

	def file_save_as(self, event=None, filepath=None):
		if filepath == None:
			ftypes = (("Text file", "*.txt"), ("Python files", "*.py *.pyw"), ("All files", "*.*"))
			filepath = filedialog.asksaveasfilename(filetypes = ftype)
			text = self.editor.get(1.0, "end-1c")
			try:
				with open(filepath, "wb") as f:
					f.write(bytes(text, "UTF-8"))
			except FileNotFoundError as e:
				print(e)
				print(" 파일 쓰기 실패! ".center(30, '*'))
				return "cancelled"
			else:
				self.editor.edit_modified(False)
				self.file_path = filepath
				self.set_title()
				return "saved"

	def file_quit(self, event=None):
		result = self.save_if_modified()

		if result != None:
			self.root.destroy()
	def edit_delete(self, event=None):
		try:
			self.editor.delete(SEL_FIRST, SEL_LAST)

		except TclError:
			pass

	def edit_cut(self, event=None):
		self.editor.event_generate("<<Cut>>")

	def edit_copy(self, event=None):
		self.editor.event_generate("<<Copy>>")

	def edit_paste(self, event=None):
		self.editor.event_generate("<<Paste>>")

	def edit_select_all(self, event=None):
		self.editor.tag_add(SEL, "1.0", END)
		self.editor.mark_set(INSERT, END)
		self.editor.see(INSERT)

   
	def edit_time(self):
		now = time.strftime("%Y-%m-%d %H:%M:%S")
		self.editor.insert(END, now)


	def help_showabout(self, event=None):
		messagebox.showinfo("TkInter 편집기", "TkInter 편집기 버전 0.1")

	def help_homepage(self):
		webbrowser.open_new("https://www.python.org/psf-landing/")

	def set_title(self, event=None):
		if self.file_path != None:
			title = os.path.basename(self.file_path)
		else:
			title = "Untitled"
		self.root.title(title + " - " + self.TITLE)

	def edit_undo(self, event=None):
		self.editor.edit_undo()
	def edit_redo(self, event=None):
		self.editor.edit_redo()

	def format_word_wrap(self):
		if self.word_wrap.get() == True:
			self.editor.config(wrap="word")
		else:
			self.editor.config(wrap="none")



	def tools_background(self):
		color = askcolor()
		print(color[1])
		self.editor.configure(background = color[1])

	def tools_foreground(self):
		color = askcolor()
		print(color[1])
		self.editor.configure(foreground = color[1])

	def tools_reset(self):
		self.editor.configure(bg = 'white', fg = 'black', font=("Helvetica", 14))
		root.geometry("800x600")
		self.editor.delete('1.0',END)

	def tools_algerian(self):
		global editor
		self.editor.configure(font="Algerian")

	def tools_arial(self):
		global editor
		self.editor.configure(font="Arial")

	def tools_courier(self):
		global editor
		self.editor.configure(font="Courier")

	def tools_cambria(self):
		global editor
		self.editor.configure(font="Cambria")

	def tools_bolddoc(self):
		global editor
		self.editor.configure(font=('arial',14,'bold'))

	def tools_calculator(self):
		window = Tk()
		window.title("My Calculator")
		display = Entry(window, width=33, bg="yellow")
		display.grid(row=0, column=0, columnspan=5)

		button_list = [
		'7', '8', '9', '/', 'C',
		'4', '5', '6', '*', '',
		'1', '2', '3', '-', '',
		'0', '.', '=', '+', '']

		row_index = 1
		col_index = 0
		for button_text in button_list:
			Button(window, text=button_text, width=5).grid(row=row_index, column=col_index)
			col_index += 1
			if col_index > 4:
				row_index += 1
				col_index = 0

		def click(key):
			if(key == "="):
				result = eval(display.get())
				s = str(result)
				display.insert(END,"="+s)
			else:
				display.insert(END, key)

		row_index = 1
		col_index = 0

		for button_text in button_list:
			def process(t=button_text):
				click(t)
			Button(window, text=button_text, width=5,
			     command=process).grid(row=row_index, column=col_index)
			col_index += 1
			if col_index > 4:
				row_index += 1
				col_index = 0

		window.mainloop()
		

	def edit_clock(self):
		root = Tk()
		root.title('Clock')
		def time():
			string = strftime('%H:%M:%S %p')
			lbl.config(text = string)
			lbl.after(1000, time)

		lbl = Label(root, font = ('calibri', 40, 'bold'),
		            background = 'black',
					foreground = 'white')

		lbl.pack(anchor = 'center')
		time()

		mainloop()	
                 
	def bind_events(self, event=None):
		self.editor.bind("<Control-o>", self.file_open)
		self.editor.bind("<Control-O>", self.file_open)
		self.editor.bind("<Control-S>", self.file_save)
		self.editor.bind("<Control-s>", self.file_save)
		self.editor.bind("<Control-y>", self.file_redo)
		self.editor.bind("<Control-Y>", self.file_redo)
		self.editor.bind("<Control-Z>", self.file_undo)
		self.editor.bind("<Control-z>", self.file_undo)

root = Tk()
root.geometry("800x600")
editor = TextEditor(root)
