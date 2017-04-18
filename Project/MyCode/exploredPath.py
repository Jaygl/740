#This is to be run in python 3.4 Env with Vispy

"""
Display the environment

Controls:

* 1  - toggle camera between first person (fly), regular 3D (turntable) and
       arcball
* 2  - toggle between volume rendering methods
* 3  - toggle between stent-CT / brain-MRI image
* 4  - toggle between colormaps
* 0  - reset cameras
* [] - decrease/increase isosurface threshold

With fly camera:

* WASD or arrow keys - move around
* SPACE - brake
* FC - move up-down
* IJKL or mouse - look around
"""
import PyQt5
from itertools import cycle
import os
import numpy as np
from math import floor
from vispy import app, scene, io
from vispy.color import get_colormaps, BaseColormap
from vispy.visuals.transforms import STTransform
from sys import exit

testingEnvironment = 4
sensor_range = 20
# Read volume

#Display Path
if testingEnvironment == 1:
    vol1 = np.load('C:/Root/740/Project/Data/generatedEnvironment_1.npy')
    vol1[3, 3, 3] = 10
    vol1[36,36,15] = 10
    temp = np.load('C:/Root/740/Project/Data/Finaloutput_1.npz')
    xpath, ypath, zpath = temp['arr_0'], temp['arr_1'], temp['arr_2']
elif testingEnvironment == 3:
    vol1 = np.load('C:/Root/740/Project/Data/generatedEnvironment_3.npy')
    vol1[90, 50, 5] = 10
    vol1[450, 200, 35] = 10
    temp = np.load('C:/Root/740/Project/Data/Finaloutput_3.npz')
    xpath, ypath, zpath = temp['arr_0'], temp['arr_1'], temp['arr_2']
elif testingEnvironment == 4:
    vol1 = np.load('C:/Root/740/Project/Data/generatedEnvironment_4.npy')
    vol1[90, 50, 5] = 10
    vol1[450, 200, 5] = 10
    temp = np.load('C:/Root/740/Project/Data/Finaloutput_4.npz')
    xpath, ypath, zpath = temp['arr_0'], temp['arr_1'], temp['arr_2']
else:
    exit("testingEnvironment not found...")

(xSize, ySize, zSize) = vol1.shape
xpath2, ypath2, zpath2 = list(xpath), list(ypath), list(zpath)
for k in range(0, len(xpath)):
    xpath2[k], ypath2[k], zpath2[k] = floor(xpath2[k]), floor(ypath2[k]), floor(zpath2[k])
    vol1[xpath2[k],ypath2[k],zpath2[k]] = 10

print(len(xpath2))
#Get the visibility map that the UAV has seen
vol2 = np.zeros_like(vol1)
for k in range(0, len(xpath2)):
    vol2[max(xpath2[k]-sensor_range,0):min(xpath2[k]+sensor_range, xSize), 
        max(ypath2[k]-sensor_range,0):min(ypath2[k]+sensor_range, ySize),
        max(zpath2[k]-sensor_range,0):min(zpath2[k]+sensor_range, zSize)] = vol1[max(xpath2[k]-sensor_range,0):min(xpath2[k]+sensor_range, xSize), 
        max(ypath2[k]-sensor_range,0):min(ypath2[k]+sensor_range, ySize),
        max(zpath2[k]-sensor_range,0):min(zpath2[k]+sensor_range, zSize)]

#for k in range(0, 5):
#    for x in range(-sensor_range, sensor_range):
#        for y in range(-sensor_range, sensor_range):
#            for z in range(-sensor_range,sensor_range):
#                vol2[xpath2[k]+x, ypath2[k]+y, zpath2[k]+z] = vol1[xpath2[k]+x, ypath2[k]+y, zpath2[k]+z]
vol3 = vol1
vol1 = vol2


# Prepare canvas
canvas = scene.SceneCanvas(keys='interactive', size=(800, 600), show=True)
canvas.measure_fps()

