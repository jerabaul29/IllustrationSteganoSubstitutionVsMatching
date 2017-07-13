from __future__ import print_function
from scipy import misc
import numpy as np
import matplotlib.pyplot as plt


class image_interaction(object):
    """A class for performing interaction with images. This should be used only
    one png, tiff or other format images that have not been compressed."""

    def __init__(self, path_in, path_out):
        """Paths in and out must be to valid png images.
        """

        self.path_in = path_in
        self.path_out = path_out
        self.read_image()

    def read_image(self):
        self.image = misc.imread(self.path_in)[:, :, 0:3]

    def write_image(self):
        misc.imsave(self.path_out, self.image)

    def get_lsb(self):
        lsb = np.mod(self.image, 2)
        return lsb

    def set_lsb(self, new_lsb):
        """Set lsb; this will be useful for lsb substitution."""

        self.image = self.image - self.get_lsb() + np.array(new_lsb, dtype=np.uint8)

    def perform_lsb_matching(self, mask_where, value_set):
        """Perform the lsb matching."""

        lsb_current = self.get_lsb()
        image_current = self.image

        # positions where must change
        must_change = np.logical_and(np.not_equal(lsb_current, value_set), mask_where)

        # positions where must change and 0
        change_0 = np.logical_and(must_change, np.equal(image_current, 0))
        self.image = (self.image.astype(np.int32) + 1 * change_0).astype(np.uint8)

        # positions where must change and 255
        change_0 = np.logical_and(must_change, np.equal(image_current, 255))
        self.image = (self.image.astype(np.int32) - 1 * change_0).astype(np.uint8)

        # other positions where must change
        lsb_current = self.get_lsb()
        must_change = np.logical_and(np.not_equal(lsb_current, value_set), mask_where)
        random_change = np.random.randint(0, 2, lsb_current.shape)
        random_change = 2 * random_change - 1

        self.image = (self.image.astype(np.int32) + random_change * must_change).astype(np.uint8)

    def show_image(self):
        """Show the image.
        """

        plt.figure()
        plt.imshow(self.image)
        plt.title('image')

        lsb = self.get_lsb()

        for channel in range(3):
            plt.figure()
            plt.imshow(lsb[:, :, channel])
            plt.title("lsb channel" + str(channel))

        plt.show()
