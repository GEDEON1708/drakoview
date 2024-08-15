'''
KITTI utilities.
TK Widgets for graphical interfaces.

Author: Bruno Silva
brunomfs@gmail.com
'''

from abc import ABC, abstractmethod

import tkinter as tk
from PIL import Image, ImageTk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from groundtruth_loader import GroundTruthLoader
from trajectory_viewer import TrajectoryViewer
from lidar_loader import LIDARLoader
from point_cloud_viewer import PointCloudViewer

class ImageWidget(tk.Label):
    '''
    Image widget for TK GUI.
    '''

    def __init__(self, master=None, scale=0.5, delta=33, cnf={}, **kwargs):
        super().__init__(master, cnf, **kwargs)
        self._pil_img = None #for resize
        self._tk_img = None #a reference must be kept in memory
        self._img_files = [] #animate with images from this list
        self._scale = scale

    def set_image(self, img_file):
        '''
        Sets an image from the
        supplied file path.
        '''

        self._pil_img = Image.open(img_file)
        self._tk_img = ImageTk.PhotoImage(self._pil_img)
        self.rescale(self._scale)
        self.configure(image=self._tk_img)

    def rescale(self, scale):
        '''
        Scales the image uniformily
        by multiplying it by the
        provided scale factor.
        '''

        if self._pil_img:
            new_size = (int(scale*self._pil_img.size[0]), int(scale*self._pil_img.size[1]))
            self._pil_img = self._pil_img.resize(new_size)
            self._tk_img = ImageTk.PhotoImage(self._pil_img)
            self.configure(image=self._tk_img)

    def configure_animation(self, img_files):
        '''
        Configures an animation from a
        supplied list of image file names.
        '''
        self._img_files = img_files.copy()
        self.set_image(self._img_files[0])

    def animate(self, idx):
        '''
        Animates: changes from img
        to img in the _image_file list
        at each call.
        Index is an integer with the timestep.
        '''
        if idx < len(self._img_files):
            img_file = self._img_files.pop(idx)
            self.set_image(img_file)

class PlotWidget(ABC):
    '''
    Abstract base class for a plot
    widget (TK GUI).
    '''

    @abstractmethod
    def __init__(self, master):
        self.master = master
        self.viewer = None
        self.figure_canvas = None
    
    @abstractmethod
    def _init_canvas(self):
        if self.viewer:
            self.figure_canvas = FigureCanvasTkAgg(self.viewer.fig, self.master)
        else:
            raise AttributeError('A viewer and figure_canvas attributes are necessary for this object.')

    def widget(self):
        if self.figure_canvas:
            return self.figure_canvas.get_tk_widget()
        else:
            raise AttributeError('A viewer and figure_canvas attributes are necessary for this object.')

class TrajectoryWidget(PlotWidget):
    '''
    Trajectory plot widget for TK GUI.
    '''

    def __init__(self, master, delta=33):
        PlotWidget.__init__(self, master)
        self._init_canvas()
        self._positions = None

    def _init_canvas(self):
        self.viewer = TrajectoryViewer()
        PlotWidget._init_canvas(self)

    def add_position(self, pos):
        '''
        Adds a position
        to the plot.
        '''
        self.viewer.add_position(pos)

    def configure_animation(self, positions):
        '''
        Configures the animation of the widget.
        positions is a Nx3 numpy.array.
        '''
        self._positions = positions.copy()

    def animate(self, idx):
        '''
        Animates: adds the positions
        in the _positions array to the plot
        at each call.
        idx is an integer with the timestep.
        '''
        if idx < len(self._positions):
            pos = self._positions[idx]
            self.add_position(pos)

class PointCloudWidget(PlotWidget):
    '''
    Point cloud  widget for TK GUI.
    '''

    def __init__(self, master):
        PlotWidget.__init__(self, master)
        self._init_canvas()
        self._scans = None

    def _init_canvas(self):
        self.viewer = PointCloudViewer()
        PlotWidget._init_canvas(self)

    def add_cloud(self, cloud):
        '''
        Adds a cloud
        to the plot.
        '''
        self.viewer.add_cloud(cloud)

    def configure_animation(self, scans):
        '''
        Configures the animation of the widget.
        scans is a Nx3 numpy.array.
        '''
        self._scans = scans.copy()

    def animate(self, idx):
        '''
        Animates: adds the scans
        in the _scans array to the plot
        at each call.
        idx is an integer with the timestep.
        '''
        if idx < len(self._scans):
            scan = self._scans[idx]
            self.add_cloud(scan)

def img_animation_callback(widget, idx, lim):
    if idx < lim:
        widget.animate(idx)
        idx += 1
        widget.after(500, lambda: img_animation_callback(widget, idx, lim))

def plot_animation_callback(widget, idx, lim):
    if idx < lim:
        widget.animate(idx)
        idx += 1
        widget.widget().after(33, lambda: plot_animation_callback(widget, idx, lim))

def main():

    root = tk.Tk()
    root.title('Widget Test')

    # -> animate image
    idx = 0
    img_widget = ImageWidget(root, delta=1000)
    img_files = ['../sequences/03/image_0/000000.png',
                 '../sequences/03/image_0/000001.png',
                 '../sequences/03/image_0/000002.png',
                 '../sequences/03/image_0/000003.png',
                 '../sequences/03/image_0/000004.png']
    img_widget.configure_animation(img_files)
    img_widget.after(500, lambda: img_animation_callback(img_widget, idx, len(img_files)))
    img_widget.pack()

    # -> animate plot: trajectory (same for point cloud plot)
    # idx = 0
    # plot = TrajectoryWidget(root)
    # plot.widget().pack()

    # gt_loader = GroundTruthLoader('../sequences/03/03.txt')
    # positions = gt_loader.get_all_positions()
    # plot.configure_animation(positions)
    # plot.widget().after(33, lambda: plot_animation_callback(plot, idx, len(positions)))

    root.mainloop()

if __name__ == '__main__':
    main()


def widgets_tk():
    return None


# widgets_tk.py
import tkinter as tk  # Certifique-se de que tkinter está importado

def create_label(root, text):
    label = tk.Label(root, text=text)
    label.pack()  # Você pode usar outras opções se necessário
    return label
