# Illustration of steganalysis of lsb substitution

This repository contains code that illustrates the weakness of lsb substitution, and the fact that lsb matching is not so easily discovered. Steganography using lsb substitution or matching should be applied to images that have not been compressed using a lossy algorithm, i.e. to for example .png or .tiff images, but not .jpg or .jpeg.

## Organisation of the repository

- **SourceImages** contains images to use for testing the algorithms.
- **Steganography** contains the code to perform dummy steganography, either lsb substitution or lsb matching. Note that this code performs dummy steganography that should model the behavior of a 'good' steganography tool, but is not able to actually hide information.
- **Steganalysis** contains the code to perform steganalysis of lsb substitution and the evaluation on the test images, and tests agains lsb matching (which, logically enough, cannot be detected by the code designed to reveal lsb substitution).

## To go further

To go further, read for example the blog post https://folk.uio.no/jeanra/Informatics/AFewWordsSteganography.html , and the more detailed pdf https://folk.uio.no/jeanra/Informatics/Vulgatization_steganography.pdf .
