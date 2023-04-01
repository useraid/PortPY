import socket
import threading
import tkinter as tk
import tkinter.ttk as ttk

class PortScannerWindow:

    def __init__(self, master):
        self.master = master
        master.title("Port Scanner")
        self.main_frame = tk.Frame(master)
        self.target_label = tk.Label(self.main_frame, text="Target IP address:")
        self.target_input = tk.Entry(self.main_frame)
        self.threads_label = tk.Label(self.main_frame, text="Number of threads:")
        self.threads_input = tk.Entry(self.main_frame)
        self.scan_button = tk.Button(self.main_frame, text="Scan", command=self.scan_ports)
        self.stop_button = tk.Button(self.main_frame, text="Stop", state="disabled", command=self.stop_scan)
        self.result_label = tk.Label(self.main_frame, text="Scan results:")
        self.result_text = tk.Text(self.main_frame, state="disabled")
        self.progress_label = tk.Label(self.main_frame, text="Progress:")
        self.progress_bar = ttk.Progressbar(self.main_frame, orient=tk.HORIZONTAL, length=200, mode='determinate')
        self.target_label.pack()
        self.target_input.pack()
        self.threads_label.pack()
        self.threads_input.pack()
        self.scan_button.pack(side="left", padx=(0, 10))
        self.stop_button.pack(side="left")
        self.result_label.pack()
        self.result_text.pack()
        self.progress_label.pack()
        self.progress_bar.pack()
        self.main_frame.pack()
        self.scan_running = False

    def scan_port(self, port):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((self.target_input.get(), port))
            if result == 0:
                self.result_text.config(state="normal")
                self.result_text.insert(tk.END, "Port {} is open\n".format(port))
                self.result_text.config(state="disabled")
            sock.close()
        except:
            pass

    def start_threads(self):
        for i in range(int(self.threads_input.get())):
            thread = threading.Thread(target=self.scan_thread)
            thread.start()

    def scan_range(self, start_port, end_port):
        for port in range(start_port, end_port):
            if not self.scan_running:
                break
            self.scan_port(port)
            progress = (port - start_port + 1) / (end_port - start_port) * 100
            self.progress_bar["value"] = progress
            self.master.update()

    def scan_thread(self):
        while True:
            port = None
            with self.lock:
                if len(self.ports) > 0:
                    port = self.ports.pop(0)
            if port is not None:
                self.scan_port(port)
            if port is None:
                break

    def scan_ports(self):
        self.result_text.config(state="normal")
        self.result_text.delete("1.0", tk.END)
        self.result_text.config(state="disabled")
        self.progress_bar["value"] = 0
        self.scan_running = True
        self.lock = threading.Lock()
        self.ports = list(range(1, 65536))
        self.start_threads()
        self.scan_range(1, 65536)
        self.scan_running = False
        self.stop_button.config(state="disabled")
        self.scan_button.config(state="normal")

    def stop_scan(self):
        self.scan_running = False
        self.stop_button.config(state="disabled")
        self.scan_button.config(state="normal")

root = tk.Tk()
scanner_window = PortScannerWindow(root)
root.mainloop()
