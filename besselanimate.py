import matplotlib
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
from scipy.special import jv, jn_zeros
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.colors import hex2color
import matplotlib.colors as mcolors
import time

#Input modes to calc roots
var_im = int(input("Enter the number of modes - m: ,"))
var_in = int(input("Enter the number of modes - n: ,"))
var_clrmap = str(input("Enter the colormap for surface plot: ,"))
var_nc = int(input("Enter the number of cycles per mode: ,"))
var_fps = int(input("Enter the frames per second: ,"))
var_zlim = float(input("Enter the height of the z axis: ,"))
var_r_count = int(input("Enter the number of radial grids for surface plot: ,"))
var_c_count = int(input("Enter the number of angular grids for surface plot: ,")


var_radius = 1 #This is the radius of the membrane
lst_roots = [] #initializing roots of the Bessel function
tpl_modes = [] #initialzing the modes (tuple) of the Bessel function

# Nested for loops to generate tuples
for i in range(var_im):
    for j in range(1, var_in + 1):
        tpl_modes.append((i, j))

# Nested for loops to generate roots
for m in range(10):
    zeros_m = jn_zeros(m, 10)
    lst_roots.append(zeros_m)

#figure setup - note the colormap variable reference
fig = plt.figure(figsize=(40, 25))
ax = fig.add_axes([0, 0, 1, 1], projection='3d')
cmap = plt.get_cmap(var_clrmap)
norm = plt.Normalize(-0.5, 0.5)

# i here is a counter and gets updated by calling the function below
def update(i):
    t = i / var_fps
    mode_idx = i // (var_nc * var_fps)
    #update m, n
    m, n = tpl_modes[mode_idx]

    r = np.linspace(0, var_radius, 50)
    theta = np.linspace(0, 2 * np.pi, 50)
    r, theta = np.meshgrid(r, theta)

    x = r * np.cos(theta)
    y = r * np.sin(theta)
    l = lst_roots[m][n - 1] / var_radius

    T = np.sin(l * t)
    R = jv(m, l * r)
    Theta = np.cos(m * theta)

    z = R * T * Theta

    ax.clear()
    ax.plot_surface(
        x,
        y,
        z,
        cmap=cmap,
        norm=norm,
        linewidth=0,
        rcount=var_r_count,
        ccount=var_c_count,
    )

    ax.set_zlim(-var_zlim, var_zlim)
    ax.xaxis.set_pane_color((1.0, 1.0, 1.0, 1.0))
    ax.yaxis.set_pane_color((1.0, 1.0, 1.0, 1.0))
    ax.zaxis.set_pane_color((1.0, 1.0, 1.0, 1.0))
    ax.grid(False, color=(0.9, 0.9, 1.0, 1.0))
    ax.set_position([-0.14, 0.1, 1.0, 0.75])
    ax.axis('on')
    plt.suptitle(f'Vibration modes of a circular membrane (Bessel function): {m, n}',x=0.37,y=0.95, fontsize=25,color='red')

    if i == len(tpl_modes) * var_nc * var_fps - 1:
        plt.close()

ani = FuncAnimation(
    fig,
    update,
    frames=len(tpl_modes) * var_nc * var_fps,
    interval=1000/var_fps,  # Adjusted interval
    repeat=False)

root = plt.get_current_fig_manager().window
left_offset = root.winfo_screenwidth() * 24 // 100
root.wm_geometry("+%d+%d" % (left_offset, 0))

plt.show()
