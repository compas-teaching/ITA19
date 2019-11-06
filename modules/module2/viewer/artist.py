from __future__ import print_function
from __future__ import absolute_import
from __future__ import division


__all__ = ["Artist"]


class Artist(object):
    """Base class for all ``Artist`` objects.

    Parameters
    ----------
    primitive : :class:`compas.geometry.Primitive`
        The instance of the primitive.
    settings : dict (optional)
        A dictionary with visualisation settings.

    Attributes
    ----------
    settings : dict
        Visualisation settings.

    """

    def __init__(self, settings):
        self.settings = settings

    @staticmethod
    def draw_collection(collection):
        raise NotImplementedError

    def draw(self):
        raise NotImplementedError

    def redraw(self):
        raise NotImplementedError

    def draw_dynamic(self):
        # should become a wrapper for using conduits
        raise NotImplementedError

    def draw_animation(self):
        raise NotImplementedError


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':
    pass
