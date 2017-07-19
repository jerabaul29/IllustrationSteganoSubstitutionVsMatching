from __future__ import print_function
import numpy as np
import matplotlib.pyplot as plt


def produce_histogram(array, n_bits=8):
    number_of_bins = np.max(array)
    number_of_occurences = np.zeros(number_of_bins + 1)

    for value in array.flatten():
        number_of_occurences[value] += 1

    return number_of_occurences


def show_histogram(histogram_intensity, ylim=None, xlim=None, fig_and_show='True'):
    if fig_and_show:
        plt.figure()

    plt.bar(np.arange(0, histogram_intensity.size, 1), histogram_intensity)

    plt.xlabel('Intensity')
    plt.ylabel('Count')

    if xlim is not None:
        plt.xlim([xlim[0], xlim[1]])

    if ylim is not None:
        plt.ylim([ylim[0], ylim[1]])

    if fig_and_show:
        plt.show()


def produce_finite_difference(array):
    d = array[1:] - array[0: -1]
    return d


def separate_even_uneven_histogram(histogram, selection_method='threshold', arg_method=None, plot=False):
    histogram_length = histogram.size

    sum_variations_0 = 0
    sum_variations_1 = 0

    list_color = []

    for ind in range(histogram_length):
        abs_value = abs(histogram[ind])

        if selection_method == 'threshold':
            threshold_min = arg_method[0]
            threshold_max = arg_method[1]
            if abs_value > threshold_min and abs_value < threshold_max:
                list_color.append('r')
                if ind % 2 == 0:
                    sum_variations_0 += abs_value

                else:
                    sum_variations_1 += abs_value

            else:
                list_color.append('b')

        elif selection_method == 'rel_slope':
            set_valid = arg_method
            if ind / 2 in set_valid:
                list_color.append('r')

                if ind % 2 == 0:
                    sum_variations_0 += abs_value

                else:
                    sum_variations_1 += abs_value

            else:
                list_color.append('b')

    if plot:
        plt.figure()
        plt.bar(np.arange(0, histogram_length, 1), histogram, color=list_color)
        plt.show()

    return (sum_variations_0, sum_variations_1)


def histogram_mean_even_uneven(histogram):
    histogram_length = histogram.size

    number_of_new_bins = int(histogram_length / 2.0)

    array_histogram_mean_even_uneven = np.zeros((number_of_new_bins))

    for ind in range(number_of_new_bins):
        array_histogram_mean_even_uneven[ind] = histogram[2 * ind] + histogram[2 * ind + 1]

    return array_histogram_mean_even_uneven


class attack_lsb_substitution(object):
    def load_array(self, array_in):
        if len(array_in.shape) > 2:
            print("warning, using RGB array")
            array_R = array_in[:, :, 0]
            array_G = array_in[:, :, 1] + 256
            array_B = array_in[:, :, 2] + 256 * 2

            self.array_in = np.concatenate((array_R, array_G, array_B)).flatten()

        else:
            self.array_in = array_in.flatten()

        self.histogram = produce_histogram(self.array_in)

    def compute_difference_histogram(self):
        self.d_histogram = produce_finite_difference(self.histogram)

    def separate_difference_histogram(self, selection_method='threshold', arg_method=None, plot=False):
        (sum_a_differences_0, sum_a_differences_1) = separate_even_uneven_histogram(self.d_histogram, selection_method=selection_method,
                                                                                    arg_method=arg_method, plot=plot)
        self.difference_0 = sum_a_differences_0
        self.difference_1 = sum_a_differences_1

    def compute_proportion_embedding(self):
        self.p = abs((self.difference_0 - self.difference_1) / (self.difference_0 + self.difference_1))

    def select_valid_bins(self, threshold_rel_variation_slope=0.5, min_slope=100, plot=False):
        # compute mean histogram on each pair belonging to the same lsb-1
        hist_mean_eu = histogram_mean_even_uneven(self.histogram)

        # compute the dif and the dif^2 of this histogram
        dif_hist_mean_eu = produce_finite_difference(hist_mean_eu)

        average_dif_hist_mean_eu = (dif_hist_mean_eu[1:] + dif_hist_mean_eu[0:-1]) / 2.0
        dif_dif_hist_mean_eu = produce_finite_difference(dif_hist_mean_eu)

        # select the valid bins to use in the separate difference analysis
        self.set_diffs_to_use = set()

        for ind in range(dif_dif_hist_mean_eu.size):
            # print(dif_dif_hist_mean_eu[ind])
            # print(average_dif_hist_mean_eu[ind])

            current_ratio = float(dif_dif_hist_mean_eu[ind]) / average_dif_hist_mean_eu[ind]

            # print(current_ratio)

            if abs(current_ratio) < threshold_rel_variation_slope and abs(average_dif_hist_mean_eu[ind]) > min_slope:
                self.set_diffs_to_use.add(ind)
                self.set_diffs_to_use.add(ind + 1)

        # show_histogram(self.histogram, ylim=None)
        # show_histogram(hist_mean_eu, ylim=None)
        # show_histogram(dif_hist_mean_eu, ylim=None)
        # show_histogram(dif_dif_hist_mean_eu, ylim=None)
        # print(self.set_diffs_to_use)

        if plot:
            plt.figure()

            plt.subplot(2, 1, 1)
            plt.bar(np.arange(0, self.histogram.size, 1), self.histogram)

            plt.xlabel('Intensity')
            plt.ylabel('Count')

            plt.subplot(2, 1, 2)
            color = []
            for ind in range(hist_mean_eu.size):
                if ind in self.set_diffs_to_use:
                    color.append('r')
                else:
                    color.append('b')
            plt.bar(np.arange(0, hist_mean_eu.size, 1), hist_mean_eu, color=color)

            plt.xlabel('Intensity')
            plt.ylabel('Count')

            plt.figure()
            color = []
            for ind in range(hist_mean_eu.size):
                if ind in self.set_diffs_to_use:
                    color.append('r')
                    color.append('r')
                else:
                    color.append('b')
                    color.append('b')

            plt.bar(np.arange(0, self.histogram.size, 1), self.histogram, color=color)

            plt.xlabel('Intensity')
            plt.ylabel('Count')

            plt.show()

    def return_proportion_embedding(self, selection_method='threshold', threshold_min=1000, threshold_max=5000, threshold_rel_variation_slope=0.2,
                                    min_slope=50, plot=False):
        if selection_method == 'threshold':
            self.compute_difference_histogram()
            self.separate_difference_histogram(selection_method='threshold', arg_method=(threshold_min, threshold_max), plot=plot)
            self.compute_proportion_embedding()

            return(self.p)

        elif selection_method == 'rel_slope':
            self.compute_difference_histogram()
            self.select_valid_bins(threshold_rel_variation_slope=threshold_rel_variation_slope, min_slope=min_slope, plot=plot)

            if not bool(self.set_diffs_to_use):
                print("No bins found that match the criterion. Aborting")
                return -1

            self.separate_difference_histogram(selection_method='rel_slope', arg_method=(self.set_diffs_to_use), plot=plot)
            self.compute_proportion_embedding()

            return(self.p)

        else:
            print("selection method " + selection_method + " not implemented!")
