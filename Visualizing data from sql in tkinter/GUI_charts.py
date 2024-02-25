import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import pandas as pd
import mysql.connector
from matplotlib.ticker import PercentFormatter
from PIL import Image, ImageTk

def fetch_av_tables():
    mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='produkcja',
    )
    mycursor = mydb.cursor()
    getRecords = 'show tables'
    mycursor.execute(getRecords)
    desRecords = mycursor.fetchall()
    mydb.close()
    records_tuple = tuple(row[0] for row in desRecords)
    records_tuple = tuple(name.upper() for name in records_tuple)
    return records_tuple

def fetch_data(obszar, zakres_od,zakres_do):
    mydb = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='produkcja',
    )
    mycursor = mydb.cursor()
    getRecords = 'Select * from '+ obszar +' where data between "'+zakres_od+'" and "'+zakres_do+'" and output > 0'
    mycursor.execute(getRecords)
    desRecords = mycursor.fetchall()
    mydb.close()
    Table = pd.DataFrame.from_records(desRecords)
    Table.rename(columns={0: "Dzien", 1: "Output", 2: "OEE"}, inplace=True)
    return Table

def update_chart(selected_item,zakres_var_od, zakres_var_do):
    ax.clear()
    ax2.clear()

    # Fetch data based on the selected item
    obszar = selected_item.lower()
    Table = fetch_data(obszar, zakres_var_od,zakres_var_do)

    # Output chart
    bar_width = 0.95
    bars = ax.bar(Table["Dzien"], Table["Output"], width=bar_width, color='royalblue', label='Output')
    ax.set_xticks(Table["Dzien"])
    ax.set_xticklabels(Table['Dzien'], rotation=90, ha='center')
    ax.set_xlabel('Dzien')
    ax.set_ylabel('Output')

    # OEE chart
    ax2.plot(Table["Dzien"], Table["OEE"], color='darkorange')
    ax2.yaxis.set_major_formatter(PercentFormatter(xmax=1, decimals=0))
    ax2.set_ylabel('OEE')
    ax2.yaxis.set_label_position('right')
    ax2.set_ylim(bottom=0, top=1)
    ax2.annotate('Annotation Text', xy=(2, 0.5), xytext=(3, 0.8), arrowprops=dict(arrowstyle='->', connectionstyle="arc3,rad=0.3"), annotation_clip=False)
    ax2.yaxis.set_major_locator(plt.MultipleLocator(0.1))

    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, yval, round(yval, 2), ha='center', va='bottom')

    # Refresh the canvas
    canvas.draw()

def on_window_resize(event):
    # Update the plot when the window is resized
    canvas.draw()

def update_db():
    mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='produkcja',
    )
    obszary = fetch_av_tables()
    for x in obszary: 
        # Importing data to MySQL
        excelFilePath = 'danezLaga.xlsx'
        readFile = pd.read_excel (excelFilePath,sheet_name=x)
        convToTuples = [(row[1], row[2], row[0].strftime("%Y-%m-%d")) for row in readFile.values]
        mycursor = mydb.cursor()
        updRecord = 'Update '+x+' set Output = %s, OEE=%s where Data = %s'
        mycursor.executemany(updRecord, convToTuples)
        mydb.commit()
        print("Dane "+x+" zaktualizowane.")
    mydb.close()
    show_label_temporarily(root, "Dane ze wszystkich tabel zostały zaktualizowane...",duration_ms=5000,color="yellow")
    update_chart(dropdown_var.get(),zakres_var_od.get(),zakres_var_do.get())

def show_label_temporarily(root, text, duration_ms=2000, color = "red"):
    label = ttk.Label(root, text=text,foreground=color,background="cadetblue4",font=("Verdena",12))
    label.place(x=10,y=window_height-30)
    root.update()
    root.after(duration_ms, label.destroy)

root = tk.Tk()

# Set window config
window_width = 1200
window_height = 800
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_coordinate = (screen_width - window_width) // 2
y_coordinate = (screen_height - window_height) // 2
root.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")
root.title("Dzienne zejścia & OEE")
root.config(bg="cadetblue4")
root.resizable(False, False)

# Create a StringVar to store the selected item
dropdown_var = tk.StringVar(root)
zakres_var_od = tk.StringVar(root)
zakres_var_do = tk.StringVar(root)

# Create a Label fo dropdown list
label = tk.Label(root, text="Wybierz obszar:",background="cadetblue4",font=("Verdana",12))
label.grid(row=0, column=0,padx=(10,0),pady=20,sticky='e')

# Create a dropdown list
options = fetch_av_tables()
dropdown = ttk.Combobox(root, textvariable=dropdown_var, values=options,width=6,font=("Verdana",12))
dropdown.grid(row=0, column=1,padx=1,sticky="w")
dropdown.set(options[0])

# Create a Label for Zakres
label2 = tk.Label(root, text="Wpisz zakres (YYYY-MM-DD) ->",background="cadetblue4",font=("Verdana",12))
label2.grid(row=0, column=2,padx=(10,0),sticky='w')

# Create a Label for Od
label2 = tk.Label(root, text="Od:",background="cadetblue4",font=("Verdana",12))
label2.grid(row=0, column=3,padx=(0,1),sticky='e')

# Create a dynamic Entry for Zakres od
zakres_entry = tk.Entry(root,textvariable=zakres_var_od,width=12,font=("Verdana",12))
zakres_entry.grid(row=0, column=4,padx=(0,2),sticky="w")
zakres_var_od.set("2024-01-01")

# Create a Label for Do
label2 = tk.Label(root, text="Do:",background="cadetblue4",font=("Verdana",12))
label2.grid(row=0, column=5,padx=(0,1),sticky='e')

# Create a dynamic Entry for Zakres do
zakres_entry_do = tk.Entry(root,textvariable=zakres_var_do,width=12,font=("Verdana",12))
zakres_entry_do.grid(row=0, column=6,padx=0,sticky="w")
zakres_var_do.set("2024-01-31")

Aktualizuj = tk.Button(root, text="Aktualizuj dane", command=update_db,font=("Verdena",12))
Aktualizuj.grid(row=0, column=7,padx=30)

# Create a Matplotlib Figure and Axes
fig = Figure(figsize=(12, 7), dpi=100,frameon=1)
ax = fig.add_subplot(111)
ax2 = ax.twinx()
fig.subplots_adjust(bottom=0.18, top=0.98)

# Create a Matplotlib canvas to embed in the Tkinter window
canvas = FigureCanvasTkAgg(fig, master=root)
canvas_widget = canvas.get_tk_widget()
canvas_widget.config(bg='lightgrey')
canvas_widget.place(x=0,y=60)

# Create a image logo
logo = Image.open("white-brand.png")
logo = logo.resize((150,40),Image.ADAPTIVE)
ikona = ImageTk.PhotoImage(logo)
tk.Label(root,image=ikona).place(x=window_width-160,y=10)

# Bind the dropdown to a function that will be called when the selection changes
dropdown.bind("<<ComboboxSelected>>", lambda event: update_chart(dropdown_var.get(),zakres_var_od.get(),zakres_var_do.get()))
root.bind("<Return>", lambda event: update_chart(dropdown_var.get(),zakres_var_od.get(),zakres_var_do.get()))

# Bind window resize event
root.bind("<Configure>", on_window_resize)

# Initial chart (you can customize this based on your needs)
update_chart(options[0],zakres_var_od.get(),zakres_var_do.get())

# Run the Tkinter event loop
root.mainloop()

#TO DO
#JPG and CTRL + S