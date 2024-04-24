import os
import tkinter as tk
from tkinter import ttk, messagebox  # Import messagebox module
import pystray
import PIL.Image
import webbrowser
from datetime import datetime

folder_extensions = {
    'Photos': ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.webp'],
    'Videos': ['.mp4', '.mov', '.avi', '.mkv', '.wmv', '.flv'],
    'Compressed': ['.zip', '.rar', '.7z', '.tar', '.gz'],
    'Executables': ['.exe', '.msi', '.bat', '.sh'],
    'Torrents': ['.torrent'],
    'Ebooks': ['.pdf', '.epub', '.mobi'],
    'Presentations': ['.ppt', '.pptx'],
    'Spreadsheets': ['.xls', '.xlsx'],
    'Documents': ['.doc', '.docx', '.txt', '.pdf']
}

def log_organize_action(file_name, file_extension, destination):
    now = datetime.now()
    date_time = now.strftime("%Y-%m-%d-%H-%M-%S")
    log_file_name = f"OrganizeLog-{date_time}.txt"
    log_folder_path = os.path.join(os.path.expanduser('~'), 'Downloads', 'OrganizeLogs')
    log_file_path = os.path.join(log_folder_path, log_file_name)
    
    if not os.path.exists(log_folder_path):
        os.makedirs(log_folder_path)
    
    with open(log_file_path, 'a') as log_file:
        log_file.write(f"File Name: {file_name}\n")
        log_file.write(f"File Extension: {file_extension}\n")
        log_file.write(f"Destination: {destination}\n\n")

def log_delete_action(file_path):
    now = datetime.now()
    date_time = now.strftime("%Y-%m-%d-%H-%M-%S")
    log_file_name = f"DeleteLog-{date_time}.txt"
    log_folder_path = os.path.join(os.path.expanduser('~'), 'Downloads', 'DeleteLog')
    log_file_path = os.path.join(log_folder_path, log_file_name)
    
    if not os.path.exists(log_folder_path):
        os.makedirs(log_folder_path)
    
    with open(log_file_path, 'a') as log_file:
        log_file.write(f"Deleted File: {file_path}\n")

def organize_files(file_type):
    downloads_folder_path = os.path.join(os.path.expanduser('~'), 'Downloads')
    folder_path = os.path.join(downloads_folder_path, file_type)
    
    if file_type == 'Torrents':
        folder_path = os.path.join(downloads_folder_path, 'Others', 'Torrents')
    elif file_type in ['Ebooks', 'Presentations', 'Spreadsheets']:
        folder_path = os.path.join(downloads_folder_path, 'Others', file_type)
    
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    files = os.listdir(downloads_folder_path)

    organized_files = 0  # Variable to count the number of organized files

    for file in files:
        file_path = os.path.join(downloads_folder_path, file)
        if os.path.isfile(file_path):
            _, file_extension = os.path.splitext(file)
            if file_extension.lower() in folder_extensions[file_type]:
                destination_path = os.path.join(folder_path, file)
                os.rename(file_path, destination_path)
                log_organize_action(file, file_extension, destination_path)
                organized_files += 1  # Increment the count

    if organized_files > 0:
        messagebox.showinfo("Organize Files", f"All {file_type} files have been organized.")

    print(f"{file_type} organized successfully.")

def delete_temp_files():
    temp_folder_path = os.path.join(os.environ['LOCALAPPDATA'], 'Temp')
    try:
        deleted_files_count = 0
        for file in os.listdir(temp_folder_path):
            file_path = os.path.join(temp_folder_path, file)
            if os.path.isfile(file_path):
                try:
                    os.remove(file_path)
                    log_delete_action(file_path)
                    deleted_files_count += 1
                except Exception as e:
                    print(f"Error deleting file {file_path}: {e}")

        if deleted_files_count > 0:
            messagebox.showinfo("Delete Temp Files", "Temporary files deleted successfully.")
        else:
            messagebox.showinfo("Delete Temp Files", "No temporary files found.")

    except Exception as e:
        print(f"Error accessing temporary files folder: {e}")

def on_open_click():
    root = tk.Tk()
    root.title("Downloads Organizer")
    root.geometry("400x300")  # Set a larger window size

    def on_file_type_change(*args):
        file_type = selected_file_type.get()
        menu = file_type_menu["menu"]
        menu.delete(0, "end")

        for file_type in folder_extensions.keys():
            menu.add_command(label=file_type, command=tk._setit(selected_file_type, file_type))

    # Add a dropdown menu to select the file type
    selected_file_type = tk.StringVar(root)
    selected_file_type.set("Photos")  # Default value

    file_type_menu = ttk.OptionMenu(root, selected_file_type, *list(folder_extensions.keys()), command=on_file_type_change)
    file_type_menu.pack(pady=10)

    def organize_selected():
        organize_files(selected_file_type.get())  # Call the organize_files function

    def delete_temp():
        delete_temp_files()  # Call delete_temp_files function

    # Add buttons to trigger the organization and delete processes
    organize_button = ttk.Button(root, text="Organize", command=organize_selected)
    organize_button.pack(pady=10)

    delete_button = ttk.Button(root, text="Delete Temp Files", command=delete_temp)
    delete_button.pack(pady=10)

    root.mainloop()

def on_exit_click():
    icon.stop()

def on_clicked(icon, item):
    if str(item) == "Hello World":
        print("Hello World")
    elif str(item) == "Exit":
        on_exit_click()
    elif str(item) == "Github":
        webbrowser.open('https://github.com/GjinPrelvukaj/fixmydownloads/')

image = PIL.Image.open("fmd.png")

icon = pystray.Icon("FMD", image, menu=pystray.Menu(
    pystray.MenuItem("Open", on_open_click),
    pystray.MenuItem("Say Hello", on_clicked),
    pystray.MenuItem("Organize", pystray.Menu(
        *[pystray.MenuItem(file_type, lambda _: organize_files(file_type)) for file_type in folder_extensions.keys()]
    )),
    pystray.MenuItem("Exit", on_clicked),
    pystray.MenuItem("Links", pystray.Menu(
        pystray.MenuItem("Github", on_clicked),
    ))
))

icon.run()
