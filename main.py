import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk

from interpreter.environment.environment import Environment
from interpreter.environment.syntax_tree import SyntaxTree
from interpreter.parser import Interpreter


def new_file():
    code_editor.delete('1.0', tk.END)  # Se borra el contenido del editor de texto.


def open_file():
    file_path = filedialog.askopenfilename(initialdir="data", filetypes=[("OLCScript", "*.olc")])

    if file_path:
        try:
            with open(file_path) as file:
                code_editor.delete('1.0', tk.END)  # Se borra el contenido del editor de texto.

                code_editor.insert('1.0', file.read())  # Se inserta el contenido del archivo en el editor de texto.
        except Exception as exception:
            messagebox.showerror("Abrir archivo", f"Error al abrir el archivo: {exception}")


def save_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".olc")

    if file_path:
        try:
            with open(file_path, 'w') as file:
                file.write(code_editor.get('1.0', tk.END))
        except Exception as exception:
            messagebox.showerror("Guardar archivo", f"Error al guardar el archivo: {exception}")


def execute_code():
    input_code = code_editor.get("1.0", tk.END)  # Se obtiene el código del editor de texto.

    environment = Environment(None, "Global")  # Se crea un entorno global.
    interpreter = Interpreter()
    syntax_tree = SyntaxTree()

    instructions = interpreter.interpret(input_code)  # Se interpreta el código y se obtienen las instrucciones.

    for instruction in instructions:  # Se ejecuta cada instrucción individualmente.
        instruction.execute(syntax_tree, environment)

    console_tab.config(state="normal")  # Se habilita la pestaña de consola.
    console_tab.delete("1.0", tk.END)  # Se borra el contenido de la pestaña de consola.
    console_tab.insert("1.0", str(syntax_tree.get_console()))  # Se inserta el contenido de la consola.
    console_tab.config(state="disabled")  # Se deshabilita la pestaña de consola.


def show_reports():
    messagebox.showinfo("Reportes", "Funcionalidad de informes no implementada.")


root = tk.Tk()  # Se crea la ventana principal.
root.title("OLCScript IDE")
root.resizable(False, False)

buttons_frame = tk.Frame(root)  # Se crea un marco para los botones.
buttons_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=5)  # Se coloca el marco en la ventana principal.
buttons_frame.grid_columnconfigure(0, weight=1)  # Se crean espaciadores para centrar los botones.
buttons_frame.grid_columnconfigure(4, weight=1)

new_button = tk.Button(buttons_frame, text="Nuevo", command=new_file, width=10)
new_button.grid(row=0, column=1, padx=2)
open_button = tk.Button(buttons_frame, text="Abrir", command=open_file, width=10)
open_button.grid(row=0, column=2, padx=2)
save_button = tk.Button(buttons_frame, text="Guardar", command=save_file, width=10)
save_button.grid(row=0, column=3, padx=2)

info_label_frame = tk.Frame(root)  # Se crea un marco para la etiqueta de información.
info_label_frame.grid(row=0, column=1, sticky="ew", padx=10, pady=5)  # Se coloca el marco en la ventana principal.
info_label_frame.grid_columnconfigure(0, weight=1)  # Se crean espaciadores para centrar la etiqueta.

info_label = tk.Label(info_label_frame, text="Información de Salida", font=("Arial", 14))
info_label.grid(row=0, column=0, sticky="ew")

code_editor = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=20)  # Se crea un editor de texto.
code_editor.grid(row=1, column=0, padx=10, pady=0, sticky="nsew")  # Se coloca el editor en la ventana principal.

execute_button = tk.Button(root, text="Ejecutar", command=execute_code)  # Se crea un botón para ejecutar.
execute_button.grid(row=2, column=0, padx=10, pady=10, sticky="ew")
report_button = tk.Button(root, text="Mostar Reportes", command=show_reports)  # Se crea un botón para reportes.
report_button.grid(row=3, column=0, padx=10, pady=10, sticky="ew")

tab_control = ttk.Notebook(root)  # Se crea un control de pestañas.

console_tab = scrolledtext.ScrolledText(tab_control, wrap=tk.WORD)  # Se crea una pestaña para la consola.
console_tab.config(state="disabled")
symbol_tab = tk.Text(tab_control)  # Se crea una pestaña para la tabla de símbolos.
symbol_tab.config(state="disabled")
errors_tab = tk.Text(tab_control)  # Se crea una pestaña para los errores.
errors_tab.config(state="disabled")

tab_control.add(console_tab, text='Consola')
tab_control.add(symbol_tab, text='Tabla de Símbolos')
tab_control.add(errors_tab, text='Errores')
tab_control.grid(row=1, column=1, rowspan=3, padx=10, pady=0, sticky="nsew")

root.mainloop()  # Se inicia el bucle principal de la ventana.
