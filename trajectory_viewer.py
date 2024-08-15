'''
KITTI utilities.
Trajectory viewer.

Author: Bruno Silva
brunomfs@gmail.com
'''

import numpy as np
import matplotlib.pyplot as plt

from groundtruth_loader import GroundTruthLoader

class TrajectoryViewer:
    '''
    Visualizer for the trajectories
    generated when processing the
    KITTI datasets.
    '''

    def __init__(self):
        #plt.ion()
        self.fig = None
        self.ax = None
        self._line = None
        self._x = []
        self._z = []
        self._tip = None
        self._initialize()
    
    def _initialize(self):
        self.fig = plt.figure(figsize=(2,2))
        self.ax = self.fig.add_subplot(111)
        self._line, = self.ax.plot(self._x, self._z, 'r-')

        self.ax.set_title('Pos.')
        self.ax.set_xlabel('x')
        self.ax.set_ylabel('z')

    def add_position(self, pos):
        '''
        Adds a position (1x3 numpy.array)
        to the plot.
        '''
        
        self._x.append(pos[0])
        self._z.append(pos[2])
        self._line.set_data(self._x, self._z)

        # print('add position before scatter')
        # if self._tip:
        #     self._tip.remove()
        # print(f'pos: {pos}')
        # self._tip = plt.scatter(pos[0], pos[2], color='black')
        # print('add position after scatter')

        self.ax.set_xlim(min(self._x) - 5, max(self._x) + 5)
        self.ax.set_ylim(min(self._z) - 5, max(self._z) + 5)

        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

def main():
    gt_loader = GroundTruthLoader('../sequences/03/03.txt')
    viewer = TrajectoryViewer()

    positions = gt_loader.get_all_translations()

    for t in positions:
        viewer.add_position(t)

if __name__ == '__main__':
    main()