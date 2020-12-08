import csv
import logging
import time 

from docopt import docopt
import numpy as np


def main():
    """
    Compute binary values for target words.
    """

    # Get the arguments 
    args = docopt("""Compute binary values for taget words.
    
    Usage:
        binary.py [-a] <path_distances> <path_targets> <path_output> <deviation_factor> [<path_areas>]

        <path_distances>    = path to file containing word distance pairs (tab-separated)
        <path_targets>      = path to file containing target words
        <path_output>       = output path for result file
        <deviaton_factor>   = threshold = mean + deviation_factor * std   
        <path_areas>        = file containing the sizes (only needed when using area method)
    
    Options:
        -a, --area  target words are classified by threshold in the freqeuncy area they belong to
        
    """)

    path_distances = args['<path_distances>']
    path_targets = args['<path_targets>']
    path_output = args['<path_output>']
    deviation_factor = float(args['<deviation_factor>'])
    path_areas = args['<path_areas>']

    is_area = args['--area']

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    logging.info(__file__.upper())
    start_time = time.time()

    # Load data 
    distances = {}
    with open(path_distances, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='\t', quoting=csv.QUOTE_NONE, strict=True)
        for row in reader:
            distances[row[0]] = float(row[1])

    with open(path_targets, 'r', encoding='utf-8') as f:
        targets = [line.strip() for line in f]

    # Area method
    if is_area:
        with open(path_areas, 'r', encoding='utf-8') as f:
            areas = f.read().split()

        # Get size of areas
        size1 = int(areas[0])
        size2 = int(areas[1])
        size3 = int(areas[2])
        size4 = int(areas[3])
        size5 = int(areas[4])
    
        # Determine area start points excluding target words
        start1 = 0
        start2 = start1 + int(areas[0])
        start3 = start2 + int(areas[1])
        start4 = start3 + int(areas[2])
        start5 = start4 + int(areas[3])

        # Determine area start points including target words
        start1_target = 0
        start2_target = start1_target + int(areas[5])
        start3_target = start2_target + int(areas[6])
        start4_target = start3_target + int(areas[7])
        start5_target = start4_target + int(areas[8])

        # Put words in according areas, including target words
        area1 = {key:distances[key] for key in list(distances.keys())[start1_target:start2_target]}
        area2 = {key:distances[key] for key in list(distances.keys())[start2_target:start3_target]}
        area3 = {key:distances[key] for key in list(distances.keys())[start3_target:start4_target]}
        area4 = {key:distances[key] for key in list(distances.keys())[start4_target:start5_target]}
        area5 = {key:distances[key] for key in list(distances.keys())[start5_target:]}

        # Create np.arrays containing the distances, excluding target words
        distances1 = np.array(list(area1.values())[0:size1])
        distances2 = np.array(list(area2.values())[0:size2])
        distances3 = np.array(list(area3.values())[0:size3])
        distances4 = np.array(list(area4.values())[0:size4])
        distances5 = np.array(list(area5.values())[0:size5])

        # Compute mean,std and threshold for every area
        mean1 = np.mean(distances1, axis=0)
        std1 = np.std(distances1, axis=0)
        threshold1 = mean1 + deviation_factor * std1

        mean2 = np.mean(distances2, axis=0)
        std2 = np.std(distances2, axis=0)
        threshold2 = mean2 + deviation_factor * std2        
        
        mean3 = np.mean(distances3, axis=0)
        std3 = np.std(distances3, axis=0)
        threshold3 = mean3 + deviation_factor * std3        
        
        mean4 = np.mean(distances4, axis=0)
        std4 = np.std(distances4, axis=0)
        threshold4 = mean4 + deviation_factor * std4        
        
        mean5 = np.mean(distances5, axis=0)
        std5 = np.std(distances5, axis=0)
        threshold5 = mean5 + deviation_factor * std5 

        # Compute binary scores according to area
        binary = {}
        for word in targets:
            if word in area1.keys():
                if distances[word] >= threshold1:
                    binary[word] = 1
                else:
                    binary[word] = 0
            elif word in area2.keys():
                if distances[word] >= threshold2:
                    binary[word] = 1
                else:
                    binary[word] = 0
            elif word in area3.keys():
                if distances[word] >= threshold3:
                    binary[word] = 1
                else:
                    binary[word] = 0
            elif word in area4.keys():
                if distances[word] >= threshold4:
                    binary[word] = 1
                else:
                    binary[word] = 0
            else:
                if distances[word] >= threshold5:
                    binary[word] = 1
                else:
                    binary[word] = 0
    # Normal mehtod
    else:
        # Create dict and np.array without targets 
        dist_without_targets = {}
        for key in distances:
            if key not in targets:
                dist_without_targets[key] = distances[key]
        dist = np.array(list(dist_without_targets.values()))

        # Compute mean, std and threshold
        mean = np.mean(dist, axis=0)
        std = np.std(dist, axis=0)
        threshold = mean + deviation_factor * std

        # Compute bianry scores
        binary = {}
        for word in targets:
            if distances[word] >= threshold:
                binary[word] = 1
            else:
                binary[word] = 0

    # Write output
    with open(path_output, 'w', encoding='utf-8') as f:
        for key, value in binary.items():
            f.write(key + '\t' + str(value) + '\n')

    logging.info("--- %s seconds ---" % (time.time() - start_time))    


if __name__ == '__main__':
    main()
