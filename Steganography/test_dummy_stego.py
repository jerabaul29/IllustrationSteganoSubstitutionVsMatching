from __future__ import print_function
import dummy_stego
import os

current_root = os.path.dirname(os.path.abspath(__file__)) + '/'
print("Using current root: " + current_root)

path_prefix = current_root + '../SourceImages/'

# test lsb substitution --------------------------------------------------------------------
print("----- test lsb substitution -----")

inst_dummy_stego = dummy_stego.dummy_lsb_stego(path_prefix + 'DSC_0028.TIF', path_prefix + 'stego_substitution_DSC_0028.TIF')

# image before lsb substitution
print("Show image before anything done on it...")
inst_dummy_stego.inst_image_interaction.show_image()

# set lsb to zero, just to check everything ok
print("Set lsb to 0 in first half and 1 in second, just to check...")
inst_dummy_stego.set_lsb_to_one_and_zero(debug=0)
inst_dummy_stego.inst_image_interaction.show_image()

print("Perform lsb substitution...")
inst_dummy_stego.perform_substitution(proportion_hiding=1.0, debug=0)

# image after lsb substitution
inst_dummy_stego.inst_image_interaction.show_image()

print("Done with lsb substitution tests!\n")

# test lsb matching ------------------------------------------------------------------------
print("----- test lsb matching -----")

inst_dummy_stego = dummy_stego.dummy_lsb_stego(path_prefix + 'DSC_0028.TIF', path_prefix + 'stego_matching_DSC_0028.TIF')

# image before lsb substitution
print("Show image before anything done on it...")
inst_dummy_stego.inst_image_interaction.show_image()

# set lsb to zero, just to check everything ok
print("Set lsb to 0 in first half and 1 in second, just to check...")
inst_dummy_stego.set_lsb_to_one_and_zero(debug=0)
inst_dummy_stego.inst_image_interaction.show_image()

print("Perform lsb matching...")
inst_dummy_stego.perform_matching(proportion_hiding=1.0)

# image after lsb substitution
inst_dummy_stego.inst_image_interaction.show_image()

print("Done with lsb matching tests!\n")

inst_dummy_stego.inst_image_interaction.path_out
# inst_dummy_stego.inst_image_interaction.write_image()
