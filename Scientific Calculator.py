from tkinter import *
import math

# =========================
# Global Variables
# =========================
expression = ""
is_degree = True
memory = 0
last_answer = ""
history = []

# =========================
# Colors / Theme
# =========================
BG_COLOR = "#121212"
DISPLAY_BG = "#1e1e1e"
DISPLAY_FG = "white"
OUTPUT_COLOR = "#7CFC00"   # light green
ERROR_COLOR = "#ff4d4d"

NUMBER_BG = "#2d2d2d"
NUMBER_HOVER = "#3a3a3a"

OPERATOR_BG = "#ff9500"
OPERATOR_HOVER = "#e68a00"

FUNC_BG = "#2d89ef"
FUNC_HOVER = "#1b6fc2"

MEMORY_BG = "#7d5fff"
MEMORY_HOVER = "#6c4fe0"

CLEAR_BG = "#d9534f"
CLEAR_HOVER = "#c9302c"

TEXT_COLOR = "white"

# =========================
# Main Window
# =========================
root = Tk()
root.title("Professional Scientific Calculator")
root.geometry("760x620")
root.configure(bg=BG_COLOR)
root.resizable(False, False)

equation = StringVar()

for i in range(7):
    root.columnconfigure(i, weight=1)
for i in range(8):
    root.rowconfigure(i, weight=1)

# =========================
# Helper functions for colors
# =========================
def set_input_color():
    entry.config(fg=DISPLAY_FG)

def set_output_color():
    entry.config(fg=OUTPUT_COLOR)

def set_error_color():
    entry.config(fg=ERROR_COLOR)

# =========================
# Calculator Functions
# =========================
def press(key):
    global expression
    expression += str(key)
    equation.set(expression)
    set_input_color()

    if str(key) == str(math.pi):
        history.append("π inserted")
    elif str(key) == str(math.e):
        history.append("e inserted")
    elif str(key) == str(2 * math.pi):
        history.append("τ inserted")

    entry.icursor(END)

def clear():
    global expression
    expression = ""
    equation.set(expression)
    set_input_color()

def backspace():
    global expression
    expression = expression[:-1]
    equation.set(expression)
    set_input_color()

def evaluate():
    global expression, last_answer
    try:
        result = str(eval(expression))
        last_answer = result
        history.append(f"{expression} = {result}")
        equation.set(result)
        expression = result
        set_output_color()
    except:
        equation.set("ERROR")
        expression = ""
        set_error_color()

def squareRoot():
    global expression
    try:
        original = expression
        result = str(math.sqrt(float(expression)))
        history.append(f"sqrt({original}) = {result}")
        equation.set(result)
        expression = result
        set_output_color()
        entry.icursor(END)
    except:
        equation.set("ERROR")
        expression = ""
        set_error_color()

def square():
    global expression
    try:
        original = expression
        result = str(float(expression) ** 2)
        history.append(f"({original})² = {result}")
        equation.set(result)
        expression = result
        set_output_color()
        entry.icursor(END)
    except:
        equation.set("ERROR")
        expression = ""
        set_error_color()

def cubeRoot():
    global expression
    try:
        original = expression
        result = str(float(expression) ** (1/3))
        history.append(f"∛({original}) = {result}")
        equation.set(result)
        expression = result
        set_output_color()
        entry.icursor(END)
    except:
        equation.set("ERROR")
        expression = ""
        set_error_color()

def factorial():
    global expression
    try:
        original = expression
        result = str(math.factorial(int(float(expression))))
        history.append(f"{original}! = {result}")
        equation.set(result)
        expression = result
        set_output_color()
        entry.icursor(END)
    except:
        equation.set("ERROR")
        expression = ""
        set_error_color()

def absolute():
    global expression
    try:
        original = expression
        result = str(abs(float(expression)))
        history.append(f"|{original}| = {result}")
        equation.set(result)
        expression = result
        set_output_color()
        entry.icursor(END)
    except:
        equation.set("ERROR")
        expression = ""
        set_error_color()

def scientificFunction(func):
    global expression
    try:
        original = expression
        value = float(expression)

        if func in ['sin', 'cos', 'tan'] and is_degree:
            value = math.radians(value)

        result = str(getattr(math, func)(value))
        history.append(f"{func}({original}) = {result}")
        equation.set(result)
        expression = result
        set_output_color()
        entry.icursor(END)
    except:
        equation.set("ERROR")
        expression = ""
        set_error_color()

def toggleDegreeMode():
    global is_degree
    is_degree = not is_degree
    mode_button.config(text="DEG" if is_degree else "RAD")

