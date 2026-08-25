import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path
from queue import Empty, Queue
from threading import Event, Thread
from ttkthemes import ThemedStyle
import converter
import ripe
import phone

PROJECT_VERSION = "0.0.1"


# --- FUNKTION FÖR RIPE-VYN ---
def create_ripe_view(parent, logo_image):
    frame = ttk.Frame(parent)
    frame.grid(row=0, column=0, sticky="nsew")
    frame.grid_columnconfigure(1, weight=1)
    frame.grid_rowconfigure(5, weight=1)

    lbl_logo = ttk.Label(frame, image=logo_image)
    lbl_logo.image = logo_image
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

def create_phone_numbers_view(parent, logo_image):
    frame = ttk.Frame(parent)
    frame.grid(row=0, column=0, sticky="nsew")
    frame.grid_columnconfigure(1, weight=1)
    frame.grid_rowconfigure(5, weight=1)  # Viktigt för att textfältet ska växa vertikalt

    lbl_logo = ttk.Label(frame, image=logo_image)
    lbl_logo.image = logo_image
    lbl_logo.grid(row=0, column=0, columnspan=2, pady=10)

    lbl_phone_title = ttk.Label(
        frame, text="Search Phone Number", font=("Arial", 16)
    )
    lbl_phone_title.grid(row=1, column=0, columnspan=2, pady=10)

    lbl_phone = ttk.Label(frame, text="Enter Phone Number with country code:")
    lbl_phone.grid(row=2, column=0, padx=20, pady=10, sticky="e")

    ent_phone = ttk.Entry(frame)
    ent_phone.grid(row=2, column=1, padx=20, pady=10, sticky="ew")

    result_label = ttk.Label(
        frame, text="", justify="left", relief="solid", padding=10
    )
    result_label.grid(row=5, column=0, columnspan=2, padx=20, pady=10, sticky="nsew")

    btn_phone_submit = ttk.Button(
        frame,
        text="SEARCH",
        command=lambda: phone.search_number(ent_phone.get(), result_label),
    )
    btn_phone_submit.grid(row=4, column=0, columnspan=2, pady=20)

    return frame


def create_converter_view(parent, logo_image):
    frame = ttk.Frame(parent)
    frame.grid(row=0, column=0, sticky="nsew")
    frame.grid_columnconfigure(1, weight=1)
    frame.grid_rowconfigure(5, weight=1)

    lbl_logo = ttk.Label(frame, image=logo_image)
    lbl_logo.image = logo_image
    lbl_logo.grid(row=0, column=0, columnspan=2, pady=10)

    lbl_title = ttk.Label(frame, text="Media Converter", font=("Arial", 16))
    lbl_title.grid(row=1, column=0, columnspan=2, pady=10)

    input_path = tk.StringVar()
    lbl_file = ttk.Label(frame, text="Choose media file:")
    lbl_file.grid(row=2, column=0, padx=20, pady=10, sticky="e")

    file_entry = ttk.Entry(frame, textvariable=input_path)
    file_entry.grid(row=2, column=1, padx=(20, 5), pady=10, sticky="ew")

    def choose_file():
        selected_file = filedialog.askopenfilename(
            initialdir=str(Path.home()),
            title="Choose a media file",
            filetypes=(
                ("All files", "*"),
                (
                    "Media files",
                    "*.mp3 *.mp4 *.avi *.mkv *.wav *.mov *.flac *.ogg *.webm",
                ),
            ),
        )
        if selected_file:
            input_path.set(selected_file)

    browse_button = ttk.Button(frame, text="Browse", command=choose_file)
    browse_button.grid(row=2, column=2, padx=(0, 20), pady=10)

    lbl_format = ttk.Label(frame, text="Convert to format:")
    lbl_format.grid(row=3, column=0, padx=20, pady=10, sticky="e")

    output_format = tk.StringVar(value="mp4")
    format_box = ttk.Combobox(
        frame,
        textvariable=output_format,
        values=("mp4", "mp3", "avi", "mkv", "wav"),
        state="readonly",
    )
    format_box.grid(row=3, column=1, padx=20, pady=10, sticky="ew")

    result_label = ttk.Label(
        frame, text="", justify="left", relief="solid", padding=10
    )
    result_label.grid(row=5, column=0, columnspan=3, padx=20, pady=10, sticky="nsew")

    progress_bar = ttk.Progressbar(frame, mode="determinate", maximum=100)
    progress_bar.grid(row=6, column=0, columnspan=3, padx=20, pady=(0, 10), sticky="ew")

    status_queue = Queue()
    cancel_event = Event()
    conversion_thread = None

    def update_status():
        try:
            while True:
                status, value = status_queue.get_nowait()
                if status == "progress":
                    progress_bar["value"] = value * 100
                elif status == "done":
                    result_label.config(text=f"Converted file:\n{value}")
                    convert_button.config(state="normal")
                    cancel_button.config(state="disabled")
                elif status == "cancelled":
                    result_label.config(text="Conversion cancelled.")
                    convert_button.config(state="normal")
                    cancel_button.config(state="disabled")
                elif status == "error":
                    messagebox.showerror("Conversion failed", value)
                    convert_button.config(state="normal")
                    cancel_button.config(state="disabled")
        except Empty:
            pass
        frame.after(100, update_status)

    def convert_file():
        nonlocal conversion_thread
        if not input_path.get():
            messagebox.showwarning("Missing file", "Please choose a media file.")
            return

        cancel_event.clear()
        progress_bar["value"] = 0
        convert_button.config(state="disabled")
        cancel_button.config(state="normal")

        def run_conversion():
            try:
                output_path = converter.konvertera_mediafil(
                    input_path.get(),
                    output_format.get(),
                    progress_callback=lambda progress: status_queue.put(
                        ("progress", progress)
                    ),
                    cancel_event=cancel_event,
                )
                status_queue.put(("done", output_path))
            except converter.ConversionCancelled:
                status_queue.put(("cancelled", None))
            except Exception as error:
                status_queue.put(("error", str(error)))

        conversion_thread = Thread(target=run_conversion, daemon=True)
        conversion_thread.start()

    def cancel_conversion():
        cancel_event.set()
        cancel_button.config(state="disabled")
        result_label.config(text="Cancelling conversion...")

    convert_button = ttk.Button(frame, text="CONVERT", command=convert_file)
    convert_button.grid(row=4, column=0, columnspan=2, pady=20)

    cancel_button = ttk.Button(
        frame, text="CANCEL", command=cancel_conversion, state="disabled"
    )
    cancel_button.grid(row=4, column=2, padx=(0, 20), pady=20)

    frame.after(100, update_status)

    return frame



