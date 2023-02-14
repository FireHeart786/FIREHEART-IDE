from tkinter import *
from colorama import init, Fore, Back, Style
from tkinter import simpledialog
from tkinter.filedialog import asksaveasfilename, askopenfilename
import subprocess
init()

compiler = Tk()
compiler.title(Fore.GREEN + 'FIRE_HEART IDE' + Style.RESET_ALL)
file_path = ''


def set_file_path(path):
    global file_path
    file_path = path


def open_file():
    path = askopenfilename(filetypes=[('Python Files', '*.py')])
    with open(path, 'r') as file:
        code = file.read()
        editor.delete('1.0', END)
        editor.insert('1.0', code)
        set_file_path(path)


def save_as():
    if file_path == '':
        path = asksaveasfilename(filetypes=[('Python Files', '*.py')])
    else:
        path = file_path
    with open(path, 'w') as file:
        code = editor.get('1.0', END)
        file.write(code)
        set_file_path(path)


def run():
    if file_path == '':
        save_prompt = Toplevel()
        text = Label(save_prompt, text='Please save your code')
        text.pack()
        return
    command = f'python {file_path}'
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    code_output.insert('1.0', output)
    code_output.insert('1.0', error, 'error')
    code_output.tag_config('error', foreground='red')



def find():
    search_term = simpledialog.askstring("Find", "Enter search term:")
    if search_term:
        start = editor.search(search_term, '1.0', stopindex=END)
        if start:
            end = f"{start}+{len(search_term)}c"
            editor.tag_remove(SEL, '1.0', END)
            editor.tag_add(SEL, start, end)
            editor.mark_set(INSERT, end)
            editor.see(INSERT)
        else:
            messagebox.showinfo("Find", f"'{search_term}' not found.")


menu_bar = Menu(compiler)

file_menu = Menu(menu_bar, tearoff=0)
file_menu.add_command(label='Open', command=open_file)
file_menu.add_command(label='Save', command=save_as)
file_menu.add_command(label='Save As', command=save_as)
file_menu.add_command(label='Exit', command=exit)
menu_bar.add_cascade(label='File', menu=file_menu)

save_bar = Menu(menu_bar, tearoff=0)
save_bar.add_command(label='Save', command=save_as)
menu_bar.add_cascade(label='Save', menu=save_bar)

find_bar = Menu(menu_bar, tearoff=0)
find_bar.add_command(label='Find', command=find)
menu_bar.add_cascade(label='Find', menu=find_bar)

run_bar = Menu(menu_bar, tearoff=0)
run_bar.add_command(label='Run', command=run)
menu_bar.add_cascade(label='Run', menu=run_bar)

compiler.config(menu=menu_bar)

editor = Text(bg='black', fg='white', insertbackground='white')
editor.pack()

code_output = Text(height=10, bg='black', fg='white', insertbackground='white') 
code_output.pack()

compiler.mainloop()
