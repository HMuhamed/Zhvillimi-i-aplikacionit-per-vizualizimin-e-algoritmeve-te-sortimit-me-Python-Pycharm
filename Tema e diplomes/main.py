import tkinter as tk
from PIL import Image, ImageTk
from merge_sort_draft import MergeSortVisualizer
from counting_sort_draft import CountingSortVisualizer
from bucket_sort_draft import BucketSortVisualizer
import os


class SortingVisualizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sorting Algorithm Visualizer")
        self.root.geometry("600x400")
        self.root.configure(bg="#e0f7fa")

        # Set the icon for the main window
        icon_path = os.path.join(os.path.dirname(__file__), "icon.png")
        self.root.iconphoto(False, tk.PhotoImage(file=icon_path))

        # Maximize the window
        self.root.state('zoomed')

        self.container = tk.Frame(root, bg="#e0f7fa")
        self.container.pack(fill=tk.BOTH, expand=True)

        # Load and resize the icon image to be displayed above the label
        icon_img = Image.open(icon_path)
        icon_img = icon_img.resize((100, 100), Image.LANCZOS)  # Resize the icon using LANCZOS method
        self.icon_img = ImageTk.PhotoImage(icon_img)

        # Create a new frame for the image to place it at the top
        image_frame = tk.Frame(self.container, bg="#e0f7fa")
        image_frame.pack(pady=(20, 0))  # Adjusted padding above the image frame

        icon_label = tk.Label(image_frame, image=self.icon_img, bg="#e0f7fa")
        icon_label.pack()

        label = tk.Label(self.container, text="Select a Sorting Algorithm to Visualize",
                         font=("Helvetica", 18, "bold"), bg="#e0f7fa", fg="#00796b")
        label.pack(pady=(20, 50))  # Increased padding below the label

        button_style = {
            'font': ("Helvetica", 14),
            'bg': "#00796b",
            'fg': "white",
            'activebackground': "#004d40",
            'activeforeground': "white",
            'width': 20,
            'height': 2,
            'bd': 0,
            'highlightthickness': 0
        }

        btn_merge_sort = tk.Button(self.container, text="Merge Sort", command=self.run_merge_sort, **button_style)
        btn_merge_sort.pack(pady=(10, 10))

        btn_counting_sort = tk.Button(self.container, text="Counting Sort", command=self.run_counting_sort,
                                      **button_style)
        btn_counting_sort.pack(pady=(10, 10))

        btn_bucket_sort = tk.Button(self.container, text="Bucket Sort", command=self.run_bucket_sort, **button_style)
        btn_bucket_sort.pack(pady=(10, 10))

        btn_help = tk.Button(self.container, text="Help", command=self.show_help, **button_style)
        btn_help.pack(pady=(10, 20))

        root.bind('<Configure>', self.on_resize)

    def on_resize(self, event):
        # Center the container when the window is resized
        self.container.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    def run_merge_sort(self):
        self.hide_main_window()
        self.choose_array_type(MergeSortVisualizer)

    def run_counting_sort(self):
        self.hide_main_window()
        self.choose_array_type(CountingSortVisualizer)

    def run_bucket_sort(self):
        self.hide_main_window()
        self.choose_array_type(BucketSortVisualizer)

    def choose_array_type(self, visualizer_class):
        self.array_type_window = tk.Toplevel(self.root)
        self.array_type_window.title("Choose Array Type")
        self.array_type_window.geometry("400x300")
        self.array_type_window.configure(bg="#e0f7fa")

        # Set the icon for the array type window
        self.array_type_window.iconphoto(False, self.icon_img)

        # Maximize the window
        self.array_type_window.state('zoomed')

        # Create a container frame to hold the buttons and label
        container = tk.Frame(self.array_type_window, bg="#e0f7fa")
        container.pack(fill=tk.BOTH, expand=True)

        # Move icons above "Choose Array Type"
        icon_label = tk.Label(container, image=self.icon_img, bg="#e0f7fa")
        icon_label.pack(pady=(50, 10))  # Adjusted padding above icon label

        label = tk.Label(container, text="Choose Array Type", font=("Helvetica", 16, "bold"), bg="#e0f7fa",
                         fg="#00796b")
        label.pack(pady=(20, 10))  # Adjusted padding above label

        button_style = {
            'font': ("Helvetica", 14),
            'bg': "#00796b",
            'fg': "white",
            'activebackground': "#004d40",
            'activeforeground': "white",
            'width': 20,
            'height': 2,
            'bd': 0,
            'highlightthickness': 0
        }

        btn_random_array = tk.Button(container, text="Random Array",
                                     command=lambda: self.start_visualizer(visualizer_class, "random"), **button_style)
        btn_random_array.pack(pady=10)

        btn_custom_array = tk.Button(container, text="Custom Array",
                                     command=lambda: self.start_visualizer(visualizer_class, "custom"), **button_style)
        btn_custom_array.pack(pady=10)

        # Bind the resize event to maintain centering
        self.array_type_window.bind('<Configure>', lambda event: self.on_resize_array_type_window(container))

    def on_resize_array_type_window(self, container):
        container.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    def start_visualizer(self, visualizer_class, array_type):
        self.array_type_window.destroy()
        visualizer_class(array_type=array_type, on_back_callback=self.show_main_window)

    def hide_main_window(self):
        self.root.withdraw()

    def show_main_window(self):
        self.root.deiconify()
        self.root.state('zoomed')  # Maximize the window again

    def show_help(self):
        help_window = tk.Toplevel(self.root)
        help_window.title("Help")
        help_window.geometry("500x400")
        help_window.configure(bg="#e0f7fa")

        # Set the icon for the help window
        help_window.iconphoto(False, self.icon_img)

        # Maximize the window
        help_window.state('zoomed')

        help_text = (
            "Sorting Algorithm Visualizer Help\n\n"
            "1. Select a sorting algorithm (Merge Sort, Counting Sort, or Bucket Sort) by clicking the corresponding button.\n"
            "2. Choose the type of array to visualize: Random Array or Custom Array.\n"
            "   - Random Array: Generates a random array for visualization.\n"
            "   - Custom Array: Allows you to input a custom array for visualization.\n"
            "3. Follow the on-screen instructions to see the visualization of the chosen sorting algorithm.\n"
            "4. To change the speed of the visualizer use 1 - Fast, 2 - Medium and    3 - Slow.\n"
            "5. To pause the visualizer press 'p' on your keyboard, and to resume press 'r'.\n"
            "6. You can go back to the main menu at any time by using the provided 'Back' button."
        )

        label = tk.Label(help_window, text=help_text, font=("Helvetica", 14), bg="#e0f7fa", fg="#00796b",
                         justify="left", wraplength=600)
        label.pack(pady=30, padx=30)

        btn_close = tk.Button(help_window, text="Back", command=help_window.destroy, font=("Helvetica", 14),
                              bg="#00796b", fg="white", activebackground="#004d40", activeforeground="white", width=10,
                              height=2, bd=0, highlightthickness=0)
        btn_close.pack(pady=30)

        # Center the label and button
        help_window.bind('<Configure>', lambda event: self.on_resize_help_window(label, btn_close))

    def on_resize_help_window(self, label, btn_close):
        label.place(relx=0.5, rely=0.4, anchor=tk.CENTER)
        btn_close.place(relx=0.5, rely=0.8, anchor=tk.CENTER)


def main():
    root = tk.Tk()
    app = SortingVisualizerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
