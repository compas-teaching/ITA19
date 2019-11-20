class AssemblyArtist(object):
    """Rudimentary assembly artist for GHpython
    """

    def __init__(self, assembly):
        self.assembly = assembly

    def draw(self):
        from compas_ghpython.artists import MeshArtist
        for vkey, element in self.assembly.elements():
            artist = MeshArtist(element.mesh)
            yield artist.draw_mesh()