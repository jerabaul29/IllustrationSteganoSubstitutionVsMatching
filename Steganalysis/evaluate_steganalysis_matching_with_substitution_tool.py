from __future__ import print_function

import sys, os

current_root = os.path.dirname(os.path.abspath(__file__)) + '/'
added_path = current_root + '../Steganography/'
print("Added path: " + added_path)
sys.path.append(added_path)

import dummy_stego
import steganalysis
import numpy as np
import matplotlib.pyplot as plt

path_prefix = current_root + '../SourceImages/'
list_images = ['DSC_0024.TIF', 'DSC_0025.TIF', 'DSC_0026.TIF', 'DSC_0027.TIF', 'DSC_0029.TIF']
list_embeddings = list(np.arange(0, 1.02, 0.05))

markers = {0: u'tickleft', 1: u'tickright', 2: u'tickup', 3: u'tickdown', 4: u'caretleft', u'D': u'diamond', 6: u'caretup',
           7: u'caretdown', u's': u'square', u'|': u'vline', None: u'nothing', u'None': u'nothing', u'x': u'x',
           5: u'caretright', u'_': u'hline', u'^': u'triangle_up', u' ': u'nothing', u'd': u'thin_diamond', u'h': u'hexagon1',
           u'+': u'plus', u'*': u'star', u',': u'pixel', u'o': u'circle', u'.': u'point', u'1': u'tri_down', u'p': u'pentagon', u'3': u'tri_left',
           u'2': u'tri_up', u'4': u'tri_right', u'H': u'hexagon2', u'v': u'triangle_down', u'': u'nothing', u'8': u'octagon', u'<': u'triangle_left',
           u'>': u'triangle_right'}

marker_list = ['*', 'o', '+', 'X', 'D', '1', '2', '3', '4', '8']
color_list = ['b', 'g', 'r', 'c', 'm', 'y', 'k']

# suffix 1 designates hard threshold; suffix 2 designate relative slope

list_embedding_values_1 = []
list_predicted_embedding_1 = []
list_image_considered_1 = []

n_cases_1 = 0

list_embedding_values_2 = []
list_predicted_embedding_2 = []
list_image_considered_2 = []

n_cases_2 = 0

for ind_image, crrt_image in enumerate(list_images):
    for crrt_embedding in list_embeddings:
        n_cases_1 += 1

        list_image_considered_1.append(ind_image)
        list_embedding_values_1.append(crrt_embedding)

        inst_dummy_stego = dummy_stego.dummy_lsb_stego(path_prefix + crrt_image, path_prefix + 'stego' + crrt_image)

        inst_dummy_stego.perform_matching(proportion_hiding=crrt_embedding)
        image_after_substitution = inst_dummy_stego.inst_image_interaction.image
        inst_attack_lsb_stego = steganalysis.attack_lsb_substitution()
        inst_attack_lsb_stego.load_array(image_after_substitution[:, :, 0])
        embedding_predicted = inst_attack_lsb_stego.return_proportion_embedding()

        list_predicted_embedding_1.append(embedding_predicted)

        print("Image, Embedding (true): " + str(crrt_image) + " , " + str(crrt_embedding))
        print("Embedding, predicted   :                " + str(embedding_predicted))
        
for ind_image, crrt_image in enumerate(list_images):
    for crrt_embedding in list_embeddings:
        n_cases_2 += 1

        list_image_considered_2.append(ind_image)
        list_embedding_values_2.append(crrt_embedding)

        inst_dummy_stego = dummy_stego.dummy_lsb_stego(path_prefix + crrt_image, path_prefix + 'stego' + crrt_image)

        inst_dummy_stego.perform_matching(proportion_hiding=crrt_embedding)
        image_after_substitution = inst_dummy_stego.inst_image_interaction.image
        inst_attack_lsb_stego = steganalysis.attack_lsb_substitution()
        inst_attack_lsb_stego.load_array(image_after_substitution[:, :, 0])
        embedding_predicted = inst_attack_lsb_stego.return_proportion_embedding(selection_method='rel_slope', threshold_rel_variation_slope=0.5)

        list_predicted_embedding_2.append(embedding_predicted)

        print("Image, Embedding (true): " + str(crrt_image) + " , " + str(crrt_embedding))
        print("Embedding, predicted   :                " + str(embedding_predicted))

array_data = np.array(list_embedding_values_1 + list_predicted_embedding_1 + list_image_considered_1 + list_embedding_values_2 + list_predicted_embedding_2 + list_image_considered_2)
np.save('data_out.npy', array_data)

plt.figure()
for ind in range(n_cases_1):
    plt.scatter(list_embedding_values_1[ind], list_predicted_embedding_1[ind], marker=marker_list[list_image_considered_1[ind]],
                color=color_list[list_image_considered_1[ind]])
plt.xlabel('True embedding fraction')
plt.ylabel('Predicted embedding fraction')
plt.title("Using hard threshold")


plt.figure()
for ind in range(n_cases_2):
    plt.scatter(list_embedding_values_2[ind], list_predicted_embedding_2[ind], marker=marker_list[list_image_considered_2[ind]],
                color=color_list[list_image_considered_2[ind]])
plt.xlabel('True embedding fraction')
plt.ylabel('Predicted embedding fraction')
plt.title("Using relative slope")
plt.show()
