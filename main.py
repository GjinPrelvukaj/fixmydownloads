import pystray
import PIL.Image
import webbrowser

image = PIL.Image.open("fmd.png")

def on_clicked(icon, item):
    if str(item) == "Hello World":
        print("Hello World")
    elif str(item) == "Exit":
        icon.stop()
    elif str(item) == "Github":
        webbrowser.open('http://example.com')



icon = pystray.Icon("FMD", image, menu=pystray.Menu(
    pystray.MenuItem("Say Hello", on_clicked),
    pystray.MenuItem("Exit", on_clicked),
    pystray.MenuItem("Links", pystray.Menu(
        pystray.MenuItem("Github", on_clicked),
    ))
))

icon.run()