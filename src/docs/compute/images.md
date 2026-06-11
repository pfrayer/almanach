# Images, videos & PDF

## Images — ImageMagick

```shell
apt install imagemagick

# Convert format
convert image.png image.jpg

# Resize to fixed dimensions
convert image.png -resize 800x600 out.png

# Resize by percentage
convert image.png -resize 50% out.png

# Strip EXIF metadata
convert image.jpg -strip out.jpg

# Batch convert all PNG → JPG
mogrify -format jpg *.png
```

## Images — WebP

```shell
apt install webp

# Encode to WebP (-q = quality 0-100)
cwebp -q 85 image.png -o image.webp

# Decode WebP → PNG
dwebp image.webp -o image.png
```

## Video — ffmpeg

```shell
apt install ffmpeg

# Convert format
ffmpeg -i input.mov output.mp4

# Extract audio
ffmpeg -i input.mp4 -vn output.mp3

# Trim (from 00:01:00, duration 30s)
ffmpeg -i input.mp4 -ss 00:01:00 -t 30 output.mp4

# Scale to 1280px wide (keep ratio)
ffmpeg -i input.mp4 -vf scale=1280:-2 output.mp4

# Extract a frame at timestamp
ffmpeg -i input.mp4 -ss 00:00:05 -frames:v 1 frame.png
```

## PDF — Ghostscript

```shell
apt install ghostscript

# Compress PDF
gs -dNOPAUSE -dBATCH -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 \
    -dPDFSETTINGS=/ebook \
    -sOutputFile=output.pdf input.pdf
```

`-dPDFSETTINGS` values (low → high quality): `/screen` · `/ebook` · `/printer` · `/prepress`

```shell
# Merge PDFs
gs -dNOPAUSE -dBATCH -sDEVICE=pdfwrite -sOutputFile=merged.pdf a.pdf b.pdf

# Extract pages 2-5
gs -dNOPAUSE -dBATCH -sDEVICE=pdfwrite -dFirstPage=2 -dLastPage=5 \
    -sOutputFile=extract.pdf input.pdf
```
