
import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedStyle
import ripe  # Din ripe.py-fil


# --- FUNKTION FÖR RIPE-VYN ---
def create_ripe_view(parent, logo_image):
    frame = ttk.Frame(parent)
    frame.grid(row=0, column=0, sticky="nsew")
    frame.grid_columnconfigure(1, weight=1)
    frame.grid_rowconfigure(
        5, weight=1
    )  # Öka radindex eftersom vi lagt till en bild på rad 0

    # Lägg till bilden överst
    lbl_logo = ttk.Label(frame, image=logo_image)
    lbl_logo.image = (
        logo_image  # VIKTIGT: Spara referens så bilden inte försvinner
    )
    lbl_logo.grid(row=0, column=0, columnspan=2, pady=10)

    lbl_title = ttk.Label(frame, text="RIPE Search Tool", font=("Arial", 16))
    lbl_title.grid(row=1, column=0, columnspan=2, pady=10)

    lbl_ip = ttk.Label(frame, text="Enter IP-address:")
    lbl_ip.grid(row=2, column=0, padx=20, pady=10, sticky="e")

    ent_name = ttk.Entry(frame)
    ent_name.grid(row=2, column=1, padx=20, pady=10, sticky="ew")

    result_label = ttk.Label(
        frame, text="", justify="left", relief="solid", padding=10
    )
    result_label.grid(row=5, column=0, columnspan=2, padx=20, pady=10, sticky="nsew")

    btn_submit = ttk.Button(
        frame,
        text="SEARCH",
        command=lambda: ripe.query_ripe(ent_name.get(), result_label),
    )
    btn_submit.grid(row=4, column=0, columnspan=2, pady=20)

    return frame


# --- FUNKTION FÖR IMEI-VYN ---
def create_imei_view(parent, logo_image):
    frame = ttk.Frame(parent)
    frame.grid(row=0, column=0, sticky="nsew")
    frame.grid_columnconfigure(1, weight=1)

    # Lägg till bilden överst även här
    lbl_logo = ttk.Label(frame, image=logo_image)
    lbl_logo.image = logo_image  # Spara referens
    lbl_logo.grid(row=0, column=0, columnspan=2, pady=10)

    lbl_imei_title = ttk.Label(
        frame, text="IMEI Checker Tool", font=("Arial", 16)
    )
    lbl_imei_title.grid(row=1, column=0, columnspan=2, pady=10)

    lbl_imei = ttk.Label(frame, text="Enter IMEI:")
    lbl_imei.grid(row=2, column=0, padx=20, pady=10, sticky="e")

    ent_imei = ttk.Entry(frame)
    ent_imei.grid(row=2, column=1, padx=20, pady=10, sticky="ew")

    btn_imei_submit = ttk.Button(
        frame, text="CHECK IMEI", command=lambda: print("Kollar IMEI...")
    )
    btn_imei_submit.grid(row=3, column=0, columnspan=2, pady=20)

    return frame


# --- HUVUDPROGRAM ---
root = tk.Tk()
root.title("P-Tools")
root.geometry("800x800")

# Se till att filnamnet matchar det som ligger i din mapp (t.ex. icon.PNG eller inon.PNG)
icon_image = tk.PhotoImage(file="icons/icon.PNG")
root.iconphoto(True, icon_image)

# Uppdaterad sökväg till din logo baserat på din beskrivning
#top_image = tk.PhotoImage(file="icons/logo_image.PNG")
# Ändra till detta för att halvera storleken:
top_image = tk.PhotoImage(file="icons/logo_image.PNG").subsample(2, 2)

# Applicera tema
style = ThemedStyle(root)
style.set_theme("equilux")

# 1. Skapa sidofältet (Sidebar)
sidebar = ttk.Frame(root, width=150)
sidebar.grid(row=0, column=0, sticky="ns")

# 2. Skapa huvudinnehållsframen (Container för alla vyer)
main_frame = ttk.Frame(root)
main_frame.grid(row=0, column=1, sticky="nsew")

# Konfigurera grid-vikter
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(0, weight=1)

main_frame.grid_columnconfigure(0, weight=1)
main_frame.grid_rowconfigure(0, weight=1)

# Skapa vyerna och skicka med bilden som argument
ripe_frame = create_ripe_view(main_frame, top_image)
imei_frame = create_imei_view(main_frame, top_image)


# --- FUNKTION FÖR ATT BYTA FRAME ---
def show_frame(frame):
    frame.tkraise()


# --- SIDOFÄLTETS KNAPPAR ---
lbl_menu = ttk.Label(sidebar, text="Menu", font=("Arial", 12, "bold"))
lbl_menu.grid(row=0, column=0, padx=10, pady=20)

btn_ripe = ttk.Button(
    sidebar, text="RIPE", width=15, command=lambda: show_frame(ripe_frame)
)
btn_ripe.grid(row=1, column=0, padx=10, pady=5)

btn_IMEI_Checker = ttk.Button(
    sidebar, text="IMEI-Checker", width=15, command=lambda: show_frame(imei_frame)
)
btn_IMEI_Checker.grid(row=2, column=0, padx=10, pady=5)

# Starta på RIPE-vyn som standard
show_frame(ripe_frame)

root.mainloop()
