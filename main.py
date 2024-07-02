import tkinter as tk
from merge_sort_draft import MergeSortVisualizer
from counting_sort_draft import CountingSortVisualizer
from bucket_sort_draft import BucketSortVisualizer

class SortingVisualizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sorting Algorithm Visualizer")
        self.root.geometry("400x300")
        self.root.configure(bg="#ffffff")

        self.container = tk.Frame(root, bg="#ffffff")
        self.container.pack(expand=True)

        label = tk.Label(self.container, text="Select a Sorting Algorithm to Visualize", font=("Helvetica", 16, "bold"),
                         bg="#ffffff")
        label.pack(pady=20)

        btn_merge_sort = tk.Button(self.container, text="Merge Sort", command=self.run_merge_sort, width=20, height=2,
                                   font=("Helvetica", 12), bg="#4CAF50", fg="white", padx=10, pady=5)
        btn_merge_sort.pack(pady=10)

        btn_counting_sort = tk.Button(self.container, text="Counting Sort", command=self.run_counting_sort, width=20,
                                      height=2, font=("Helvetica", 12), bg="#2196F3", fg="white", padx=10, pady=5)
        btn_counting_sort.pack(pady=10)

        btn_bucket_sort = tk.Button(self.container, text="Bucket Sort", command=self.run_bucket_sort, width=20,
                                    height=2, font=("Helvetica", 12), bg="#FF9800", fg="white", padx=10, pady=5)
        btn_bucket_sort.pack(pady=10)

        root.bind('<Configure>', self.on_resize)

    def on_resize(self, event):
        # Center the container when the window is resized
        self.container.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    def run_merge_sort(self):
        self.hide_main_window()
        MergeSortVisualizer(on_back_callback=self.show_main_window)

    def run_counting_sort(self):
        self.hide_main_window()
        CountingSortVisualizer(on_back_callback=self.show_main_window)

    def run_bucket_sort(self):
        self.hide_main_window()
        BucketSortVisualizer(on_back_callback=self.show_main_window)

    def hide_main_window(self):
        self.root.withdraw()

    def show_main_window(self):
        self.root.deiconify()

def main():
    root = tk.Tk()
    app = SortingVisualizerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
