import pexif
import os
import sys
import glob
import Tkinter
import tkMessageBox
import threading
from PIL import Image
from PIL import ImageTk

def updateImage(root, filename):
    im = Image.open(filename)

    # Scale image by half until it fits on the screen
    while im.size[0] > 1600 or im.size[1] > 900:
        im = im.resize((im.size[0] / 2, im.size[1] / 2), Image.ANTIALIAS)

    tkimage = ImageTk.PhotoImage(im)

    # Draw the new image
    root.title("Captioner 0.1a: " + filename)
    root.toplabel.configure(image=tkimage)
    root.toplabel.image = tkimage
    root.toplabel.pack()

def waitForInput():
    root.input_ready.wait()

    # Check to see if we were woken up by the window close event.
    if root.closed:
        sys.exit(0)

    root.input_ready.clear()
    return root.entry.get()

def CaptionApp(root, files):
    for infile in files:

        """
        Set up NextImage event handler to use the default arguments
        of our root window and the file we want to caption.
        """
        def handler(event, root=root, filename=infile):
            updateImage(root, filename)

        # Bind the handler and draw the image.
        root.bind("<<NextImage>>", handler)
        root.event_generate("<<NextImage>>")

        # Get caption from our text box. and add it to the metadata.
        comment = waitForInput()
        root.entry.delete(0, Tkinter.END)
        source = pexif.JpegFile.fromFile(infile)
        source.exif.primary.ImageDescription = comment

        base_fname, ext = os.path.splitext(infile)

        source.writeFile(base_fname + "_captioned" + ext)

    # We have processed all the files.  Now close our window.
    root.quit()

def onClose():
    if DEBUG:
        root.closed = True
        root.input_ready.set()
        root.destroy()
        root.quit()
        sys.exit(0)
        
    if tkMessageBox.askokcancel(
            "Quit?", "Are you sure you want to quit?"):
        root.input_ready.set()
        root.closed = True
        root.destroy()
        root.quit()        
        sys.exit(0)

if len(sys.argv) > 1:
    path = sys.argv[1]
else:
    path = os.getcwd() + '/'


DEBUG = True
# Get a list of all JPEG files in directory
files = glob.glob(path + '*.jpg')

if len(files) == 0:
    print 'No JPEG files found in ' + path
    sys.exit(0)

# Set up our window.
root = Tkinter.Tk()

# Create an event for communication between data editing thread
# and the window thread so we know to write out the caption
root.input_ready = threading.Event()
root.closed = False

root.toplabel = Tkinter.Label(root)
root.toplabel.pack()
root.bottomlabel = Tkinter.Label(root)
root.bottomlabel.pack()
root.bottomlabel.entry = Tkinter.Entry(root.bottomlabel, width=50)
root.bottomlabel.entry.grid(row=0)

# Bind pressing Enter while in the text field to accept the caption
# Use a lambda binding to discard the event argument as it is not needed
root.bottomlabel.entry.bind('<Return>', lambda x: root.input_ready.set())

root.bottomlabel.button = Tkinter.Button(root.bottomlabel,
                             text='Ok',
                             width=10,
                             command=root.input_ready.set)
root.bottomlabel.button.grid(row=0, column=1)

# Set up a handler for the window close event
root.protocol("WM_DELETE_WINDOW", onClose)

# Run the captioning thread.
display = threading.Thread(target=CaptionApp, args=(root, files))
display.start()

root.mainloop()
