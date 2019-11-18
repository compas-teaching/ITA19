from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import json

from compas.geometry import Frame
from compas.geometry import Transformation
from compas.datastructures import mesh_transform

__all__ = ['Element']

class Element(object):
    """A data structure for the individual elements of a discrete element assembly.

    Attributes
    ----------
    name : str
        The name that identifies the element.
    frame : :class:`compas.geometry.Frame`
        The frame of the element.
    gripping_frame : :class:`compas.geometry.Frame`
        The gripping frame of the element.
        Defaults to the frame.

    Examples
    --------
    from compas.datastructures import Mesh
    frame = Frame.worldXY()
    element = Element(frame)
    mesh = Mesh.from_polyhedron(4)
    ...
    """


    def __init__(self, frame, mesh=None, gripping_frame=None):
        super(Element, self).__init__()
        self.frame = frame
        self.gripping_frame = gripping_frame or frame
        self.mesh = mesh

    @property
    def frame(self):
        """Frame: The element's frame."""
        return self._frame

    @frame.setter
    def frame(self, frame):
        self._frame = Frame(frame[0], frame[1], frame[2])

    @property
    def gripping_frame(self):
        """gripping_frame: The element's gripping frame."""
        return self._gripping_frame

    @gripping_frame.setter
    def gripping_frame(self, frame):
        self._gripping_frame = Frame(frame[0], frame[1], frame[2])

    def __str__(self):
        """Generate a readable representation of the data of the element."""
        return str(self.data)
    
    @property
    def centroid(self):
        return self.mesh.centroid()

    @classmethod
    def from_data(cls, data):
        """Construct an element from its data representation.

        Parameters
        ----------
        data : :obj:`dict`
            The data dictionary.

        Returns
        -------
        Element
            The constructed element.

        Examples
        --------
        >>> data = {frame': Frame.worldXY().data, 'gripping_frame': Frame.worldXY().data}
        >>> element = Element.from_data(data)
        """
        element = cls(Frame.worldXY())
        element.data = data
        return element

    @property
    def data(self):
        """Returns the data dictionary that represents the element.

        Returns
        -------
        dict
            The element data.

        Examples
        --------
        >>> element = Element(Frame.worldXY())
        >>> print(element.data)
        """
        return {'frame'     : self.frame.data,
                'gripping_frame': self.gripping_frame.data,
                'mesh'      : self.mesh
                }

    @data.setter
    def data(self, data):
        self.frame = Frame.from_data(data['frame'])
        self.gripping_frame = data['gripping_frame']

    def to_data(self):
        """Returns the data dictionary that represents the element.
        Returns
        -------
        dict
            The element data.
        Examples
        --------
        from compas.geomtry import Frame
        from compas_fab.assembly import Element
        element = Element(Frame.worldXY())
        print(element.to_data)
        """
        return self.data

    @classmethod
    def from_mesh(cls, mesh=None): # classmethod or instance method?
        """Class method for constructing an element from a COMPAS mesh # or a Rhino mesh
        Parameters
        ----------
        mesh : :class:`compas.geometry.Mesh`
            The COMPAs mesh.
        Returns
        -------
        Element
            The element corresponding to the input mesh.
        """

        centroid = mesh.centroid()
        frame_centroid = Frame(centroid, [1, 0, 0], [0, 1, 0])
        return Element(frame_centroid, mesh=mesh)
    

    def transform(self, transformation):
        self.frame.transform(transformation)
        self.gripping_frame.transform(transformation)
        mesh_transform(self.mesh, transformation)
        
    def __repr__(self):
        return 'Element({}, {})'.format(self.frame, self.gripping_frame)

    def copy(self):
        """Make a copy of this ``Element``.
        Returns
        -------
        Element
            The copy.
        """
        cls = type(self)
        return cls(self.frame.copy(), 
                   mesh=self.mesh.copy(),
                   gripping_frame=self.gripping_frame.copy())

# ==============================================================================
# Main
# ==============================================================================
if __name__ == "__main__":
    pass