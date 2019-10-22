class test(object):

    def __init__(self):
        self._a = None
        self.a = 1

    @property
    def a(self):
        return self._a
    
    @a.setter
    def a(self, a):
        print('hello')
        self._a = a


t = test()
