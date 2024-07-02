import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Button

class BucketSortVisualizer:
    def __init__(self, on_back_callback=None):
        self.arr = np.random.randint(1, 100, 10).tolist()  # Initial array with 5 elements
        self.interval = 1.0  # Default execution speed
        self.paused = False  # Flag to track pause/resume
        self.fig, self.ax = plt.subplots()
        self.text = self.fig.text(0.02, 0.02, "", fontsize=10, color="black")

        self.ax.set_title('Initial Array')
        self.plot_bars()

        # Add speed selection instructions to the plot
        self.speed_instructions = self.fig.text(0.5, 0.95,
                                                "Press 1 for Slow speed\nPress 2 for Medium speed\nPress 3 for Fast speed",
                                                ha='center', va='center', fontsize=10, color='blue')

        # Connect events for speed selection and pause/resume
        self.fig.canvas.mpl_connect('key_press_event', self.on_key_press)
        self.speed_choice = 2  # Default speed (medium)

        # Callback for returning to the main screen
        self.on_back_callback = on_back_callback

        self.run_algorithm()

    def plot_bars(self):
        self.ax.clear()
        self.bars = self.ax.bar(range(len(self.arr)), self.arr, color='blue', align='center')
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
            self.update_speed_message(f"Resumed. Current speed: {['Slow', 'Medium', 'Fast'][self.speed_choice - 1]}")

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
        self.bars = self.ax.bar(range(len(flattened)), flattened, color='blue', align='center')

        # Highlight the current bucket being processed
        colors = ['blue'] * len(flattened)
        if filling:
            start = sum(len(buckets[i]) for i in range(idx))
            end = start + len(buckets[idx])
            for i in range(start, end):
                colors[i] = 'yellow'
        elif sorting:
            start = sum(len(buckets[i]) for i in range(idx))
            end = start + len(buckets[idx])
            for i in range(start, end):
                colors[i] = 'green'
        elif merging:
            colors = ['green'] * len(flattened)

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

        self.text.set_text(f'Current Array: {flattened}')
        self.fig.canvas.draw()
        plt.pause(self.interval)

    def run_algorithm(self):
        plt.waitforbuttonpress()

        self.bucket_sort()

        self.ax.set_title('Sorted Array')
        self.text.set_text(f'Sorted Array: {self.arr}')
        self.fig.canvas.draw()

        # Add "Back to Main" button
        back_button_ax = self.fig.add_axes([0.45, 0.01, 0.1, 0.06])  # Center the button
        back_button = Button(back_button_ax, 'Back to Main Menu', color='#4CAF50', hovercolor='lightgreen')
        back_button.on_clicked(self.on_back_clicked)

        plt.show()

    def on_back_clicked(self, event):
        plt.close(self.fig)
        if self.on_back_callback:
            self.on_back_callback()

def main(on_back_callback=None):
    visualizer = BucketSortVisualizer(on_back_callback=on_back_callback)

if __name__ == "__main__":
    main()
