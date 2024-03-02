import cv2
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from PIL import Image, ImageTk
import os

class VideoFrameExtractorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Frame Extractor")
        self.root.geometry("400x200")

        self.video_path = tk.StringVar()
        self.output_path = tk.StringVar()
        self.progress_var = tk.DoubleVar()

        tk.Label(root, text="Video File:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.video_entry = tk.Entry(root, textvariable=self.video_path, width=40)
        self.video_entry.grid(row=0, column=1, padx=10, pady=10)
        tk.Button(root, text="Browse", command=self.browse_video).grid(row=0, column=2, padx=5, pady=10)

        tk.Label(root, text="Output Location:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.output_entry = tk.Entry(root, textvariable=self.output_path, width=40)
        self.output_entry.grid(row=1, column=1, padx=10, pady=10)
        tk.Button(root, text="Browse", command=self.browse_output).grid(row=1, column=2, padx=5, pady=10)

        self.progress_bar = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate", variable=self.progress_var)
        self.progress_bar.grid(row=2, columnspan=3, padx=10, pady=10)

        tk.Button(root, text="Extract Frames", command=self.extract_frames).grid(row=3, columnspan=3, pady=10)

    def browse_video(self):
        file_path = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4 *.avi *.mov")])
        self.video_path.set(file_path)

    def browse_output(self):
        output_path = filedialog.askdirectory()
        self.output_path.set(output_path)

    def extract_frames(self):
        video_path = self.video_path.get()
        output_dir = self.output_path.get()
        
        if not video_path or not output_dir:
            tk.messagebox.showerror("Error", "Please select video file and output directory")
            return

        try:
            os.makedirs(output_dir, exist_ok=True)
            cap = cv2.VideoCapture(video_path)
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            success, image = cap.read()
            count = 0

            while success:
                cv2.imwrite(os.path.join(output_dir, f"frame_{count}.jpg"), image)
                success, image = cap.read()
                count += 1
                progress_value = (count / total_frames) * 100
                self.progress_var.set(progress_value)
                self.root.update_idletasks()

            cap.release()
            tk.messagebox.showinfo("Extraction Complete", "Frames extracted successfully!")
        except Exception as e:
            tk.messagebox.showerror("Error", f"Error occurred: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoFrameExtractorApp(root)
    root.mainloop()
