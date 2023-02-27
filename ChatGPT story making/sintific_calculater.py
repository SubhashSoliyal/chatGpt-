import tkinter as tk
import math

# Define the calculator functions

def add(*args):
    result = sum(args)
    output.config(text="Result: " + str(result))

def subtract(*args):
    result = args[0] - sum(args[1:])
    output.config(text="Result: " + str(result))

def multiply(*args):
    result = 1
    for arg in args:
        result *= arg
    output.config(text="Result: " + str(result))

def divide(*args):
    result = args[0]
    for arg in args[1:]:
        result /= arg
    output.config(text="Result: " + str(result))

def power(base, exponent=2):
    result = base ** exponent
    output.config(text="Result: " + str(result))

def sqrt(num):
    try:
        result = math.sqrt(num)
        output.config(text="Result: " + str(result))
    except ValueError:
        output.config(text="Please enter a valid number")
    except Exception:
        output.config(text="An error occurred")

def arcsin(num):
    try:
        result = math.asin(num)
        output.config(text="Result: " + str(result))
    except ValueError:
        output.config(text="Please enter a valid number between -1 and 1")
    except Exception:
        output.config(text="An error occurred")

def arccos(num):
    try:
        result = math.acos(num)
        output.config(text="Result: " + str(result))
    except ValueError:
        output.config(text="Please enter a valid number between -1 and 1")
    except Exception:
        output.config(text="An error occurred")

def arctan(num):
    try:
        result = math.atan(num)
        output.config(text="Result: " + str(result))
    except Exception:
        output.config(text="An error occurred")

def logarithm(num, base=10):
    try:
        result = math.log(num, base)
        output.config(text="Result: " + str(result))
    except ValueError:
        output.config(text="Please enter a valid number and base")
    except Exception:
        output.config(text="An error occurred")

def natural_logarithm(num):
    try:
        result = math.log(num)
        output.config(text="Result: " + str(result))
    except ValueError:
        output.config(text="Please enter a valid number")
    except Exception:
        output.config(text="An error occurred")

def factorial(num, mod=None):
    try:
        if mod is None:
            result = math.factorial(num)
        else:
            result = 1
            for i in range(1, num + 1):
                result = (result * i) % mod
        output.config(text="Result: " + str(result))
    except ValueError:
        output.config(text="Please enter a valid number")
    except Exception:
        output.config(text="An error occurred")

# Define the GUI function
def create_gui():
    # Create the main window
    window = tk.Tk()
    window.title("Scientific Calculator")

    # Create the input field
    input_field = tk.Entry(window)
    input_field.pack()

    # Create the output label
    global output
    output = tk.Label(window, text="Enter an equation and press Enter")
    output.pack()

    # Create
    # Create the calculator buttons
    button_frame = tk.Frame(window)
    button_frame.pack()

    tk.Button(button_frame, text="+", command=lambda: on_button_click(add, *parse_input())).grid(row=0, column=0)
    tk.Button(button_frame, text="-", command=lambda: on_button_click(subtract, *parse_input())).grid(row=0, column=1)
    tk.Button(button_frame, text="*", command=lambda: on_button_click(multiply, *parse_input())).grid(row=0, column=2)
    tk.Button(button_frame, text="/", command=lambda: on_button_click(divide, *parse_input())).grid(row=0, column=3)
    tk.Button(button_frame, text="^", command=lambda: on_button_click(power, *parse_input())).grid(row=1, column=0)
    tk.Button(button_frame, text="sqrt", command=lambda: on_button_click(sqrt, *parse_input())).grid(row=1, column=1)
    tk.Button(button_frame, text="arcsin", command=lambda: on_button_click(arcsin, *parse_input())).grid(row=1, column=2)
    tk.Button(button_frame, text="arccos", command=lambda: on_button_click(arccos, *parse_input())).grid(row=1, column=3)
    tk.Button(button_frame, text="arctan", command=lambda: on_button_click(arctan, *parse_input())).grid(row=2, column=0)
    tk.Button(button_frame, text="log", command=lambda: on_button_click(logarithm, *parse_input())).grid(row=2, column=1)
    tk.Button(button_frame, text="ln", command=lambda: on_button_click(natural_logarithm, *parse_input())).grid(row=2, column=2)
    tk.Button(button_frame, text="!", command=lambda: on_button_click(factorial, *parse_input())).grid(row=2, column=3)

    # Start the main event loop
    window.mainloop()

    # Define a function to parse the user input and convert it to arguments for the calculator functions
    def parse_input():
        try:
            input_str = input_field.get()
            args = []
            for item in input_str.split():
                try:
                    args.append(float(item))
                except ValueError:
                    args.append(item)
            return args
        except Exception:
            output.config(text="An error occurred")

    # Define the function that handles button clicks
    def on_button_click(func, *args, **kwargs):
        try:
            func(*args, **kwargs)
        except TypeError:
            output.config(text="Invalid input")

# Create the GUI
create_gui()