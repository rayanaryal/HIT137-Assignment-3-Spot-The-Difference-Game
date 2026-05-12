import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
import cv2


class SpotTheDifferenceGUI:
    def __init__(self, root, game_logic):
        self.root = root
        self.game_logic = game_logic

        self.root.title("Spot the Difference")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 700)
        self.root.resizable(True, True)

        self.tk_original = None
        self.tk_modified = None
        self.game_started = False
        self.win_shown = False
        self.game_over_shown = False

        self.build_layout()

    def build_layout(self):
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        self.title_frame = tk.Frame(self.root)
        self.title_frame.grid(row=0, column=0, sticky="ew", pady=(10, 5))

        self.title_label = tk.Label(
            self.title_frame,
            text="Spot the Difference",
            font=("Arial", 24, "bold")
        )
        self.title_label.pack()

        self.instruction_label = tk.Label(
            self.title_frame,
            text="Please click on 👉 New Game 👈  button at the bottom left of this screen to Enjoy. 😊",
            font=("Arial", 14),
            fg="gray"
        )
        self.instruction_label.pack(pady=(5, 0))


        self.canvas_frame = tk.Frame(self.root)
        self.canvas_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        self.canvas_frame.grid_columnconfigure(0, weight=1)
        self.canvas_frame.grid_columnconfigure(1, weight=1)
        self.canvas_frame.grid_rowconfigure(0, weight=1)

        self.original_canvas = tk.Canvas(self.canvas_frame, bg="black", highlightthickness=1, highlightbackground="gray")
        self.modified_canvas = tk.Canvas(self.canvas_frame, bg="black", highlightthickness=1, highlightbackground="gray")

        self.original_canvas.grid(row=0, column=0, sticky="n", padx=10, pady=10)
        self.modified_canvas.grid(row=0, column=1, sticky="n", padx=10, pady=10)

        self.modified_canvas.bind("<Button-1>", self.on_click)

        self.info_frame = tk.Frame(self.root)
        self.info_frame.grid(row=2, column=0, sticky="ew", pady=(0, 5))

        self.remaining_label = tk.Label(self.info_frame, text="Remaining: 0", font=("Arial", 12))
        self.mistake_label = tk.Label(self.info_frame, text="Mistakes: 0", font=("Arial", 12))

        self.remaining_label.pack(side="left", padx=20)
        self.mistake_label.pack(side="left", padx=20)

        self.button_frame = tk.Frame(self.root)
        self.button_frame.grid(row=3, column=0, sticky="ew", pady=(5, 10))

        self.new_game_button = tk.Button(self.button_frame, text="New Game", command=self.start_new_game, width=12)
        self.reveal_button = tk.Button(self.button_frame, text="Reveal All", command=self.reveal_all, width=12)
        self.quit_button = tk.Button(self.button_frame, text="Quit", command=self.root.quit, width=12)

        self.new_game_button.pack(side="left", padx=10)
        self.reveal_button.pack(side="left", padx=10)
        self.quit_button.pack(side="left", padx=10)

    def start_new_game(self):
        file_path = filedialog.askopenfilename(
            title="Select an Image",
            filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp")]
        )

        if not file_path:
            messagebox.showwarning("No Image Selected", "Please select an image to start the game.")
            return

        self.clear_canvas()
        self.game_logic.image_manager.image_path = file_path
        self.game_logic.start_game()

        self.load_images()
        self.update_labels()

        self.game_started = True
        self.win_shown = False
        self.game_over_shown = False

    def clear_canvas(self):
        self.original_canvas.delete("all")
        self.modified_canvas.delete("all")
        self.original_canvas.config(width=500, height=500)
        self.modified_canvas.config(width=500, height=500)

    def load_images(self):
        original = self.game_logic.image_manager.get_original_image()
        modified = self.game_logic.image_manager.get_modified_image()

        if original is None or modified is None:
            messagebox.showerror("Error", "Images could not be loaded.")
            return

        original_rgb = cv2.cvtColor(original, cv2.COLOR_BGR2RGB)
        modified_rgb = cv2.cvtColor(modified, cv2.COLOR_BGR2RGB)

        original_pil = Image.fromarray(original_rgb)
        modified_pil = Image.fromarray(modified_rgb)

        self.tk_original = ImageTk.PhotoImage(original_pil)
        self.tk_modified = ImageTk.PhotoImage(modified_pil)

        width, height = original_pil.size
        self.original_canvas.config(width=width, height=height)
        self.modified_canvas.config(width=width, height=height)

        self.original_canvas.delete("all")
        self.modified_canvas.delete("all")

        self.original_canvas.create_image(0, 0, anchor="nw", image=self.tk_original)
        self.modified_canvas.create_image(0, 0, anchor="nw", image=self.tk_modified)

    def on_click(self, event):
        if not self.game_started or self.tk_modified is None:
            return

        found, region = self.game_logic.check_click(event.x, event.y)

        if found and region is not None:
            self.draw_region(self.original_canvas, region, "red")
            self.draw_region(self.modified_canvas, region, "red")

            if self.game_logic.all_found() and not self.win_shown:
                self.win_shown = True
                messagebox.showinfo("Completed", "You found all differences!")

        else:
            if self.game_logic.is_game_over() and not self.game_logic.all_found() and not self.game_over_shown:
                self.game_over_shown = True
                messagebox.showinfo("Game Over", "Too many mistakes. Game over.")

        self.update_labels()

    def draw_region(self, canvas, region, color):
        x1, y1, x2, y2 = region.get_bbox()
        canvas.create_oval(x1, y1, x2, y2, outline=color, width=3)

    def reveal_all(self):
        if self.tk_modified is None:
            return

        unfound = self.game_logic.get_unfound_regions()

        for region in unfound:
            self.draw_region(self.original_canvas, region, "blue")
            self.draw_region(self.modified_canvas, region, "blue")

        self.game_logic.reveal_all()
        self.update_labels()

        if not self.win_shown:
            self.win_shown = True
            messagebox.showinfo("Reveal", "We are about to see all the differences.")

    def update_labels(self):
        remaining = self.game_logic.remaining_differences()
        mistakes = self.game_logic.get_mistakes()

        self.remaining_label.config(text=f"Remaining: {remaining}")
        self.mistake_label.config(text=f"Mistakes: {mistakes}/{self.game_logic.max_mistakes}")
