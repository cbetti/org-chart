import os
import webbrowser


def showpicture(imagepath):
    # webbrowser.open politely invokes Preview for images
    abspath = os.path.abspath(imagepath)
    webbrowser.open('file://' + abspath)