# --- FUNKTION FÖR IMEI-VYN ---
def create_imei_view(parent, logo_image):
    frame = ttk.Frame(parent)
    frame.grid(row=0, column=0, sticky="nsew")
    frame.grid_columnconfigure(1, weight=1)

    lbl_logo = ttk.Label(frame, image=logo_image)
    lbl_logo.image = logo_image
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



# --- FUNKTION FÖR ABOUT-VYN ---
def create_about_view(parent, logo_image):
    frame = ttk.Frame(parent)
    frame.grid(row=0, column=0, sticky="nsew")
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_rowconfigure(3, weight=1)  # Allows text area to expand vertically

    lbl_logo = ttk.Label(frame, image=logo_image)
    lbl_logo.image = logo_image
    lbl_logo.grid(row=0, column=0, columnspan=2, pady=10)

    lbl_about_title = ttk.Label(
        frame, text="P-Tools - ABOUT", font=("Arial", 16)
    )
    lbl_about_title.grid(row=1, column=0, columnspan=2, pady=10)

    lbl_version = ttk.Label(
        frame, text=f"Version: {PROJECT_VERSION}", font=("Arial", 12)
    )
    lbl_version.grid(row=2, column=0, columnspan=2, pady=10)

    license_text = "Kunde inte hitta LICENSE-filen."
    try:
        with open("../LICENSE", "r", encoding="utf-8") as file:
            license_text = file.read()
    except FileNotFoundError:
        pass

    # Create Text widget and Scrollbar
    license_label = tk.Text(frame, wrap="word", width=40, height=10)
    license_label.insert("1.0", "Licens:\n" + license_text)

    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=license_label.yview)
    license_label.config(yscrollcommand=scrollbar.set)

    # Position elements properly side-by-side
    license_label.grid(row=3, column=0, padx=(20, 0), pady=20, sticky="nsew")
    scrollbar.grid(row=3, column=1, padx=(0, 20), pady=20, sticky="ns")

    return frame

# --- HUVUDPROGRAM ---
root = tk.Tk()
root.title("P-Tools")
root.geometry("800x800")

icon_image = tk.PhotoImage(file="icons/icon.PNG")
root.iconphoto(True, icon_image)

top_image = tk.PhotoImage(file="icons/logo_image.PNG").subsample(2, 2)

style = ThemedStyle(root)
style.set_theme("equilux")

sidebar = ttk.Frame(root, width=150)
sidebar.grid(row=0, column=0, sticky="ns")

main_frame = ttk.Frame(root)
main_frame.grid(row=0, column=1, sticky="nsew")

root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(0, weight=1)

main_frame.grid_columnconfigure(0, weight=1)
main_frame.grid_rowconfigure(0, weight=1)

ripe_frame = create_ripe_view(main_frame, top_image)
imei_frame = create_imei_view(main_frame, top_image)
about_frame = create_about_view(main_frame, top_image)
phone_frame = create_phone_numbers_view(main_frame, top_image)
converter_frame = create_converter_view(main_frame, top_image)


def show_frame(frame):
    frame.tkraise()


lbl_menu = ttk.Label(sidebar, text="Menu", font=("Arial", 12, "bold"))
lbl_menu.grid(row=0, column=0, padx=10, pady=20)

btn_ripe = ttk.Button(
    sidebar, text="RIPE", width=15, command=lambda: show_frame(ripe_frame)
)
btn_ripe.grid(row=1, column=0, padx=10, pady=5)

#btn_IMEI_Checker = ttk.Button(
#    sidebar, text="IMEI-Checker", width=15, command=lambda: show_frame(imei_frame)
    #)
#btn_IMEI_Checker.grid(row=2, column=0, padx=10, pady=5)

btn_phone_number = ttk.Button(
    sidebar, text="Phone Numbers", width=15, command=lambda: show_frame(phone_frame)
)
btn_phone_number.grid(row=2, column=0, padx=10, pady=5)

btn_converter = ttk.Button(
    sidebar, text="Converter", width=15, command=lambda: show_frame(converter_frame)
)
btn_converter.grid(row=3, column=0, padx=10, pady=5)

btn_about_window = ttk.Button(
    sidebar, text="About", width=15, command=lambda: show_frame(about_frame)
)
btn_about_window.grid(row=4, column=0, padx=10, pady=5)

show_frame(ripe_frame)

root.mainloop()
