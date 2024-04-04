import tkinter as tk
from tkinter import PhotoImage
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
import base64
import io
import wave
import base64
from getdata import *
import threading
import pyaudio


ding_WAVbase64 = get_ding_WAVbase64()
decoded_data = base64.b64decode(ding_WAVbase64) # Decode the base64 encoded string
wav_data = io.BytesIO(decoded_data) # Create a BytesIO object to handle the decoded data



# Base64 encoded icon
icon_data = get_icon_data()
icon_bytes = base64.b64decode(icon_data) # Convert base64 string to bytes




def play_ding():
    # Reset the file pointer to the beginning of the file
    wav_data.seek(0)

    with wave.open(wav_data, 'rb') as wf:
        # Create a PyAudio instance
        p = pyaudio.PyAudio()

        # Open a stream to play the audio
        stream = p.open(
            format=p.get_format_from_width(wf.getsampwidth()),
            channels=wf.getnchannels(),
            rate=wf.getframerate(),
            output=True
        )

        # Read data in chunks and play
        chunk_size = 1024
        data = wf.readframes(chunk_size)
        while data:
            stream.write(data)
            data = wf.readframes(chunk_size)

        # Close the stream and PyAudio instance
        stream.stop_stream()
        stream.close()
        p.terminate()

pomodor_timer = 25 * 60
rest_timer = 5 * 60

class TimerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Pomodoro timer ")
        self.master.configure(bg='black')
        self.master.attributes('-topmost', True)
        self.master.resizable(False, False) 
        icon_image = PhotoImage(data=icon_bytes)# Create a PhotoImage from the icon bytes
        self.master.iconphoto(True, icon_image)

        # Position the window in the top right corner of the screen
        screen_width = self.master.winfo_screenwidth()
        window_width = 200  # Set the desired window width
        window_height = 100  # Set the desired window height
        x_position = screen_width - window_width
        y_position = 100
        self.master.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

        self.main_timer_seconds = pomodor_timer
        self.rest_timer_seconds = rest_timer
        self.is_timer_running = False
        self.is_counting_up = False
        self.is_rest_timer_active = False
        self.is_paused = False
        self.is_blinking = False
        self.timer_id = None  # Store the ID of the scheduled timer_tick

        self.timer_label = tk.Label(master, text=self.format_time(self.main_timer_seconds), font=("Arial", 20), fg='white', bg='black')
        self.timer_label.pack(pady=10)
        self.timer_label.bind("<Button-1>", self.toggle_pause)

        self.start_button = tk.Button(master, text="Start", command=self.start_main_timer, bg='black', fg='white')
        self.start_button.pack(side=tk.LEFT, padx=5)

        self.stop_button = tk.Button(master, text="Stop", command=self.stop_timer, bg='black', fg='white')
        self.stop_button.pack(side=tk.LEFT, padx=5)
        self.stop_button.pack_forget()

        self.rest_button = tk.Button(master, text="Rest", command=self.start_or_reset_rest_timer, bg='black', fg='white')
        self.rest_button.pack(side=tk.LEFT, padx=5)

        self.skip_button = tk.Button(master, text="Skip", command=self.skip_rest_timer, bg='black', fg='white')
        self.skip_button.pack(side=tk.LEFT, padx=5)
        self.skip_button.pack_forget()

        self.timer_mode_var = tk.IntVar()  # Variable to store the checkbox state
        self.timer_mode_checkbox = tk.Checkbutton(master, text="50/10", variable=self.timer_mode_var, bg='black', fg='white', selectcolor='black', command=self.update_timer_mode)
        self.timer_mode_checkbox.pack(side=tk.LEFT, padx=5)

        self.check_window_state()

        self.start_server()

    def start_server(self):
        def run_server():
            server_address = ('', 7847)
            httpd = HTTPServer(server_address, TimerServer)
            print('Starting server on port 7847...')
            httpd.serve_forever()

        server_thread = threading.Thread(target=run_server)
        server_thread.daemon = True  # Daemonize thread
        server_thread.start()

    def update_timer_mode(self):
        global pomodor_timer
        global rest_timer
        if self.timer_mode_var.get() == 1:
            self.main_timer_seconds = 50 * 60  # 50 minutes
            self.rest_timer_seconds = 10 * 60   # 10 minutes
            pomodor_timer = self.main_timer_seconds
            rest_timer = self.rest_timer_seconds
        else:
            self.main_timer_seconds = 25 * 60  # 25 minutes
            self.rest_timer_seconds = 5 * 60    # 5 minutes
            pomodor_timer = self.main_timer_seconds
            rest_timer = self.rest_timer_seconds

    def format_time(self, seconds):
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes:02d}:{seconds:02d}"

    def update_timer_label(self, blink=False):
        if self.is_rest_timer_active:
            self.timer_label.config(fg='orange' if not blink else 'black')
            self.timer_label.config(text=self.format_time(self.rest_timer_seconds))
        elif self.is_counting_up:
            self.timer_label.config(fg='green' if not blink else 'black')
            self.timer_label.config(text=self.format_time(self.main_timer_seconds))
        else:
            self.timer_label.config(fg='white' if not blink else 'black')
            self.timer_label.config(text=self.format_time(self.main_timer_seconds))

    def timer_tick(self):
        if self.is_timer_running and not self.is_paused:
            if self.is_rest_timer_active:
                self.rest_timer_seconds -= 1
                if self.rest_timer_seconds == 0:
                    play_ding_thread = threading.Thread(target=play_ding)
                    play_ding_thread.start()
                    self.skip_rest_timer()
            elif self.is_counting_up:
                self.main_timer_seconds += 1
            else:
                self.main_timer_seconds -= 1
                if self.main_timer_seconds == 0:
                    self.is_counting_up = True
                    play_ding_thread = threading.Thread(target=play_ding)
                    play_ding_thread.start()
            self.update_timer_label()
            self.timer_id = self.master.after(1000, self.timer_tick)

    def start_main_timer(self):
        if not self.is_timer_running:
            self.is_timer_running = True
            self.is_counting_up = False
            self.is_rest_timer_active = False
            self.is_paused = False
            self.is_blinking = False
            if self.timer_id:
                self.master.after_cancel(self.timer_id)  # Cancel any existing timer_tick
            self.timer_tick()
            self.start_button.pack_forget()
            self.stop_button.pack(side=tk.LEFT, padx=5)

    def start_or_reset_rest_timer(self):
        if self.is_timer_running and not self.is_paused:
            self.is_rest_timer_active = True
            self.rest_timer_seconds = rest_timer
            self.update_timer_label()
            self.skip_button.pack(side=tk.LEFT, padx=5)
            if self.timer_id:
                self.master.after_cancel(self.timer_id)  # Cancel any existing timer_tick
            self.timer_tick()

    def stop_timer(self):
        self.is_timer_running = False
        self.is_counting_up = False
        self.is_rest_timer_active = False
        self.is_paused = False
        self.is_blinking = False
        if self.timer_id:
            self.master.after_cancel(self.timer_id)  # Cancel any existing timer_tick
        self.timer_id = None
        self.main_timer_seconds = pomodor_timer
        self.rest_timer_seconds = rest_timer
        self.update_timer_label()
        self.skip_button.pack_forget()
        self.stop_button.pack_forget()
        self.start_button.pack(side=tk.LEFT, padx=5)

    def skip_rest_timer(self):
        self.is_rest_timer_active = False
        self.rest_timer_seconds = rest_timer
        self.is_counting_up = False
        self.main_timer_seconds = pomodor_timer
        self.is_paused = False
        self.is_blinking = False
        if self.timer_id:
            self.master.after_cancel(self.timer_id)  # Cancel any existing timer_tick
        self.timer_id = None
        self.update_timer_label()
        self.skip_button.pack_forget()
        self.stop_button.pack_forget()
        self.start_button.pack(side=tk.LEFT, padx=5)

    def toggle_pause(self, event):
        if self.is_timer_running:
            self.is_paused = not self.is_paused
            if self.is_paused:
                self.start_blinking()
                if self.timer_id:
                    self.master.after_cancel(self.timer_id)  # Cancel any existing timer_tick
                    self.timer_id = None
            else:
                self.stop_blinking()
                self.timer_tick()

    def start_blinking(self):
        if not self.is_blinking:
            self.is_blinking = True
            self.blink()

    def stop_blinking(self):
        self.is_blinking = False
        self.update_timer_label()

    def blink(self):
        if self.is_blinking:
            self.update_timer_label(blink=True)
            self.master.after(500, lambda: self.update_timer_label(blink=False))
            self.master.after(1000, self.blink)

    def check_window_state(self):
        if self.master.wm_state() == 'iconic':
            self.master.wm_state('normal')
        self.master.after(100, self.check_window_state)

class TimerServer(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/isactive':
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            if app.is_timer_running and not app.is_rest_timer_active:
                self.wfile.write(b'active')
            else:
                self.wfile.write(b'unactive')
        else:
            self.send_response(404)
            self.end_headers()


if __name__ == "__main__":
    root = tk.Tk()
    app = TimerApp(root)
    root.mainloop()