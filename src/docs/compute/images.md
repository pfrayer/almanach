# Images, videos & PDF

## Reduce PDF size on Linux

Use `ghostscript` to reduce PDF size without altering PDF quality too much.

```shell
# Install ghostscript
$ sudo apt install ghostscript

# Use it, update input & output paths
$ gs -dNOPAUSE \
    -dBATCH \
    -sDEVICE=pdfwrite \
    -dCompatibilityLevel=1.4 \
    -dPDFSETTINGS=/ebook \
    -sOutputFile=/path/to/output.pdf \
    /path/to/input.pdf
```

Here the lower quality (and thus the smallest size) is brought by the `-dPDFSETTINGS=/ebook` param.

Other possible values for this params are (from lower quality to best quality):

- `/screen`: low-resolution output similar to the Acrobat Distiller (up to version X) "Screen Optimized" setting.
- `/ebook`: medium-resolution output similar to the Acrobat Distiller (up to version X) "eBook" setting.
- `/printer`: output similar to the Acrobat Distiller "Print Optimized" (up to version X) setting.
- `/prepress`: output similar to Acrobat Distiller "Prepress Optimized" (up to version X) setting.

## Convert image to .webp format

```shell
$ sudo apt install webp

# -q is the quality to keep in percent
# -o is the name of the output file
$ cwebp -q 100 my_image.png -o my_image.webp
```

## Resize images

```shell
$ sudo apt install imagemagick

# Resize image in fixed dimensions
$ convert my_image.webp -resize 200x100 my_image_resized.webp

# Resize image in %
$ convert my_image.webp -resize 700% my_image.webp

# Resise big image without impacting computer memory
$ convert -limit memory 2mb -limit map 2mb my_image.webp -resize 700% my_image.webp
```
