# Steganalysis

This code performs steganalysis based on the histogram function of the images. Such attack works very well against lsb substitution, but not against lsb matching.

## Organisation of the code

- **steganalysis.py** contains the code for histogram steganalysis of lsb substitution.
- **evaluate_steganalysis_substitution.py** illustrates how well the histogram analysis works agains lsb matching. Two variants of the histogram analysis are used, one with a hard threshold and the other one with a smarter, relative slope threshold for determining which bins to use in the analysis. The relative slope threshold method should be preferred. The results obtained on the test images are presented in the figures *lsb_substitution_detection_ht.png* and *lsb_substitution_detection_rl.png*, respectively. Each symbol indicates a different figure from the **SourceImages** folder. Note that if you run the test scripts, you may get slight variations in the plots, are the steganographied pictures are random and therefore will be different on each run.
- **evaluate_steganalysis_matching_with_substitution_tool.py** illustrates the fact that the histogram analysis that is successfull on lsb substitution is useless against lsb matching. Results are presented in the figures *lsb_substitution_detection_ht_on_matching.png* and *lsb_substitution_detection_rl_on_matching.png*.
