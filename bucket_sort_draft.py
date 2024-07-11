import tkinter as tk
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Button


class BucketSortVisualizer:
    def __init__(self, array_type="random", on_back_callback=None):
        self.on_back_callback = on_back_callback
        self.paused = False
        self.fig, self.ax = plt.subplots()
        self.fig.canvas.manager.window.state('zoomed')  # Maximize window
        self.text = self.fig.text(0.02, 0.02, "", fontsize=10, color="black")
        self.interval = 1.0  # Default execution speed

        self.create_back_button()  # Always visible back button

        if array_type == "random":
            self.arr = np.random.randint(1, 100, np.random.randint(1, 21))
            self.init_visualization()
        elif array_type == "custom":
            self.arr = []
            self.get_custom_array()

    def create_back_button(self):
        back_button_ax = self.fig.add_axes([0.45, 0.01, 0.1, 0.06])  # Adjusted position
        self.back_button = Button(back_button_ax, 'Back to Main Menu', color='#4CAF50', hovercolor='lightgreen')
        self.back_button.on_clicked(self.on_back_clicked)

    def init_visualization(self):
        self.ax.set_title('Initial Array')
        self.plot_bars()

        # Add speed selection instructions to the plot
        self.speed_instructions = self.fig.text(0.5, 0.95,
                                                "Press 1 for Slow speed\nPress 2 for Medium speed\nPress 3 for Fast speed",
                                                ha='center', va='center', fontsize=10, color='blue')

        # Connect events for speed selection and pause/resume
        self.fig.canvas.mpl_connect('key_press_event', self.on_key_press)
        self.speed_choice = 2  # Default speed (medium)

        self.run_algorithm()

    def plot_bars(self):
        self.ax.clear()
        self.bars = self.ax.bar(range(len(self.arr)), self.arr, color='skyblue',
                                align='center')  # Set initial color to 'skyblue'
        for bar in self.bars:
            height = bar.get_height()
            self.ax.text(bar.get_x() + bar.get_width() / 2., height + 1, '%d' % int(height), ha='center', va='bottom',
                         fontsize=8, color='black')
        plt.xticks(range(len(self.arr)), [str(x) for x in self.arr])
        plt.ylim(0, max(self.arr) + 10)  # Adjust y-axis limit dynamically
        plt.pause(self.interval)

    def on_key_press(self, event):
        if event.key == '1':
            self.speed_choice = 1
            self.interval = 2.0
            self.update_speed_message("Speed set to: Slow")
        elif event.key == '2':
            self.speed_choice = 2
            self.interval = 1.0
            self.update_speed_message("Speed set to: Medium")
        elif event.key == '3':
            self.speed_choice = 3
            self.interval = 0.5
            self.update_speed_message("Speed set to: Fast")
        elif event.key == 'p':  # Change stop key to 'p' (pause)
            self.paused = True
            self.update_speed_message("Paused. Press 'r' to resume.")
        elif event.key == 'r':
            self.paused = False
            self.update_speed_message("Resumed. Current speed: Medium")

    def update_speed_message(self, message):
        self.speed_instructions.set_text(message)

    def bucket_sort(self):
        max_value = max(self.arr)
        num_buckets = 10  # Number of buckets to use

        # Create empty buckets
        buckets = [[] for _ in range(num_buckets)]

        # Distribute elements into buckets
        for num in self.arr:
            index = num // 10  # Each bucket range is 10
            buckets[index].append(num)

            # Visualize each bucket being filled
            self.visualize_bucket(buckets, index, filling=True)
            self.wait_if_paused()

        # Sort each bucket and visualize
        for i in range(num_buckets):
            buckets[i] = sorted(buckets[i])

            # Visualize sorting of each bucket
            self.visualize_bucket(buckets, i, sorting=True)
            self.wait_if_paused()

        # Concatenate buckets and visualize
        result = []
        for bucket in buckets:
            result.extend(bucket)

            # Visualize merging of buckets
            self.visualize_bucket(buckets, idx=None, sorting=False, merging=True)
            self.wait_if_paused()

        self.arr = result

    def wait_if_paused(self):
        while self.paused:
            plt.pause(0.1)

    def visualize_bucket(self, buckets, idx, filling=False, sorting=False, merging=False):
        self.ax.clear()
        flattened = [item for sublist in buckets for item in sublist]
        self.bars = self.ax.bar(range(len(flattened)), flattened, color='skyblue', align='center')

        # Highlight the current bucket being processed
        colors = ['skyblue'] * len(flattened)
        if filling:
            start = sum(len(buckets[i]) for i in range(idx))
            end = start + len(buckets[idx])
            for i in range(start, end):
                colors[i] = 'gold'
        elif sorting:
            start = sum(len(buckets[i]) for i in range(idx))
            end = start + len(buckets[idx])
            for i in range(start, end):
                colors[i] = 'lightgreen'
        elif merging:
            colors = ['lightgreen'] * len(flattened)

        for bar, color in zip(self.bars, colors):
            bar.set_color(color)

        for bar in self.bars:
            height = bar.get_height()
            self.ax.text(bar.get_x() + bar.get_width() / 2., height + 1, '%d' % int(height), ha='center', va='bottom',
                         fontsize=8, color='black')

        plt.ylim(0, max(flattened) + 10)

        if filling:
            self.ax.set_title(f'Filling bucket {idx + 1}')
        elif sorting:
            self.ax.set_title(f'Sorting bucket {idx + 1}')
        elif merging:
            self.ax.set_title('Merging buckets')

        self.text.set_text(f'Current Array: {[int(item) for item in flattened]}')
        self.fig.canvas.draw()
        plt.pause(self.interval)

    def run_algorithm(self):
        plt.waitforbuttonpress()

        self.bucket_sort()

        sorted_array_text = ', '.join(map(str, map(int, self.arr)))
        self.ax.set_title('Sorted Array')
        self.text.set_text(f'Sorted Array: [{sorted_array_text}]')
        self.fig.canvas.draw()

    def on_back_clicked(self, event):
        plt.close(self.fig)
        if self.on_back_callback:
            self.on_back_callback()

    def get_custom_array(self):
        self.root = tk.Tk()
        self.root.title("Enter Custom Array")
        self.root.configure(bg="#e0f7fa")

        self.center_window(self.root, 400, 300)

        container = tk.Frame(self.root, bg="#e0f7fa")
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        label = tk.Label(container, text="Enter the length of the array:", font=("Helvetica", 14), bg="#e0f7fa", fg="#00796b")
        label.pack(pady=(10, 10))

        self.array_length_entry = tk.Entry(container, font=("Helvetica", 14), justify='center')
        self.array_length_entry.pack(pady=(0, 20))

        submit_button = tk.Button(container, text="Submit", command=self.submit_length, font=("Helvetica", 14), bg="#00796b", fg="white", activebackground="#004d40", activeforeground="white", width=10, height=1, bd=0, highlightthickness=0)
        submit_button.pack(pady=(0, 20))

        self.root.mainloop()

    def submit_length(self):
        array_length = int(self.array_length_entry.get())
        self.arr = []

        self.root.destroy()
        self.root = tk.Tk()
        self.root.title("Enter Custom Array Elements")
        self.root.configure(bg="#e0f7fa")

        self.center_window(self.root, 400, 300)

        container = tk.Frame(self.root, bg="#e0f7fa")
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        label = tk.Label(container, text="Enter the elements of the array:", font=("Helvetica", 14), bg="#e0f7fa", fg="#00796b")
        label.pack(pady=(10, 10))

        self.entries = []
        for i in range(array_length):
            entry = tk.Entry(container, font=("Helvetica", 14), justify='center')
            entry.pack(pady=(0, 10))
            self.entries.append(entry)

        submit_button = tk.Button(container, text="Submit", command=self.submit_elements, font=("Helvetica", 14), bg="#00796b", fg="white", activebackground="#004d40", activeforeground="white", width=10, height=1, bd=0, highlightthickness=0)
        submit_button.pack(pady=(0, 20))

        self.root.mainloop()

    def submit_elements(self):
        self.arr = [int(entry.get()) for entry in self.entries]
        self.root.destroy()
        self.init_visualization()

    def center_window(self, root, width, height):
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        root.geometry(f"{width}x{height}+{x}+{y}")


def main(on_back_callback=None):
    visualizer = BucketSortVisualizer(on_back_callback=on_back_callback)


if __name__ == "__main__":
    main()