# Set up a viewbox to display the image with interactive pan/zoom
view = canvas.central_widget.add_view()

# Set whether we are emulating a 3D texture
emulate_texture = False

# Create the volume visuals, only one is visible
volume1 = scene.visuals.Volume(vol1, parent=view.scene, threshold=0.225,
                               emulate_texture=emulate_texture)
volume1.transform = scene.STTransform(translate=(64, 64, 0))

# Create three cameras (Fly, Turntable and Arcball)
fov = 60.
cam1 = scene.cameras.FlyCamera(parent=view.scene, fov=fov, name='Fly')
cam2 = scene.cameras.TurntableCamera(parent=view.scene, fov=fov,
                                     name='Turntable')
cam3 = scene.cameras.ArcballCamera(parent=view.scene, fov=fov, name='Arcball')
view.camera = cam2  # Select turntable at first

# Create an XYZAxis visual
axis = scene.visuals.XYZAxis(parent=view)
s = STTransform(translate=(50, 50), scale=(50, 50, 50, 1))
affine = s.as_matrix()
axis.transform = affine

# create colormaps that work well for translucent and additive volume rendering
class TransFire(BaseColormap):
    glsl_map = """
    vec4 translucent_fire(float t) {
        return vec4(pow(t, 0.5), t, t*t, max(0, t*1.05 - 0.05));
    }
    """
    
class TransGrays(BaseColormap):
    glsl_map = """
    vec4 translucent_grays(float t) {
        return vec4(t, t, t, t*0.05);
    }
    """

# Setup colormap iterators
opaque_cmaps = cycle(get_colormaps())
translucent_cmaps = cycle([TransFire(), TransGrays()])
opaque_cmap = next(opaque_cmaps)
translucent_cmap = next(translucent_cmaps)


# Implement axis connection with cam2
@canvas.events.mouse_move.connect
def on_mouse_move(event):
    if event.button == 1 and event.is_dragging:
        axis.transform.reset()

        axis.transform.rotate(cam2.roll, (0, 0, 1))
        axis.transform.rotate(cam2.elevation, (1, 0, 0))
        axis.transform.rotate(cam2.azimuth, (0, 1, 0))

        axis.transform.scale((50, 50, 0.001))
        axis.transform.translate((50., 50.))
        axis.update()


# Implement key presses
@canvas.events.key_press.connect
def on_key_press(event):
    global opaque_cmap, translucent_cmap
    if event.text == '1':
        cam_toggle = {cam1: cam2, cam2: cam3, cam3: cam1}
        view.camera = cam_toggle.get(view.camera, cam2)
        print(view.camera.name + ' camera')
        if view.camera is cam2:
            axis.visible = True
        else:
            axis.visible = False
    elif event.text == '2':
        methods = ['mip', 'translucent', 'iso', 'additive']
        method = methods[(methods.index(volume1.method) + 1) % 4]
        print("Volume render method: %s" % method)
        cmap = opaque_cmap if method in ['mip', 'iso'] else translucent_cmap
        volume1.method = method
        volume1.cmap = cmap
    elif event.text == '3':
        volume1.visible = not volume1.visible
    elif event.text == '4':
        if volume1.method in ['mip', 'iso']:
            cmap = opaque_cmap = next(opaque_cmaps)
        else:
            cmap = translucent_cmap = next(translucent_cmaps)
        volume1.cmap = cmap
    elif event.text == '0':
        cam1.set_range()
        cam3.set_range()
    elif event.text != '' and event.text in '[]':
        s = -0.025 if event.text == '[' else 0.025
        volume1.threshold += s
        th = volume1.threshold
        print("Isosurface threshold: %0.3f" % th)

# for testing performance
# @canvas.connect
# def on_draw(ev):
# canvas.update()

if __name__ == '__main__':
    print(__doc__)
    app.run()
