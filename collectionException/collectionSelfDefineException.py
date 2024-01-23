# -*- encoding:utf-8 -*-
class CollectionElementNotFoundException(Exception):
    def __init__(self, text):
        super().__init__()
        self.name = text

    def __str__(self):
        return '{} element no find'.format(self.name)


class ElementNotFoundException(Exception):
    def __init__(self):
        super().__init__()
        self.name = 'NumNotFound'

    def __str__(self):
        return '{}'.format(self.name)
