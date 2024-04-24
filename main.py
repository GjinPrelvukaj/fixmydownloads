import os
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

def monitor_downloads_folder(icon):
    # Get the path to the downloads folder from the environment variables
    downloads_folder_path = os.path.join(os.path.expanduser('~'), 'Downloads')

    # List all files in the downloads folder
    files = os.listdir(downloads_folder_path)
    
    for file in files:
        file_path = os.path.join(downloads_folder_path, file)
        if os.path.isfile(file_path):
            filename, file_extension = os.path.splitext(file)
            print(f"Downloaded file: {file} | Extension: {file_extension}")

def organize_photos(icon):
    organize_files_by_type('Photos')

def organize_videos(icon):
    organize_files_by_type('Videos')

def organize_compressed(icon):
    organize_files_by_type('Compressed')

def organize_executables(icon):
    organize_files_by_type('Executables')

def organize_torrents(icon):
    organize_files_by_type('Torrents')

def organize_ebooks(icon):
    organize_files_by_type('Ebooks')

def organize_presentations(icon):
    organize_files_by_type('Presentations')

def organize_spreadsheets(icon):
    organize_files_by_type('Spreadsheets')

def organize_documents(icon):
    organize_files_by_type('Documents')

def organize_all(icon):
    for file_type in folder_extensions:
        organize_files_by_type(file_type)

def delete_temp_files(icon):
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

        print("Temporary files deleted successfully.")

    except Exception as e:
        print(f"Error accessing temporary files folder: {e}")

def organize_files_by_type(file_type):
    downloads_folder_path = os.path.join(os.path.expanduser('~'), 'Downloads')

    # Create the main 'Organize' folder if it doesn't exist
    organize_folder_path = os.path.join(downloads_folder_path, 'OrganizeTM')
    if not os.path.exists(organize_folder_path):
        os.makedirs(organize_folder_path)

    # Define the folder path for the specified file type
    if file_type == 'Torrents':
        folder_path = os.path.join(organize_folder_path, 'Torrents')
    elif file_type in ['Ebooks', 'Presentations', 'Spreadsheets']:
        folder_path = os.path.join(organize_folder_path, file_type)
    else:
        folder_path = os.path.join(organize_folder_path, file_type)

    # Create the folder if it doesn't exist
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # List all files in the downloads folder
    files = os.listdir(downloads_folder_path)

    # Move files to the appropriate folder based on their extensions
    for file in files:
        file_path = os.path.join(downloads_folder_path, file)
        if os.path.isfile(file_path):
            _, file_extension = os.path.splitext(file)
            if file_extension.lower() in folder_extensions[file_type]:
                destination_path = os.path.join(folder_path, file)
                os.rename(file_path, destination_path)
                log_organize_action(file, file_extension, destination_path)
    
    print(f"{file_type} organized successfully.")

def log_organize_action(file_name, file_extension, destination):
    now = datetime.now()
    date_time = now.strftime("%Y-%m-%d-%H-%M-%S")
    log_file_name = f"OrganizeLog-{date_time}.txt"
    log_folder_path = os.path.join(os.path.expanduser('~'), 'Downloads', 'OrganizeLogs')
    log_file_path = os.path.join(log_folder_path, log_file_name)
    
    # Create the OrganizeLogs folder if it doesn't exist
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
    
    # Create the DeleteLog folder if it doesn't exist
    if not os.path.exists(log_folder_path):
        os.makedirs(log_folder_path)
    
    with open(log_file_path, 'a') as log_file:
        log_file.write(f"Deleted File: {file_path}\n")

def on_clicked(icon, item):
    if str(item) == "Exit":
        icon.stop()
    elif str(item) == "Github":
        webbrowser.open('https://github.com/GjinPrelvukaj/fixmydownloads/')

image = PIL.Image.open("fmd.png")

icon = pystray.Icon("FMD", image, menu=pystray.Menu(
    pystray.MenuItem("Organize", pystray.Menu(
        pystray.MenuItem("Photos", organize_photos),
        pystray.MenuItem("Videos", organize_videos),
        pystray.MenuItem("Documents", organize_documents),
        pystray.MenuItem("Compressed", organize_compressed),
        pystray.MenuItem("Executables", organize_executables),
        pystray.MenuItem("Others", pystray.Menu(
            pystray.MenuItem("Torrents", organize_torrents),
            pystray.MenuItem("Ebooks", organize_ebooks),
            pystray.MenuItem("Presentations", organize_presentations),
            pystray.MenuItem("Spreadsheets", organize_spreadsheets),
        )),
    )),
    pystray.MenuItem("Delete Temp Files", delete_temp_files),
    pystray.MenuItem("Exit", on_clicked),
    pystray.MenuItem("Links", pystray.Menu(
        pystray.MenuItem("Github", on_clicked),
    ))
))

icon.run()
