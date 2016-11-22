## author: Jorge Castillo

import numpy as np
from vispy import app, gloo
from vispy.gloo.util import _screenshot

vertex = """
attribute vec2 a_position;
varying vec2 v_position;
void main()
{
    gl_Position = vec4(a_position, 0.0, 1.0);
    v_position = a_position;
}
"""

fragment = """
#include "math/constants.glsl"
//const float M_PI = 3.14159265358979323846;
uniform float u_time;
varying vec2 v_position;

/**********************************************************
        parameters
**********************************************************/
const float z_offset = 1.5;  // (z+z_offset)/z_max should be in [0,1]
const float z_max = 2.;
const float x_scale = 3.;  // x is between -x_scale and +x_scale
const float y_scale = 3.; // y is between -y_scale and +y_scale
const float t_scale = 5.; // scale for the time
const float amplitude = 0.25;
/*********************************************************/

float f(float x, float y, float t) {

    // x is in [-x_scale, +x_scale]
    // y is in [-y_scale, +y_scale]
    // t is in [0, +oo)

    /**********************************************************
    FUNCTIONS.
    **********************************************************/

    float k = pow(cos(t*10), 2)/(21);

    float transition = (10/pow(t, 1.5));

    float i1 = cos(t/4)*0 + transition*0;
    float j1 = sin(t/4)*0;

    float i2 = -cos(t/4)*0 - transition*0;
    float j2 = -sin(t/4)*0;

    return (((pow(x-1.5, 2) + pow(y-0, 2) )/1.5
            *(pow(x+1.5, 2) + pow(y-0, 2))/1.5
            + k)/2);

    /*********************************************************/

}

vec4 jet(float x) {

    vec3 a, b;
    float c;

    // rgb(132,255,255)
    // rgb(0,188,212)
    // rgb(66,66,66)

    if (x < 0.89) {
         a = vec3(0, 188./255., 212./255.);
         b = vec3(132/255., 188./255., 212./255.);
         c = (x - 0.64) / (0.89 - 0.64);
    } else {
        a = vec3(132./255., 188./255., 212./255.);
        b = vec3(1./255., 1./255., 33./255.);
        c = (x - 0.89) / (1.0 - 0.89);
    }
    return vec4(mix(a, b, c), 1.0);
}

void main() {
    vec2 pos = v_position;
    float z = f(x_scale * pos.x, y_scale * pos.y, t_scale * u_time);
    gl_FragColor = (jet((z + z_offset) / (z_max))*1.5);
}
"""


class Canvas(app.Canvas):
    def __init__(self):
        app.Canvas.__init__(self, position=(300, 100),
                            size=(800, 800), keys='interactive')

        self.program = gloo.Program(vertex, fragment)
        self.program['a_position'] = [(-1., -1.), (-1., +1.),
                                      (+1., -1.), (+1., +1.)]

        self.program['u_time'] = 0.0
        self.timer = app.Timer('auto', connect=self.on_timer, start=True)

        self.show()

    def on_timer(self, event):
        self.program['u_time'] = event.elapsed
        self.update()

    def on_resize(self, event):
        width, height = event.physical_size
        gloo.set_viewport(0, 0, width, height)

    def on_draw(self, event):
        self.program.draw('triangle_strip')

    def movie_animate(self, t):
        self.program['u_time'] = t
        self.update()
        gloo.clear()
        self.program.draw('triangle_strip')
        return _screenshot((0, 0, self.size[0], self.size[1]))[:,:,:3]

if __name__ == '__main__':
    #from moviepy.editor import VideoClip
    canvas = Canvas()
    #clip = VideoClip(canvas.movie_animate, duration=10)
    #clip.write_gif('hyrdogen.gif', fps=20, opt='OptimizePlus')
    app.run()
