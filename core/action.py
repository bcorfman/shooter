import sys, traceback
from copy import copy
from .vector2 import Vector2

StopMode = 0
RepeatMode = 1
PingPongMode = 2


class Action(object):
    def __init__(self):
        self._next = None
        self._node = None
        self._limit = None
        self._aborted = False

    aborted = property(lambda self: self._aborted)

    def __add__(self, other):
        obj = self.copy()
        obj.chain(other)
        return obj

    def __iadd__(self, other):
        self.chain(other)
        return self

    def __radd__(self, other):
        if type(other) is type:
            other = other()
        else:
            other = other.copy()
        other.chain(self)

    def copy(self):
        obj = copy(self)
        if self._next is not None:
            obj._next = self._next.copy()
        return obj

    def chain(self, other):
        if self._next is not None:
            self._next.chain(other)
        else:
            if type(other) is type:
                other = other()
            else:
                other = other.copy()
            self._next = other

    def limit(self, time):
        if time < 0:
            time = 0
        self._limit = time
        return self

    def end(self):
        self.on_end()

    def abort(self):
        self._aborted = True
        self.end()

    def do(self, *actors):
        if not actors:
            actors = [None]
        result = []
        for node in actors:
            obj = self.copy()
            obj._callbacks = None
            obj._node = node
            obj.activate()
            result.append(obj)
        if len(result) == 1:
            return result[0]
        return result

    def activate(self):
        if self._node is not None:
            if self._node.deleted:
                self._aborted = True
                return
            self._node._actions.add(self)
        self.on_activate()

    def on_activate(self):
        pass

    def on_end(self):
        if self._node is not None:
            self._node._actions.discard(self)
        if self.aborted:
            return
        try:
            if self._next is not None:
                self._next._node = self._node
                self._next.activate()
        except:
            traceback.print_exc(sys.stdout)
            sys.stdout.flush()
            raise


class CallFunc(Action):
    def __init__(self, _func, *arg, **kw):
        self.func = _func
        self.arg = arg
        self.kw = kw
        Action.__init__(self)

    def on_activate(self):
        self.func(*self.arg, **self.kw)
        self.on_end()


class CallFuncNode(CallFunc):
    def on_activate(self):
        self.func(self._node, *self.arg, **self.kw)


class Delete(Action):
    def on_activate(self):
        n = self._node
        self._node = None
        self.on_end()
        if n is not None:
            n.delete()


class Repeat(Action):
    def __init__(self, action, repeats=None):
        self.action = action
        self.repeats = repeats
        Action.__init__(self)

    def on_activate(self):
        if self.repeats is None:
            do = True
        elif self.repeats > 0:
            do = True
            self.repeats -= 1
        else:
            do = False
        if do:
            act = self.action.copy() + CallFunc(self.activate)
            act.do(self._node)
        else:
            self.on_end()


class Move(Action):
    def __init__(self, velocity):
        Action.__init__(self)
        self.velocity = velocity

    def on_activate(self):
        self.activate(Move, Vector2(*self.velocity))


class Delay(Action):
    _needs_node = False

    def __init__(self, secs):
        Action.__init__(self)
        self.secs = secs

    def on_activate(self):
        self.activate(Delay, self.secs)


class IntervalAction(Action):
    def __init__(self, secs, mode=StopMode):
        Action.__init__(self)
        self.secs = secs
        self.mode = mode
        self.fadein = None

    def smooth(self, fadein, fadeout):
        self.fadein = fadein
        self.fadeout = fadeout
        return self
