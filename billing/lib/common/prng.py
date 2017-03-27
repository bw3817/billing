#----------------------------------------------------------------------
# Author:            Brian Wolf
# Date:                2006.03.22
# Module:            prng.py
# Description:        Generates an ID based upon a
#                    pseudo-random number generator (prng)
#                    using various numbers and letters.
#
# Modifications:
#
#
#----------------------------------------------------------------------


from random import Random


#----------------------------------------------------------------------
# classes
#----------------------------------------------------------------------


class PRNG:
    def __init__(self, size=40):
        self.id = None
        self.DEFAULT_ID_LENGTH = size
        self.DEFAULT_PWD_LENGTH = 8
        self.MAX_ITERATIONS = 10
        self.farm = '0123456789ABCDEFGHJKMNPQRSTVXY'
        self.punctuation = '@#$%^&*'

    def nextID(self, size=None, seed=None):
        r = Random()
        r.seed(seed)
        self.id = ''
        if size is None:
            size = self.DEFAULT_ID_LENGTH
        for char_no in range(size):
            # max iterations to find non-repeating characters
            for n in range(self.MAX_ITERATIONS):
                indx = r.randint(0, len(self.farm) - 1)
                new_char = self.farm[indx]
                if char_no > 0:
                    if new_char != self.id[char_no - 1]: break
            self.id += new_char
        return self.id

    def docID(self, size=None, seed=None):
        r = Random()
        r.seed(seed)
        self.id = ''
        if size is None:
            size = self.DEFAULT_ID_LENGTH
        for char_no in range(size):
            indx = r.randint(0, len(self.farm) - 1)
            self.id += self.farm[indx]
        return self.id

    def genpwd(self, size=None, seed=None):
        r = Random()
        r.seed(seed)
        farm = ('0123456789', 'ABCDEFGHJKMNPQRSTVXY', 'abcdefghjkmnpqrstuvwxy', self.punctuation)
        #farm = ('123456789', 'ABCDEFGHJKMNPQRSTVXY')
        farm_parts_len = len(farm)
        self.id = ''
        if size is None: size = self.DEFAULT_PWD_LENGTH
        # take from each part of farm for first three characters
        for n in range(farm_parts_len):
            self.id += farm[n][r.randint(0, len(farm[n]) - 1)]
        # remainder of characters
        farm = ''.join(farm)
        for char_no in range(size - farm_parts_len):
            # max iterations to find non-repeating characters
            for n in range(10):
                # hexidecimal + some letters
                indx = r.randint(0, len(farm) - 1)
                new_char = farm[indx]
                if new_char != self.id[char_no]: break
            self.id += new_char
        return self.id

