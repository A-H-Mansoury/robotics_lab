import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class Visualization:

    def __init__(self):
        
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(projection='3d')
        
        
        self.ax.set_xlabel('X Label')
        self.ax.set_ylabel('Y Label')
        self.ax.set_zlabel('Z Label')
        self.ax.set(xlim=[-100, 100], ylim=[0, 200], zlim=[400, 500])
        self.points = []


    def plot_point(self, X):
        assert X.shape == (3, 1)
        a,b,c = X.ravel()
        point = self.ax.scatter(a, b, c)
        self.points.append(point)

    def update(self, frame):
        for point in self.points:
            point.remove()
        self.points = []

        X = frame[0]
        self.plot_point(X)

    def animate(self, frames):
        ani = FuncAnimation(self.fig, self.update, frames=frames, interval=100)
        ani.save('animation.mp4', writer='ffmpeg')

        plt.show()


