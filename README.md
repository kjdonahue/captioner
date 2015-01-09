captioner.py: a simple application to add captions to the ImageDescription
field of images' EXIF metadata.

For the time being the application simply copies the image with updated
metadata from 'foo.jpg' to 'foo_captioned.jpg'.

Future plans:
-Move from reading from command line to a prompt within the viewing window
-Make sure extra large captions do not overwrite other EXIF fields or image
      data

Send all questions or comments to:
Kyle Donahue
kyle.donahue@gmail.com

Changelog:
v0.1 - initial version.  Supports command-line caption entry.