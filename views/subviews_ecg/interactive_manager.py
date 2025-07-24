import numpy as np
import matplotlib.pyplot as plt


class InteractiveManager:
    def __init__(self, ax):
        self.ax = ax
        self.fig = ax.figure
        self.initial_xlim = ax.get_xlim()
        self.initial_ylim = ax.get_ylim()
        self.initial_center = (
            (self.initial_xlim[0] + self.initial_xlim[1]) / 2,
            (self.initial_ylim[0] + self.initial_ylim[1]) / 2
        )
        self.pan_start = None
        self._connect_events()

    def _connect_events(self):
        self.fig.canvas.mpl_connect('scroll_event', self._on_scroll)
        self.fig.canvas.mpl_connect('button_press_event', self._on_press)
        self.fig.canvas.mpl_connect('button_release_event', self._on_release)
        self.fig.canvas.mpl_connect('motion_notify_event', self._on_motion)
        self.fig.canvas.mpl_connect('button_press_event', self._on_right_click)

    def _on_scroll(self, event):
        if event.inaxes != self.ax:
            return

        base_scale = 1.2
        cur_xlim = self.ax.get_xlim()
        cur_ylim = self.ax.get_ylim()
        xdata, ydata = event.xdata, event.ydata

        if event.button == 'up':
            scale_factor = 1 / base_scale
        elif event.button == 'down':
            scale_factor = base_scale
        else:
            return

        new_width = (cur_xlim[1] - cur_xlim[0]) * scale_factor
        new_height = (cur_ylim[1] - cur_ylim[0]) * scale_factor

        self.ax.set_xlim([xdata - new_width / 2, xdata + new_width / 2])
        self.ax.set_ylim([ydata - new_height / 2, ydata + new_height / 2])
        self.fig.canvas.draw()

    def _on_press(self, event):
        if event.inaxes != self.ax or event.button != 1:
            return
        self.pan_start = (event.xdata, event.ydata)

    def _on_motion(self, event):
        if self.pan_start is None or event.inaxes != self.ax:
            return

        dx = event.xdata - self.pan_start[0]
        dy = event.ydata - self.pan_start[1]

        self.ax.set_xlim([x - dx for x in self.ax.get_xlim()])
        self.ax.set_ylim([y - dy for y in self.ax.get_ylim()])
        self.fig.canvas.draw()

    def _on_release(self, event):
        self.pan_start = None

    def _reset_view(self):
        width = self.initial_xlim[1] - self.initial_xlim[0]
        height = self.initial_ylim[1] - self.initial_ylim[0]

        self.ax.set_xlim([
            self.initial_center[0] - width / 2,
            self.initial_center[0] + width / 2
        ])
        self.ax.set_ylim([
            self.initial_center[1] - height / 2,
            self.initial_center[1] + height / 2
        ])
        self.fig.canvas.draw()

    def _on_right_click(self, event):
        if event.inaxes != self.ax or event.button != 3:
            return
        self._reset_view()


