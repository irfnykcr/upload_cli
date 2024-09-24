from threading import Thread
from tkinter import Tk, Canvas, Entry, Text, Button, filedialog
from tkinter.ttk import Combobox
from json import load
from requests import post
from subprocess import PIPE, Popen
from datetime import datetime

FILE = ""
ACCEPTED_CHR = list("0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZıĞğÜüŞşİÖöÇç-,._()!+-[]{} ")
VIDEO_EXT = [".mp4", ".mov", ".avi", ".wmv", ".mkv", ".webm", ".flv", ".ts"]
PHOTO_EXT = [".jpg", ".jpeg", ".png", ".gif", ".webp"]
TXT_EXT = [".txt"]


try:
	with open("./config/config.json", "r") as f:
		j = load(f)
		CMD = fr"{j['cmd']}"
		API_KEY = j['api_key']
	r = post("https://api.turkuazz.online/upload/get_categories", headers={"api-key":API_KEY})
	CATEGORIES = r.json()
except:
	print("something went wrong. check your api key.")
	exit()

allof = []
for i in CATEGORIES:
	allof.append(f"{i}/")
	for k in CATEGORIES[i]:
		allof.append(f"{i}/{k}/")
		for l in CATEGORIES[i][k]:
			allof.append(f"{i}/{k}/{l}/")

window = Tk()

window.title("upload")
window.iconbitmap(r"./assets/favicon.ico")
width = 900
height = 720
x = (window.winfo_screenwidth() - width) // 2
y = (window.winfo_screenheight() - height) // 2
window.configure(bg = "#181818")
window.geometry(f"900x720+{x}+{y}")

canvas = Canvas(
	window,
	bg = "#181818",
	width = 900,
	height = 720,
	bd = 0,
	highlightthickness = 0,
	relief = "ridge"
)

canvas.place(x = 0, y = 0)


choices = [0,1]
t_private = Combobox(
	window,
	values=choices,
	state="readonly",
)
t_private.place(
	x=416,
	y=306,
	width=350,
	height=24.0
)
t_private.current(0)


choices = ["video","image","txt","other"]
t_type = Combobox(
	window,
	values=choices,
	state="readonly",
)
t_type.place(
	x=416.0,
	y=250,
	width=350,
	height=24.0
)
t_type.current(0)



t_category = Combobox(
	window,
	values=allof,
	state="readonly",
)
t_category.place(
	x=416,
	y=193,
	width=350,
	height=24.0
)
t_category.current(0)



t_about = Entry(
	bd=0,
	bg="#FFFFFF",
	fg="#000000",
	highlightthickness=0,
)
t_about.insert(0, "a file")
t_about.place(
	x=416,
	y=138,
	width=350,
	height=24.0
)



t_filename = Entry(
	bd=0,
	bg="#FFFFFF",
	fg="#000000",
	highlightthickness=0
)
t_filename.insert(0, "filename")
t_filename.place(
	x=416,
	y=82,
	width=350,
	height=24.0
)

def get_file():
	global FILE
	global ACCEPTED_CHR
	global VIDEO_EXT
	global PHOTO_EXT
	global TXT_EXT
	FILE = filedialog.askopenfilename(title="Select file location", filetypes=(("All files", "*.*"),))
	t_fileloc.config(text=FILE)
	t_filename.delete(0, "end")

	filename = FILE.split("/")[-1]
	ext = "." + filename.split(".")[-1]
	if ext in VIDEO_EXT:
		t_type.current(0)
	elif ext in PHOTO_EXT:
		t_type.current(1)
	elif ext in TXT_EXT:
		t_type.current(2)
	else:
		t_type.current(3)
	for i in filename:
		if i not in ACCEPTED_CHR:
			filename = filename.replace(i, "")
			
	t_filename.insert(0, filename)
	return 1
t_fileloc = Button(
	bg="#FFFFFF",
	fg="#000000",
	borderwidth=0,
	highlightthickness=0,
	command=get_file,
	relief="flat",
)
t_fileloc.place(
	x=416,
	y=26,
	width=350,
	height=24.0
)



canvas.create_text(
	241,
	300,
	anchor="nw",
	text="private",
	fill="#DADADA",
	font=("Inter", 32 * -1)
)

canvas.create_text(
	259,
	244,
	anchor="nw",
	text="type",
	fill="#DADADA",
	font=("Inter", 32 * -1)
)

canvas.create_text(
	228,
	188,
	anchor="nw",
	text="category",
	fill="#DADADA",
	font=("Inter", 32 * -1)
)

canvas.create_text(
	249,
	132,
	anchor="nw",
	text="about",
	fill="#DADADA",
	font=("Inter", 32 * -1)
)

canvas.create_text(
	224,
	76,
	anchor="nw",
	text="file name",
	fill="#DADADA",
	font=("Inter", 32 * -1)
)

canvas.create_text(
	208,
	20,
	anchor="nw",
	text="file location",
	fill="#DADADA",
	font=("Inter", 32 * -1)
)

def upfunc():
	global t_fileloc
	global t_filename
	global t_about
	global t_category
	global t_type
	global t_private
	global b_start
	global FILE
	global CMD
	t_fileloc.config(state="disabled")
	t_filename.config(state="disabled")
	t_about.config(state="disabled")
	t_category.config(state="disabled")
	t_type.config(state="disabled")
	t_private.config(state="disabled")
	b_start.config(state="disabled")
	args = fr'"{FILE}" "{t_filename.get()}" "{t_about.get()}" "{t_category.get()}" "{t_type.get()}" "{t_private.get()}"'
	proc = Popen(f"{CMD} {args}", stdout=PIPE, text=True, bufsize=1)
	while True:
		line = proc.stdout.readline()
		change_console(f"{datetime.now()}>> {line.strip()}\n\n")
		if not line:
			break
	change_console("you can close the window now.")

def start():
	t = Thread(target=upfunc, daemon=False)
	t.start()
	
b_start = Button(
	borderwidth=0,
	highlightthickness=0,
	command=start,
	relief="flat",
	text="start"
)
b_start.place(
	x=280,
	y=350,
	width=340,
	height=40
)

def change_console(txt):
	global t_console
	t_console.config(state="normal")
	# t_console.delete("1.0", "end")
	t_console.insert("end", txt)
	t_console.config(state="disabled")
	t_console.see("end")

t_console = Text(
	bd=0,
	bg="#D9D9D9",
	fg="#000000",
	highlightthickness=0,
	state="disabled"
)
t_console.place(
	x=10,
	y=410,
	width=880,
	height=300
)

window.resizable(False, False)
window.mainloop()