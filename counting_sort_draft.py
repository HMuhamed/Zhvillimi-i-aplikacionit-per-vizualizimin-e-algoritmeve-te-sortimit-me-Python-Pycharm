import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Button

class CountingSortVisualizer:
    def __init__(self, on_back_callback=None):
        self.arr = np.random.randint(1, 30, 7)  # Random array for visualization
        self.interval = 1.0  # Default execution speed
        self.paused = False  # Flag to track pause/resume
        self.sorted = False  # Flag to track if array is sorted
        self.fig, self.ax = plt.subplots()
        self.text = self.fig.text(0.02, 0.02, "", fontsize=10, color="black")
        self.on_back_callback = on_back_callback

        self.ax.set_title('Initial Array')
        self.plot_bars()

        # Add speed selection instructions to the plot
        self.speed_instructions = self.fig.text(0.5, 0.95,
            "Press 1 for Slow speed\nPress 2 for Medium speed\nPress 3 for Fast speed",
            ha='center', va='center', fontsize=10, color='blue')

        # Connect events for speed selection and pause/resume
        self.fig.canvas.mpl_connect('key_press_event', self.on_key_press)
        self.speed_choice = "Medium"  # Default speed (medium)

        self.run_algorithm()

    def plot_bars(self):
        self.ax.clear()
        if self.sorted:
            colors = ['green'] * len(self.arr)
        else:
            colors = ['blue'] * len(self.arr)
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
            self.speed_choice = "Slow"
            self.interval = 2.0
            self.update_speed_message("Speed set to: Slow")
        elif event.key == '2':
            self.speed_choice = "Medium"
            self.interval = 1.0
            self.update_speed_message("Speed set to: Medium")
        elif event.key == '3':
            self.speed_choice = "Fast"
            self.interval = 0.5
            self.update_speed_message("Speed set to: Fast")
        elif event.key == 'p':  # Change stop key to 'p' (pause)
            self.paused = True
            self.update_speed_message("Paused. Press 'r' to resume.")
        elif event.key == 'r':
            self.paused = False
            self.update_speed_message(f"Resumed. Current speed: {self.speed_choice}")

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
            if self.paused:
                while self.paused:
                    plt.pause(0.1)

        # Indicate transition to cumulative count
        self.ax.set_title('Transition to Cumulative Count')
        self.fig.canvas.draw()
        plt.pause(self.interval)

        # Calculate cumulative counts
        for i in range(1, len(count)):
            count[i] += count[i - 1]
            self.visualize(count=count, phase="Cumulative Array")
            if self.paused:
                while self.paused:
                    plt.pause(0.1)

        # Display cumulative count array before placing elements
        self.ax.set_title('Cumulative Count Array')
        self.fig.canvas.draw()
        plt.pause(self.interval)

        # Place the elements in sorted order
        for num in reversed(self.arr):
            output[count[num - min_val] - 1] = num
            count[num - min_val] -= 1
            self.visualize(output=output, phase=f"Placing {num} at index {count[num - min_val]}")
            if self.paused:
                while self.paused:
                    plt.pause(0.1)

        # Copy the sorted elements back to the original array
        for i in range(len(self.arr)):
            self.arr[i] = output[i]
            self.visualize(output=output, phase="Final Sorting")
            if self.paused:
                while self.paused:
                    plt.pause(0.1)

        self.sorted = True
        self.visualize(phase="Sorted Array")  # Update to show final sorted state

    def visualize(self, count=None, output=None, phase="Initial Array"):
        self.plot_bars()

        if count is not None:
            colors = ['yellow'] * len(self.arr)
            for i in range(len(self.arr)):
                if output is not None and self.arr[i] != output[i]:
                    colors[i] = 'green'
        else:
            colors = ['blue'] * len(self.arr)
            if self.sorted:
                colors = ['green'] * len(self.arr)

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

        # Add "Back to Main" button
        back_button_ax = self.fig.add_axes([0.45, 0.01, 0.1, 0.06])  # Match padding from bucket sort
        back_button = Button(back_button_ax, 'Back to Main Menu', color='#4CAF50', hovercolor='lightgreen')
        back_button.on_clicked(self.on_back_clicked)

        plt.show()

    def on_back_clicked(self, event):
        plt.close(self.fig)
        if self.on_back_callback:
            self.on_back_callback()

def main(on_back_callback=None):
    visualizer = CountingSortVisualizer(on_back_callback=on_back_callback)

if __name__ == "__main__":
    main()
