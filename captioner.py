import pexif
import os
import sys
import glob
import Tkinter
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
    root.label.configure(image=tkimage)
    root.label.image = tkimage
    root.label.pack()

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

        # Get caption from command line and add it to the metadata.
        print 'Enter a caption: '
        comment = sys.stdin.readline()
        source = pexif.JpegFile.fromFile(infile)
        source.exif.primary.ImageDescription = comment

        base_fname, ext = os.path.splitext(infile)

        source.writeFile(base_fname + "_captioned" + ext)

if len(sys.argv) > 1:
    path = sys.argv[1]
else:
    path = os.getcwd() + '/'

# Get a list of all JPEG files in directory
files = glob.glob(path + '*.jpg')

# Set up our window.
root = Tkinter.Tk()
root.label = Tkinter.Label(root)
root.label.pack()

# Run the captioning thread.
display = threading.Thread(target=CaptionApp, args=(root, files))
display.start()

root.mainloop()