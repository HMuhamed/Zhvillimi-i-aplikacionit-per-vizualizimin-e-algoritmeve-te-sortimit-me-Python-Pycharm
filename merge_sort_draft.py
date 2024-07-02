import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Button

class MergeSortVisualizer:
    def __init__(self, on_back_callback=None):
        self.arr = np.random.randint(1, 100, 10)
        self.interval = 1.0  # Default execution speed
        self.paused = False  # Flag to track pause/resume
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
        self.speed_choice = 2  # Default speed (medium)

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

        colors = ['blue'] * len(self.arr)
        if l is not None and r is not None:
            if merged:
                for i in range(l, r + 1):
                    colors[i] = 'green'  # Highlighting the merged range in green
            elif show_yellow:
                for i in range(l, r + 1):
                    colors[i] = 'yellow'  # Highlighting the range in yellow before merging
            else:
                for i in range(l, r + 1):
                    colors[i] = 'blue'  # Default color if not merged or showing yellow

        for bar, color in zip(self.bars, colors):
            bar.set_color(color)

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

        # Add "Back to Main" button
        back_button_ax = self.fig.add_axes([0.45, 0.01, 0.1, 0.06])  # Match padding from other visualizations
        back_button = Button(back_button_ax, 'Back to Main Menu', color='#4CAF50', hovercolor='lightgreen')
        back_button.on_clicked(self.on_back_clicked)

        plt.show()

    def on_back_clicked(self, event):
        plt.close(self.fig)
        if self.on_back_callback:
            self.on_back_callback()

def main(on_back_callback=None):
    visualizer = MergeSortVisualizer(on_back_callback=on_back_callback)

if __name__ == "__main__":
    main()