def memoryStore():
    global memory
    try:
        memory = float(equation.get())
        history.append(f"M+ : Stored {memory}")
        entry.icursor(END)
    except:
        memory = 0

def memoryRecall():
    global expression
    expression += str(memory)
    equation.set(expression)
    history.append(f"MR : Recalled {memory}")
    set_input_color()
    entry.icursor(END)

def memoryClear():
    global memory
    memory = 0
    history.append("MC : Memory Cleared")

def memorySubtract():
    global memory
    try:
        value = float(equation.get())
        memory -= value
        history.append(f"M- : New Memory = {memory}")
        entry.icursor(END)
    except:
        pass

def showHistory():
    top = Toplevel(root)
    top.title("Calculation History")
    top.geometry("360x420")
    top.configure(bg="#1c1c1c")

    title = Label(top, text="History", font=("Arial", 16, "bold"),
                  bg="#1c1c1c", fg="white")
    title.pack(pady=10)

    lb = Listbox(top, font=('Consolas', 13), bg="#2b2b2b",
                 fg="white", selectbackground="#444", bd=0)
    lb.pack(expand=True, fill=BOTH, padx=10, pady=10)

    for item in history:
        lb.insert(END, item)

# =========================
# Tooltip Function
# =========================
def createToolTip(widget, text):
    tooltip = Toplevel(widget)
    tooltip.wm_overrideredirect(True)
    tooltip.withdraw()
    tooltip.configure(bg="#333333")

    label = Label(
        tooltip,
        text=text,
        bg="#333333",
        fg="white",
        padx=6,
        pady=3,
        font=('Arial', 9)
    )
    label.pack()

    def enter(event):
        tooltip.deiconify()

    def move(event):
        tooltip.geometry(f"+{event.x_root+20}+{event.y_root+20}")

    def leave(event):
        tooltip.withdraw()

    widget.bind("<Enter>", enter)
    widget.bind("<Leave>", leave)
    widget.bind("<Motion>", move)

# =========================
# Hover Effect
# =========================
def on_enter(e, btn, hover_color):
    btn['bg'] = hover_color

def on_leave(e, btn, normal_color):
    btn['bg'] = normal_color

# =========================
# Display Entry
# =========================
entry = Entry(
    root,
    textvariable=equation,
    font=('Consolas', 28, 'bold'),
    bg=DISPLAY_BG,
    fg=DISPLAY_FG,
    insertbackground="white",
    relief="flat",
    bd=10,
    justify="right"
)
entry.grid(row=0, column=0, columnspan=7, padx=10, pady=12, sticky="nsew", ipady=18)
entry.focus_set()

