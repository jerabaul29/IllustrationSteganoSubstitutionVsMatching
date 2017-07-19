from __future__ import print_function

import sys
import os

current_root = '/home/jrlab/Desktop/Git/IllustrationSteganoSubstitutionVsMatching/Steganalysis' + '/'
added_path = current_root + '../Steganography/'
print("Added path: " + added_path)
sys.path.append(added_path)

import dummy_stego
import steganalysis
import numpy as np
import matplotlib.pyplot as plt

path_prefix = current_root + '../SourceImages/'

inst_dummy_stego = dummy_stego.dummy_lsb_stego(path_prefix + 'DSC_0027.TIF', path_prefix + 'stego_substitution_DSC_0028.TIF')
image = inst_dummy_stego.inst_image_interaction.image
histogram = steganalysis.produce_histogram(image)
steganalysis.show_histogram(histogram)

steganalysis.show_histogram(histogram, xlim=(52, 83), ylim=(31000, 115000))

inst_dummy_stego.perform_substitution(proportion_hiding=1.0)

image = inst_dummy_stego.inst_image_interaction.image
histogram = steganalysis.produce_histogram(image)
steganalysis.show_histogram(histogram)

steganalysis.show_histogram(histogram, xlim=(52, 83), ylim=(31000, 115000))

inst_attack_lsb_stego = steganalysis.attack_lsb_substitution()
inst_attack_lsb_stego.load_array(image[:, :, 0])

inst_attack_lsb_stego.select_valid_bins(plot=True)
