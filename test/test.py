import sys
import os
curr_dir = os.path.dirname(os.path.abspath(__file__))
prj_root = os.path.abspath(os.path.join(curr_dir, "../"))
sys.path.append(prj_root)

from tqdm import tqdm
import random
import re
from cross_line_word_detector import CrossLineWordDetector
import logging

test_data_list = []
test_case_limit = 10000
with open ('text.txt', 'r') as f:
    for line in tqdm(f):
        words = re.split(r'\s', line)
        for word in words:
            size = len(word)
            if size <= 2 or random.random() < 0.5: continue
            index = random.randint(1, size-2)
            a, b = word[:index], word[index:]
            test_data_list.append([a, b, True])
            test_data_list.append([a + "-", b, True])
            if len(test_data_list) == test_case_limit: break
        if len(test_data_list) == test_case_limit: break

positive_count = len(test_data_list)
for i in range(min(positive_count, 1000)):
    j = random.randint(0, positive_count-1)
    a = test_data_list[i][0]
    b = test_data_list[j][1]
    test_data_list.append([a, b, False])

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setLevel(logging.DEBUG)
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)
crossLineWordDetector = CrossLineWordDetector(logger=logger)

error_count = 0
tp, fp, tn, fn = 0, 0, 0, 0
for case in test_data_list:
    a, b, label = case
    is_word = crossLineWordDetector.detect(a, b, True)
    if is_word == True:
        if label:
            tp += 1
        else:
            fp += 1
    else:
        if label:
            fn += 1
        else:
            tn += 1


print("ACC : [{:.4f}] REC: [{:.4f}]".format( tp * 1.0 / (tp + fp), tp * 1.0 / (tp + fn) ))
print("TP/FP/TN/FN : [{}][{}][{}][{}]".format(tp, fp, tn, fn))