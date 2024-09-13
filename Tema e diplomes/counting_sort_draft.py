import tkinter as tk
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Button

class CountingSortVisualizer:
    def __init__(self, array_type="random", on_back_callback=None):
        self.on_back_callback = on_back_callback
        self.paused = False
        self.sorted = False
        self.fig, self.ax = plt.subplots()
        self.fig.canvas.manager.window.state('zoomed')  # Maximize window
        self.text = self.fig.text(0.02, 0.02, "", fontsize=10, color="black")
        self.interval = 1.0  # Default execution speed

        # Initialize buttons
        self.init_buttons()

        if array_type == "random":
            self.original_array = np.random.randint(1, 20, np.random.randint(5, 10))  # Random array for visualization
            self.arr = self.original_array.copy()
            self.init_visualization()
        elif array_type == "custom":
            self.arr = []
            self.get_custom_array()
        else:
            raise ValueError("Invalid array type. Choose 'random' or 'custom'.")

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
        if self.sorted:
            colors = ['#4CAF50'] * len(self.arr)  # Green color for sorted state
        else:
            colors = ['skyblue'] * len(self.arr)  # Default blue for initial state
        self.bars = self.ax.bar(range(len(self.arr)), self.arr, color=colors, align='center')
        for bar in self.bars:
            height = bar.get_height()
            self.ax.text(bar.get_x() + bar.get_width() / 2., height + 0.1, '%d' % int(height), ha='center', va='bottom',
                         fontsize=8, color='black')
        plt.xticks(range(len(self.arr)), [str(x) for x in self.arr])
        plt.ylim(0, max(self.arr) + 3)  # Adjust y-axis limit dynamically
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
            self.update_speed_message(f"Resumed. Current speed: {['Slow', 'Medium', 'Fast'][self.speed_choice - 1]}")

    def update_speed_message(self, message):
        self.speed_instructions.set_text(message)

    def counting_sort(self):
        max_val = max(self.arr)
        min_val = min(self.arr)
        range_val = max_val - min_val + 1

        count = [0] * range_val
        output = [0] * len(self.arr)

        self.visualize(phase="Starting Counting Sort")

        # Count frequencies of each element
        for num in self.arr:
            count[num - min_val] += 1
            self.visualize(count=count, phase="Count Array")
            self.wait_if_paused()

        # Indicate transition to cumulative count
        self.ax.set_title('Transition to Cumulative Count')
        self.fig.canvas.draw()
        plt.pause(self.interval)

        # Calculate cumulative counts
        for i in range(1, len(count)):
            count[i] += count[i - 1]
            self.visualize(count=count, phase="Cumulative Array")
            self.wait_if_paused()

        # Display cumulative count array before placing elements
        self.ax.set_title('Cumulative Count Array')
        self.fig.canvas.draw()
        plt.pause(self.interval)

        # Place the elements in sorted order
        for num in reversed(self.arr):
            output[count[num - min_val] - 1] = num
            count[num - min_val] -= 1
            self.visualize(output=output, phase=f"Placing {num} at index {count[num - min_val]}")
            self.wait_if_paused()

        # Copy the sorted elements back to the original array
        for i in range(len(self.arr)):
            self.arr[i] = output[i]
            self.visualize(output=output, phase="Final Sorting")
            self.wait_if_paused()

        self.sorted = True
        self.visualize(phase="Sorted Array")  # Update to show final sorted state

    def wait_if_paused(self):
        while self.paused:
            plt.pause(0.1)

    def visualize(self, count=None, output=None, phase="Initial Array"):
        self.plot_bars()

        if count is not None:
            colors = ['gold'] * len(self.arr)  # Yellow for counting phase
            for i in range(len(self.arr)):
                if output is not None and self.arr[i] != output[i]:
                    colors[i] = 'lightgreen'  # Green for placement phase
        else:
            colors = ['skyblue'] * len(self.arr)
            if self.sorted:
                colors = ['lightgreen'] * len(self.arr)

        for bar, color in zip(self.bars, colors):
            bar.set_color(color)

        if count is not None:
            self.ax.set_title(f'{phase}: {count}')
        else:
            self.ax.set_title(phase)
        self.text.set_text(f'Current Array: {self.arr}')
        self.fig.canvas.draw()
        plt.pause(self.interval)

    def run_algorithm(self):
        plt.waitforbuttonpress()

        self.counting_sort()

        self.ax.set_title('Sorted Array')
        self.text.set_text(f'Sorted Array: {self.arr}')
        self.fig.canvas.draw()

        plt.show()

    def on_back_clicked(self, event):
        plt.close(self.fig)
        if self.on_back_callback:
            self.on_back_callback()

    def on_restart_clicked(self, event):
        self.arr = self.original_array.copy()
        self.sorted = False
        self.ax.clear()
        self.fig.texts.clear()  # Clear all existing text from the figure
        self.init_visualization()  # Restart the visualization with the same array

    def init_buttons(self):
        # Initialize "Restart" button
        restart_button_ax = self.fig.add_axes([0.4, 0.001, 0.1, 0.06])  # Adjusted position and size
        self.restart_button = Button(restart_button_ax, 'Restart', color='#4CAF50', hovercolor='lightgreen')
        self.restart_button.on_clicked(self.on_restart_clicked)

        # Initialize "Back to Main" button
        back_button_ax = self.fig.add_axes([0.52, 0.001, 0.1, 0.06])  # Adjusted position and size
        self.back_button = Button(back_button_ax, 'Back to Main Menu', color='#4CAF50', hovercolor='lightgreen')
        self.back_button.on_clicked(self.on_back_clicked)

    def get_custom_array(self):
        self.root = tk.Tk()
        self.root.title("Enter Custom Array")
        self.root.configure(bg="#e0f7fa")

        self.center_window(self.root, 400, 200)

        label = tk.Label(self.root, text="Enter the number of elements:", font=("Helvetica", 14), bg="#e0f7fa", fg="#00796b")
        label.pack(pady=(20, 10))

        self.array_length_entry = tk.Entry(self.root, font=("Helvetica", 14), justify='center')
        self.array_length_entry.pack(pady=(0, 20))

        submit_button = tk.Button(self.root, text="Submit", command=self.submit_length, font=("Helvetica", 14), bg="#00796b", fg="white", activebackground="#004d40", activeforeground="white", width=10, height=1, bd=0, highlightthickness=0)
        submit_button.pack(pady=(0, 20))

        self.root.mainloop()

    def submit_length(self):
        self.array_length = int(self.array_length_entry.get())
        self.arr = [0] * self.array_length  # Initialize the array with zeros
        self.original_array = self.arr.copy()

        self.root.destroy()
        self.input_elements()

    def input_elements(self):
        self.root = tk.Tk()
        self.root.title("Enter Array Elements")
        self.root.configure(bg="#e0f7fa")

        self.element_index = 0
        self.center_window(self.root, 400, 200)

        self.label = tk.Label(self.root, text=f"Enter element {self.element_index + 1}:", font=("Helvetica", 14), bg="#e0f7fa", fg="#00796b")
        self.label.pack(pady=(20, 10))

        self.element_entry = tk.Entry(self.root, font=("Helvetica", 14), justify='center')
        self.element_entry.pack(pady=(0, 20))

        self.submit_button = tk.Button(self.root, text="Submit", command=self.submit_element, font=("Helvetica", 14), bg="#00796b", fg="white", activebackground="#004d40", activeforeground="white", width=10, height=1, bd=0, highlightthickness=0)
        self.submit_button.pack(pady=(0, 20))

        self.root.mainloop()

    def submit_element(self):
        self.arr[self.element_index] = int(self.element_entry.get())
        self.element_index += 1

        if self.element_index < self.array_length:
            self.label.config(text=f"Enter element {self.element_index + 1}:")
            self.element_entry.delete(0, tk.END)
        else:
            self.root.destroy()
            self.init_visualization()

    def center_window(self, root, width, height):
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        x_coordinate = (screen_width / 2) - (width / 2)
        y_coordinate = (screen_height / 2) - (height / 2)

        root.geometry(f"{width}x{height}+{int(x_coordinate)}+{int(y_coordinate)}")

def main():
    root = tk.Tk()
    root.title("Choose Array Type")
    root.configure(bg="#e0f7fa")

    def on_random():
        root.destroy()
        CountingSortVisualizer(array_type="random")

    def on_custom():
        root.destroy()
        CountingSortVisualizer(array_type="custom")

    label = tk.Label(root, text="Choose array type:", font=("Helvetica", 14), bg="#e0f7fa", fg="#00796b")
    label.pack(pady=(20, 10))

    random_button = tk.Button(root, text="Random Array", command=on_random, font=("Helvetica", 14), bg="#00796b", fg="white", activebackground="#004d40", activeforeground="white", width=15, height=2, bd=0, highlightthickness=0)
    random_button.pack(pady=(10, 10))

    custom_button = tk.Button(root, text="Custom Array", command=on_custom, font=("Helvetica", 14), bg="#00796b", fg="white", activebackground="#004d40", activeforeground="white", width=15, height=2, bd=0, highlightthickness=0)
    custom_button.pack(pady=(10, 10))

    root.mainloop()

if __name__ == "__main__":
    main()
