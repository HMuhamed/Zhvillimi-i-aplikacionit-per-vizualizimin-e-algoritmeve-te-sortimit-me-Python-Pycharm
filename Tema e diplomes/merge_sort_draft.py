import tkinter as tk
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Button

class MergeSortVisualizer:
    def __init__(self, array_type="random", on_back_callback=None):
        self.on_back_callback = on_back_callback
        self.paused = False
        self.fig, self.ax = plt.subplots()
        self.fig.canvas.manager.window.state('zoomed')  # Maximize window
        self.text = self.fig.text(0.02, 0.02, "", fontsize=10, color="black")
        self.interval = 1.0  # Default execution speed

        if array_type == "random":
            self.original_array = np.random.randint(1, 100, np.random.randint(5, 10))
            self.arr = self.original_array.copy()
            self.init_visualization()
        elif array_type == "custom":
            self.arr = []
            self.get_custom_array()

    def init_visualization(self):
        self.ax.clear()  # Clear previous plot elements
        self.ax.set_title('Initial Array')
        self.plot_bars()

        # Add speed selection instructions to the plot
        self.speed_instructions = self.fig.text(0.5, 0.95,
                                                "Press 1 for Slow speed\nPress 2 for Medium speed\nPress 3 for Fast speed",
                                                ha='center', va='center', fontsize=10, color='blue')

        # Connect events for speed selection and pause/resume
        self.fig.canvas.mpl_connect('key_press_event', self.on_key_press)
        self.speed_choice = 2  # Default speed (medium)

        # Add "Restart" button
        restart_button_ax = self.fig.add_axes([0.4, 0.001, 0.1, 0.06])  # Adjusted position and size
        self.restart_button = Button(restart_button_ax, 'Restart', color='#4CAF50', hovercolor='lightgreen')
        self.restart_button.on_clicked(self.on_restart_clicked)

        # Add "Back to Main Menu" button
        back_button_ax = self.fig.add_axes([0.52, 0.001, 0.1, 0.06])  # Adjusted position and size
        self.back_button = Button(back_button_ax, 'Back to Main Menu', color='#4CAF50', hovercolor='lightgreen')
        self.back_button.on_clicked(self.on_back_clicked)

        self.run_algorithm()

    def plot_bars(self):
        self.ax.clear()
        self.bars = self.ax.bar(range(len(self.arr)), self.arr, color='skyblue', align='center')  # Changed color to skyblue
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

    def merge(self, l, m, r):
        L = self.arr[l:m + 1].copy()
        R = self.arr[m + 1:r + 1].copy()

        i = j = 0
        k = l

        # Visualize L and R in yellow before merging
        self.visualize(l, m, show_yellow=True)
        self.visualize(m + 1, r, show_yellow=True)

        while i < len(L) and j < len(R):
            if L[i] <= R[j]:
                self.arr[k] = L[i]
                i += 1
            else:
                self.arr[k] = R[j]
                j += 1
            k += 1

            # Check for pause and resume
            if self.paused:
                while self.paused:
                    plt.pause(0.1)

        while i < len(L):
            self.arr[k] = L[i]
            i += 1
            k += 1

            # Check for pause and resume
            if self.paused:
                while self.paused:
                    plt.pause(0.1)

        while j < len(R):
            self.arr[k] = R[j]
            j += 1
            k += 1

            # Check for pause and resume
            if self.paused:
                while self.paused:
                    plt.pause(0.1)

        # Visualize the merged section in green
        self.visualize(l, r, merged=True)

    def merge_sort(self, l, r):
        if l < r:
            m = (l + r) // 2

            self.merge_sort(l, m)
            self.merge_sort(m + 1, r)
            self.merge(l, m, r)

    def visualize(self, l=None, r=None, merged=False, show_yellow=False):
        self.plot_bars()

        colors = ['skyblue'] * len(self.arr)  # Adjusted to use skyblue color
        if l is not None and r is not None:
            if merged:
                for i in range(l, r + 1):
                    colors[i] = 'lightgreen'  # Highlighting the merged range in lightgreen
            elif show_yellow:
                for i in range(l, r + 1):
                    colors[i] = 'gold'  # Highlighting the range in gold before merging
            else:
                for i in range(l, r + 1):
                    colors[i] = 'skyblue'  # Default color if not merged or showing yellow

        for bar, color in zip(self.bars, colors):
            bar.set_color(color)

        self.ax.set_title('')  # Clear previous title
        self.text.set_text('')  # Clear previous text
        self.speed_instructions.set_text('')  # Clear speed selection instructions
        if l is not None and r is not None:
            if merged:
                self.ax.set_title(f'Merged subarrays: {self.arr[l:r + 1]}')
            else:
                self.ax.set_title(f'Merging subarrays: {self.arr[l:r + 1]}')
        else:
            self.ax.set_title('Initial Array')
        self.text.set_text(f'Current Array: {self.arr}')
        self.fig.canvas.draw()
        plt.pause(self.interval)

    def run_algorithm(self):
        plt.waitforbuttonpress()
        self.merge_sort(0, len(self.arr) - 1)

        self.ax.set_title('Sorted Array')
        self.text.set_text(f'Sorted Array: {self.arr}')
        self.fig.canvas.draw()

        plt.show()

    def on_back_clicked(self, event):
        plt.close(self.fig)
        if self.on_back_callback:
            self.on_back_callback()

    def on_restart_clicked(self, event):
        plt.close(self.fig)
        self.fig, self.ax = plt.subplots()
        self.fig.canvas.manager.window.state('zoomed')  # Maximize window
        self.init_visualization()  # Restart the visualization with the same array

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
        self.original_array = np.random.randint(1, 100, array_length)
        self.arr = self.original_array.copy()

        self.root.destroy()
        self.root = tk.Tk()
        self.root.title("Enter Custom Array Elements")
        self.root.configure(bg="#e0f7fa")

        self.center_window(self.root, 400, 300)

        container = tk.Frame(self.root, bg="#e0f7fa")
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        self.entries = []
        self.current_index = 0

        self.label = tk.Label(container, text=f"Enter element {self.current_index + 1}:", font=("Helvetica", 14), bg="#e0f7fa", fg="#00796b")
        self.label.pack(pady=(10, 10))

        self.entry = tk.Entry(container, font=("Helvetica", 14), justify='center')
        self.entry.pack(pady=(0, 20))  # Centered padding

        submit_button = tk.Button(container, text="Next", command=self.submit_element, font=("Helvetica", 14), bg="#00796b", fg="white", activebackground="#004d40", activeforeground="white", width=10, height=1, bd=0, highlightthickness=0)
        submit_button.pack(pady=(20, 0))

        self.root.mainloop()

    def submit_element(self):
        element_value = self.entry.get().strip()
        if element_value.isdigit():
            self.original_array[self.current_index] = int(element_value)
            self.arr[self.current_index] = int(element_value)
            self.current_index += 1

        if self.current_index < len(self.arr):
            self.label.config(text=f"Enter element {self.current_index + 1}:")
            self.entry.delete(0, tk.END)  # Clear the entry for the next element
        else:
            self.root.destroy()
            self.init_visualization()

    def center_window(self, window, width, height):
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()

        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)

        window.geometry(f'{width}x{height}+{x}+{y}')

if __name__ == "__main__":
    app = MergeSortVisualizer(array_type="custom")
