from copy import copy
from vector2 import Vector2
import pyxel


class NodeBase:
    def __init__(self):
        self._position = None
        self._rotation = 0
        self._scale = 1.0

    def do(self, *actions):
        """Perform an action on this Node."""
        for act in actions:
            act.do(self)
        return self

    def set_position(self, x, y):
        self._position = Vector2.from_floats(x, y)

    def get_position(self):
        return self._position

    position = property(get_position, set_position, doc="Relative position to parent")

    def set_rotation(self, r):
        self._rotation = r

    def get_rotation(self):
        return self._rotation

    rotation = property(get_rotation, set_rotation, doc="Angle of rotation in degrees")

    def set_scale(self, scale):
        self._scale = scale

    def get_scale(self):
        return self._scale

    scale = property(
        get_scale, set_scale, doc="Sprite scale (1.0 normal, <1.0 smaller, >1.0 bigger)"
    )


class Node(NodeBase):
    def abort_actions(self, type=None):
        """Stop actions immediately."""
        if type is None:
            l = self._actions[:]
        else:
            l = [x for x in self._actions if isinstance(x, type)]
        for act in l:
            act.abort()

    def end_actions(self, type=None):
        """Stop actions at the end of their run."""
        if type is None:
            l = self._actions[:]
        else:
            l = [x for x in self._actions if isinstance(x, type)]
        for act in l:
            act.end()


class Sprite(Node):
    def __init__(self, **kwargs):
        self.x = kwargs["x"]
        self.y = kwargs["y"]
        self.tm = kwargs["tilemap_index"]
        self.u = kwargs["tile_xloc"]
        self.v = kwargs["tile_yloc"]
        self.w = kwargs["tile_width"]
        self.h = kwargs["tile_height"]
        self.colkey = kwargs.get("transparent_colorkey")

    def blit(self):
        pyxel.bltm(self.x, self.y, self.tm, self.u, self.v, self.w, self.h, self.colkey)
