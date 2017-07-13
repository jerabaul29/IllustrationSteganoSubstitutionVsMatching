"""
Perform dummy lsb substitution or matching on an image using randomly generated
data at random locations.

This can be used to look for detection techniques of Steganography. The random
data should be the analogous of strongly encrypted data.
"""

import image_interaction
import numpy as np


class dummy_lsb_stego(object):
    def __init__(self, path_in, path_out, substitution_location='random',
                 proportion_hiding=1.):
        """Use image in path_in for steganogralphy and save it in path_out. The
        message used is a random binary string.

        substitution_location:
            random: randomly select the positions where to perform the substitution.

        proportion_hiding:
            proportion of the pixels on which to perform substitution.
        """

        self.inst_image_interaction = image_interaction.image_interaction(path_in, path_out)

        self.substitution_location = substitution_location
        self.proportion_hiding = proportion_hiding

    def set_lsb_to_one_and_zero(self, debug=0):
        """Put half the image lsbs to 0 and half to 1. This was used for debugging.
        """
        lsb = self.inst_image_interaction.get_lsb()

        lsb_shape = lsb.shape
        lsb_size = lsb.size

        lsb = np.zeros((lsb_shape))

        lsb = lsb.reshape([lsb_size])
        max_ind_1 = int(lsb_size / 2.0)
        lsb[0: max_ind_1] = 1
        lsb = lsb.reshape(list(lsb_shape))

        if debug > 5:
            print lsb

        self.inst_image_interaction.set_lsb(lsb)

        if debug > 5:
            print self.inst_image_interaction.image

    def generate_mask(self, proportion_hiding):
        """Generate a mask that selects proportion_hiding proportion of the pixels.
        If the substitution_location is random, then do a permutation of the mask
        so that random pixels are used for steganography.
        """

        lsb = self.inst_image_interaction.get_lsb()

        lsb_size = lsb.size
        lsb_shape = lsb.shape

        mask = np.zeros(lsb_shape)
        stegano_length = int(proportion_hiding * lsb_size)

        mask = mask.reshape([lsb_size])
        mask[0: stegano_length] = 1

        if self.substitution_location == 'random':
            # random boolean mask for which values will be changed
            mask = np.random.permutation(mask).astype(np.bool)

        mask = mask.reshape((lsb_shape))

        return mask

    def perform_substitution(self, debug=0, proportion_hiding=None):
        """Perform lsb substitution on proportion_hiding of the pixels.
        """

        if proportion_hiding is None:
            proportion_hiding = self.proportion_hiding

        lsb = self.inst_image_interaction.get_lsb()

        mask = self.generate_mask(proportion_hiding)

        # random matrix the same shape of the data
        r = np.random.randint(0, 2, lsb.shape)

        # use the mask to replace values in the input array
        lsb[mask] = r[mask]

        self.inst_image_interaction.set_lsb(lsb)

    def perform_matching(self, proportion_hiding=None):
        """Perform lsb matching on proportion_hiding of the pixels.
        """

        if proportion_hiding is None:
            proportion_hiding = self.proportion_hiding

        lsb = self.inst_image_interaction.get_lsb()

        lsb_size = lsb.size
        lsb_shape = lsb.shape

        value_set = np.random.randint(0, 2, lsb.shape)

        mask = self.generate_mask(proportion_hiding)

        self.inst_image_interaction.perform_lsb_matching(mask, value_set)
