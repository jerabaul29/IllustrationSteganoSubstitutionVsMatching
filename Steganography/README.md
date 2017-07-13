# Steganography

This code performs dummy lsb substitution or matching.

Dummy means, that random data is hiden in the lsb at random places. This should be a simple to implement but accurate model of a 'good' steganography tool, that spreads randomly the information in the image and strongly encrypts the data.

## Organisation of the code

- **image_interaction.py** helps reading, writing, substituting lsb, and matching lsb on images.
- **dummy_stego.py** performs dummy substitution or matching.
- **test_dummy_stego.py** shows the output of steganography and was used to debug.

