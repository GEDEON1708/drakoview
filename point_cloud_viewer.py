'''
KITTI utilities.
Point cloud viewer.

Author: Bruno Silva
brunomfs@gmail.com
'''

import numpy as np
import matplotlib.pyplot as plt

from lidar_loader import LIDARLoader

class PointCloudViewer:
    '''
    Visualizer for the point clouds
    (LIDAR data) of the
    KITTI datasets.
    '''

    def __init__(self):
        #plt.ion()
        self.fig = None
        self.ax = None
        self._initialize()

    def _initialize(self):
        self.fig = plt.figure(figsize=(2,2))
        self.ax = self.fig.add_subplot(111, projection='3d')

        self.ax.set_title('Scan')
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Z')
        self.ax.view_init(elev=90, azim=-90)

    def add_cloud(self, cloud, k=100, pt_size=0.05):
        '''
        Adds a point cloud (Nx3 numpy.array)
        to the plot.

        Plots only the k-th point for faster
        rendering.
        '''

        self.ax.cla()

        self.ax.set_title('Scan')
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Z')

        self.ax.scatter(cloud[::k,0], cloud[::k,1], cloud[::k,2], s=pt_size, c=cloud[::k,3], cmap='viridis')

        xmin, xmax = -50, 50
        ymin, ymax = -50, 50
        zmin, zmax = -50, 50
        self.ax.set_xlim([xmin-2, xmax+2])
        self.ax.set_ylim([ymin-2, ymax+2])
        self.ax.set_zlim([zmin-2, zmax+2])

        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

def main():
    lidar_loader = LIDARLoader('../sequences/03/velodyne/index.txt')
    viewer = PointCloudViewer()

    clouds = lidar_loader.get_all_scans()

    for c in clouds:
        viewer.add_cloud(c)

if __name__ == '__main__':
    main()