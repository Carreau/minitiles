from flask import Flask

app = Flask(__name__)

import numpy as np
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
viridis = plt.cm.viridis
import io
from scipy.misc import imsave
from imageio import imwrite

maxx = 1
maxy = 1
maxz = 1

@app.route("/")
def index():
    with open('index.html') as f: 
        return f.read()

def coord_arr(zoom,x,y):
    step = 2**(15-zoom)
    rg = np.arange(256)
    rx = (x*255+rg)*step
    ry = (y*255+rg)*step
    #print(f'from x={x} to {x+1} our array spans from {rx[0]} to {rx[-1]}')
    #print(f'from y={y} to {y+1} our array spans from {ry[0]} to {ry[-1]}')
    return np.meshgrid(rx, ry)


@app.route("/tile/<int:x>/<int:y>/<int:zoom>/<extra>")
def tile(zoom,x,y, extra):
    st = 2**(15-zoom)

    mg = coord_arr(zoom, x,y)
    print('>>>', mg[1][0,0])

    cplx = (mg[0]-4175900+1j*(mg[1]-2778460))/255/255
    print(f'zoom = {zoom}')
    #print(f'Tile span..... {cplx[0,0].real:02c}...{cplx[-1,0]}')
    #print(f'               {cplx[0,-1]}...{cplx[-1,-1]}')
    #print(f"min-max {-np.min(abs(cplx))+np.max(abs(cplx)):4.2}")
    #print(f"min and max {-np.min(abs(cplx)):4.2}/{np.max(abs(cplx)):4.2}")
    arr = abs(cplx)

    arr = np.zeros((256, 256), dtype=np.uint8)
    N = 256
    cc = complex(extra)
    try:
        for i in range(N):
            mask = np.abs(cplx) > 2
            arr[np.abs(cplx)>2] = i
            cplx = cplx**2+cc
    except: 
        return
        pass
    arr = arr*10

    buf= io.BytesIO()
    for where in (buf,):
        imwrite(where, viridis(arr) , format='png')
    buf.seek(0)
    return buf.read()

coord_arr(12, 10, 18)
coord_arr(12, 11, 18)

app.run()
