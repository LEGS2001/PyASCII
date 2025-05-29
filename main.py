import cv2
import os
import sys
import shutil
import time

# Mapa de caracteres ASCII por brillo
ASCII_CHARS = " .:-=+*#%@"
def brightness_to_char(v):
    return ASCII_CHARS[int(v / 256 * len(ASCII_CHARS))]

def get_terminal_size():
    size = shutil.get_terminal_size(fallback=(80, 24))
    return size.columns, size.lines

def pixel_to_ansi(r, g, b, char):
    return f"\033[38;2;{r};{g};{b}m{char}\033[0m"

video_path = "video.mp4"  # Cambia esto por tu ruta de video
cap = cv2.VideoCapture(video_path)

fps = cap.get(cv2.CAP_PROP_FPS)
if fps <= 0:
    fps = 24  # valor por defecto si no se puede leer

frame_count = 0
start_time = time.time()

# Oculta el cursor
print("\033[?25l", end="")

try:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        term_width, term_height = get_terminal_size()
        new_width = term_width
        new_height = term_height  # ajustar relación de aspecto vertical

        frame = cv2.resize(frame, (new_width, new_height))
        output = ""

        for row in frame:
            for pixel in row:
                b, g, r = pixel
                brightness = 0.2126 * r + 0.7152 * g + 0.0722 * b
                char = brightness_to_char(brightness)
                output += pixel_to_ansi(r, g, b, char)
            output += "\n"

        # Mover cursor al inicio sin limpiar pantalla (más rápido y sin parpadeo)
        print("\033[H", end="")
        sys.stdout.write(output)
        sys.stdout.flush()

        frame_count += 1
        elapsed = time.time() - start_time
        expected = frame_count / fps
        to_sleep = expected - elapsed
        if to_sleep > 0:
            time.sleep(to_sleep)

finally:
    cap.release()
    # Muestra el cursor de nuevo al salir
    print("\033[?25h")
