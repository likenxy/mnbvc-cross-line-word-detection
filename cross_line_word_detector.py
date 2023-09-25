import logging
import os

class CrossLineWordDetector:
    def __init__(self, word_dict_path=None, logger=logging.getLogger()) -> None:
        '''
            word_dict_path : 辞典路径，行分割文本
            logger : 日志
        '''
        self.logger = logger
        self.word_set = set()
        if word_dict_path is None:
            word_dict_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'english-words/words_alpha.txt')
        for line in open(word_dict_path).readlines():
            word = line.strip()
            if len(word) == 0 : continue
            self.word_set.add(word)
            self.word_set.add(word.lower())
        self.logger.info('Load words finish, words cound: [{}]'.format(len(self.word_set)))

    def detect(self, part_a, part_b, to_lower=True):
        '''
            part_a : 词组a
            part_b : 词组b
            to_lower : 是否转小写

            返回: True or False 是否可以连成同一个词
        '''
        a = part_a.lower() if to_lower else part_a
        b = part_b.lower() if to_lower else part_b
        part_a_in_flag = (a in self.word_set)
        part_b_in_flag = (b in self.word_set)
        part_merge = a + b
        if a.endswith('-'):
            part_merge = a[:-1] + b
        part_merge_in_flag = (part_merge in self.word_set)
        return part_merge_in_flag or (not part_a_in_flag and not part_b_in_flag)
        