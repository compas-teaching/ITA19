from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import ast
import json

from compas.datastructures import Network
from .element import Element


__all__ = ['Assembly']

#g = gravity

class Assembly(object):
    """A data structure for discrete element assemblies.

    An assembly is essentially a network of assembly elements.
    Each vertex of the network represents an element of the assembly.
    Each edge of the network represents an interface between two assembly elements.
    
    Attributes
    ----------
    blocks : list of :class:`compas_assembly.datastructures.Block`, optional
        A list of assembly blocks.
    attributes : dict, optional
        User-defined attributes of the assembly.
        Built-in attributes are:
        * name (str) : 'Assembly'
    default_vertex_attributes : dict, optional
        User-defined default attributes of the vertices of the network.
        Since the vertices of the assembly network represent the individual
        elements, the built-in attributes are:
        * is_support (bool) : False
    default_edge_attributes : dict, optional
        User-defined default attributes of the edges of the network.
        Since the edges of the assembly network represent the interfaces between
        the individual elements, the built-in attributes are:
        * interface_points (list) : None
        * interface_type ({'face_face', 'face_edge', 'face_vertex'}) : None
        * interface_size (float) : None
        * interface_uvw (list) : None
        * interface_origin (list) : None
        * interface_forces (list) : None

    Examples
    --------
    >>> assembly = Assembly()
    >>> for i in range(2):
    >>>     block = Block.from_polyhedron(6)
    >>>     assembly.add_block(block)
    >>> print(assembly.summary())
    """

    __module__ = 'compas_assembly.datastructures'

    def __init__(self,
                 elements=None,
                 attributes=None,
                 default_vertex_attributes=None,
                 default_edge_attributes=None):
        
        self.network = Network()
        self.elements = {}

        self.network.attributes.update({'name': 'Assembly'})
        if attributes is not None:
            self.network.attributes.update(attributes)

        self.network.default_vertex_attributes.update({
            'is_support': False,
            'is_placed': False,
            'course': None,
        })

        if default_vertex_attributes is not None:
            self.network.default_vertex_attributes.update(default_vertex_attributes)

        self.network.default_edge_attributes.update({
            'interface_points': None,
            'interface_type': None,
            'niterface_size': None,
            'interface_uvw': None,
            'interface_origin': None,
            'interface_forces': None,
        })

        if default_edge_attributes is not None:
            self.network.default_edge_attributes.update(default_edge_attributes)

        if elements:
            for element in elements:
                self.add_element(element)

    @classmethod
    def from_json(cls, filepath):
        """Construct an assembly from the data contained in a JSON file.

        Parameters
        ----------
        filepath : str
            Path to the file containing the data.
        
        Returns
        -------
        Assembly
            An assembly data structure.
        
        Examples
        --------
        >>> assembly = Assembly.from_json('assembly.json')
        """

        with open(filepath, 'r') as fo:
            data = json.load(fo)

            # vertex keys in an assembly can be of any hashable type
            # keys in the blocks dict should be treated the same way!

            assembly = cls.from_data(data['assembly'])
            assembly.elements = {int(key): Element.from_data(data['blocks'][key]) for key in data['blocks']}

        return assembly

    def to_json(self, filepath):
        """Serialise the data dictionary representing an assembly to JSON and store in a file.

        Parameters
        ----------
        filepath : str
            Path to the file.
        
        Examples
        --------
        >>> assembly = Assembly.from_json('assembly.json')
        >>> # do stuff
        >>> assembly.to_json('assembly.json')
        """
        data = {
            'assembly': self.to_data(),
            'blocks': {str(key): self.elements[key].to_data() for key in self.elements}
        }
        with open(filepath, 'w') as fo:
            json.dump(data, fo, indent=4, sort_keys=True)

    def copy(self):
        """Make an independent copy of an assembly.

        Examples
        --------
        >>> copy_of_assembly = assembly.copy()
        """
        assembly = super(Assembly, self).copy()
        assembly.elements = {key: self.blocks[key].copy() for key in self.vertices()}
        return assembly

    def add_element(self, element, key=None, attr_dict={}, **kwattr):
        """Add an element to the assembly.

        Parameters
        ----------
        block : compas_assembly.datastructures.Block
            The block to add.
        attr_dict : dict, optional
            A dictionary of block attributes. Default is ``None``.

        Returns
        -------
        hashable
            The identifier of the block.

        Notes
        -----
        The block is added as a vertex in the assembly data structure.
        The XYZ coordinates of the vertex are the coordinates of the centroid of the block.
        """
        attr_dict.update(kwattr)
        x, y, z = element.centroid
        key = self.network.add_vertex(key=key, attr_dict=attr_dict, x=x, y=y, z=z)
        self.elements[key] = element
        return key

    def number_of_interface_vertices(self):
        """Compute the total number of interface vertices.

        Returns
        -------
        int
            The number of vertices.
        """
        return sum(len(attr['interface_points']) for u, v, attr in self.edges(True))

    def subset(self, keys):
        """Create an assembly that is a subset of the current assembly.

        Parameters
        ----------
        keys : list
            Identifiers of the blocks that should be included in the subset.

        Returns
        -------
        :class: `Assembly`
            The sub-assembly.

        Examples
        --------
        >>> assembly = Assembly.from_json('assembly.json')
        >>> sub = assembly.subset([0, 1, 2, 3])
        """
        cls = type(self)
        sub = cls()
        for key, attr in self.network.vertices(True):
            if key in keys:
                block = self.elements[key].copy()
                sub.network.add_vertex(key=key, **attr)
                sub.network.elements[key] = block
        for u, v, attr in self.network.edges(True):
            if u in keys and v in keys:
                sub.network.add_edge(u, v, **attr)
        return sub



# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    pass