# =========================
# Button Configurations
# =========================
buttons = [
    ('Clear', 1, 0, clear, 'Clear all', CLEAR_BG, CLEAR_HOVER),
    ('⌫', 1, 1, backspace, 'Backspace', CLEAR_BG, CLEAR_HOVER),
    ('%', 1, 2, lambda: press("%"), 'Modulus', OPERATOR_BG, OPERATOR_HOVER),
    ('/', 1, 3, lambda: press("/"), 'Divide', OPERATOR_BG, OPERATOR_HOVER),
    ('sqrt', 1, 4, squareRoot, 'Square root', FUNC_BG, FUNC_HOVER),
    ('x²', 1, 5, square, 'Square', FUNC_BG, FUNC_HOVER),
    ('∛x', 1, 6, cubeRoot, 'Cube root', FUNC_BG, FUNC_HOVER),

    ('7', 2, 0, lambda: press("7"), 'Number 7', NUMBER_BG, NUMBER_HOVER),
    ('8', 2, 1, lambda: press("8"), 'Number 8', NUMBER_BG, NUMBER_HOVER),
    ('9', 2, 2, lambda: press("9"), 'Number 9', NUMBER_BG, NUMBER_HOVER),
    ('*', 2, 3, lambda: press("*"), 'Multiply', OPERATOR_BG, OPERATOR_HOVER),
    ('(', 2, 4, lambda: press("("), 'Open bracket', FUNC_BG, FUNC_HOVER),
    (')', 2, 5, lambda: press(")"), 'Close bracket', FUNC_BG, FUNC_HOVER),
    ('π', 2, 6, lambda: press(str(math.pi)), 'Pi', FUNC_BG, FUNC_HOVER),

    ('4', 3, 0, lambda: press("4"), 'Number 4', NUMBER_BG, NUMBER_HOVER),
    ('5', 3, 1, lambda: press("5"), 'Number 5', NUMBER_BG, NUMBER_HOVER),
    ('6', 3, 2, lambda: press("6"), 'Number 6', NUMBER_BG, NUMBER_HOVER),
    ('-', 3, 3, lambda: press("-"), 'Subtract', OPERATOR_BG, OPERATOR_HOVER),
    ('sin', 3, 4, lambda: scientificFunction('sin'), 'Sine', FUNC_BG, FUNC_HOVER),
    ('cos', 3, 5, lambda: scientificFunction('cos'), 'Cosine', FUNC_BG, FUNC_HOVER),
    ('e', 3, 6, lambda: press(str(math.e)), 'Euler number', FUNC_BG, FUNC_HOVER),

    ('1', 4, 0, lambda: press("1"), 'Number 1', NUMBER_BG, NUMBER_HOVER),
    ('2', 4, 1, lambda: press("2"), 'Number 2', NUMBER_BG, NUMBER_HOVER),
    ('3', 4, 2, lambda: press("3"), 'Number 3', NUMBER_BG, NUMBER_HOVER),
    ('+', 4, 3, lambda: press("+"), 'Add', OPERATOR_BG, OPERATOR_HOVER),
    ('tan', 4, 4, lambda: scientificFunction('tan'), 'Tangent', FUNC_BG, FUNC_HOVER),
    ('log', 4, 5, lambda: scientificFunction('log10'), 'Log base 10', FUNC_BG, FUNC_HOVER),
    ('τ', 4, 6, lambda: press(str(2 * math.pi)), 'Tau', FUNC_BG, FUNC_HOVER),

    ('0', 5, 0, lambda: press("0"), 'Number 0', NUMBER_BG, NUMBER_HOVER),
    ('.', 5, 1, lambda: press("."), 'Decimal', NUMBER_BG, NUMBER_HOVER),
    ('=', 5, 2, evaluate, 'Evaluate', OPERATOR_BG, OPERATOR_HOVER),
    ('exp', 5, 3, lambda: scientificFunction('exp'), 'Exponential', FUNC_BG, FUNC_HOVER),
    ('ln', 5, 4, lambda: scientificFunction('log'), 'Natural log', FUNC_BG, FUNC_HOVER),
    ('!', 5, 5, factorial, 'Factorial', FUNC_BG, FUNC_HOVER),
    ('Ans', 5, 6, lambda: press(last_answer), 'Last answer', MEMORY_BG, MEMORY_HOVER),

    ('|x|', 6, 0, absolute, 'Absolute value', FUNC_BG, FUNC_HOVER),
    ('x^y', 6, 1, lambda: press("**"), 'Power', FUNC_BG, FUNC_HOVER),
    ('M+', 6, 2, memoryStore, 'Memory store', MEMORY_BG, MEMORY_HOVER),
    ('M-', 6, 3, memorySubtract, 'Memory subtract', MEMORY_BG, MEMORY_HOVER),
    ('MC', 6, 4, memoryClear, 'Memory clear', MEMORY_BG, MEMORY_HOVER),
    ('MR', 6, 5, memoryRecall, 'Memory recall', MEMORY_BG, MEMORY_HOVER),
    ('Hist', 6, 6, showHistory, 'Show history', MEMORY_BG, MEMORY_HOVER),
]

for (textName, rowNumber, columnNumber, fun, tooltip, bg_color, hover_color) in buttons:
    btn = Button(
        root,
        text=textName,
        command=fun,
        font=('Arial', 15, 'bold'),
        bg=bg_color,
        fg=TEXT_COLOR,
        activeforeground="white",
        relief="flat",
        bd=0,
        cursor="hand2"
    )
    btn.grid(row=rowNumber, column=columnNumber, padx=4, pady=4, sticky="nsew", ipady=12)

    btn.bind("<Enter>", lambda e, b=btn, hc=hover_color: on_enter(e, b, hc))
    btn.bind("<Leave>", lambda e, b=btn, nc=bg_color: on_leave(e, b, nc))

    createToolTip(btn, tooltip)

# =========================
# Degree / Radian Toggle Button
# =========================
mode_button = Button(
    root,
    text="DEG",
    command=toggleDegreeMode,
    font=('Arial', 15, 'bold'),
    bg="#444444",
    fg="white",
    relief="flat",
    bd=0,
    cursor="hand2"
)
mode_button.grid(row=7, column=0, columnspan=7, sticky="nsew", padx=6, pady=8, ipady=10)
createToolTip(mode_button, "Degree / Radian Mode")

# =========================
# Key Bindings
# =========================
def keyInput(event):
    if event.char in "0123456789+-/%*.()":
        press(event.char)
    elif event.keysym == 'Return':
        evaluate()
    elif event.keysym == 'BackSpace':
        backspace()
    elif event.char in 'cC':
        clear()

root.bind("<Key>", keyInput)

root.mainloop()

