#
# Part of p5: A Python package based on Processing
# Copyright (C) 2017 Abhik Pal
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#

"""Base module for a sketch."""

import builtins
from functools import wraps

import __main__ as user_sketch

import pyglet

from ..opengl import renderer

_min_width = 100
_min_height = 100

builtins.WIDTH = 800
builtins.HEIGHT = 600
builtins.TITLE = "p5py"
builtins.FOCUSED = False
builtins.FRAME_COUNT = None
builtins.FRAME_RATE = None

# builtins.PIXEL_HEIGHT = None
# builtins.PIXEL_WIDTH = None

window = pyglet.window.Window(
    width=WIDTH,
    height=HEIGHT,
    caption=TITLE,
    resizable=False,
    visible=False,
    vsync=True
)

window.set_minimum_size(100, 100)

def initialize(*args, **kwargs):
    gl_version = window.context.get_info().get_version()[:3]
    renderer.initialize(gl_version)
    window.set_visible()

def _default_draw():
    renderer.clear()

def _default_setup():
    pass

def size(width, height):
    """Resize the window.

    :param width: width of the sketch window.
    :type width: int

    :param height: height of the sketch window.
    :type height: int

    """
    builtins.WIDTH = int(width)
    builtins.HEIGHT = int(height)
    window.set_size(width, height)

def title(new_title):
    """Set the title of the p5 window.

    :param new_title: new title of the window.
    :type new_title: str

    """
    window.set_caption("{} - p5".format(new_title))

def run(setup=None, draw=None):
    """Run a sketch.
    """
    # set up required handlers depending on how the sketch is being
    # run (i.e., are we running from a standalone script, or are we
    # running inside the REPL?)

    if (setup is None) and (draw is None):
        if hasattr(user_sketch, 'draw'):
            setup = user_sketch.setup
        if hasattr(user_sketch, 'setup'):
            draw = user_sketch.draw

    if setup is None:
        setup = _default_setup
    elif draw is None:
        draw = _default_draw

    def update(dt):
        renderer.pre_render()
        draw()
        renderer.post_render()

    initialize()
    setup()
    pyglet.clock.schedule(update)
    pyglet.app.run()

def artist(f):
    # a decorator that will wrap around the the "artists" in the
    # sketch -- these are functions that draw stuff on the screen like
    # rect(), line(), etc.
    #
    #    @_p5_artist
    #    def rect(*args, **kwargs):
    #        # code that creates a rectangular Shape object and
    #        # returns it.
    @wraps(f)
    def decorated(*args, **kwargs):
        shape = f(*args, **kwargs)
        renderer.render(shape)
        return shape
    return decorated

def test_run():
    initialize()
    def tester(dt):
        renderer.pre_render()
        renderer.test_render()
        renderer.post_render()
    pyglet.clock.schedule(tester)
    pyglet.app.run()