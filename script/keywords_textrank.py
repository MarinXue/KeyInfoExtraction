#!/usr/bin/env python3
# coding: utf-8
# File: textrank.py
# Author: lhy<lhy_in_blcu@126.com,https://huangyong.github.io>
# Date: 18-4-17

from collections import defaultdict
import jieba.posseg as pseg
from .textrank import *

class TextRank:
    def __init__(self):
        self.candi_pos = ['n', 'v', 'a']
        self.span = 5

    def extract_keywords(self, text, num_keywords):
        g = textrank_graph()
        cm = defaultdict(int)
        word_list = [[word.word, word.flag] for word in pseg.cut(text)]
        for i, word in enumerate(word_list):
            if word[1][0] in self.candi_pos and len(word[0]) > 1:
                for j in range(i + 1, i + self.span):
                    if j >= len(word_list):
                        break
                    if word_list[j][1][0] not in self.candi_pos or len(word_list[j][0]) < 2:
                        continue
                    pair = tuple((word[0], word_list[j][0]))
                    cm[(pair)] +=  1

        for terms, w in cm.items():
            g.addEdge(terms[0], terms[1], w)
        nodes_rank = g.rank()
        nodes_rank = sorted(nodes_rank.items(), key=lambda asd:asd[1], reverse=True)

        return nodes_rank[:num_keywords]

# def test():
#     text = '''（原标题：央视独家采访：陕西榆林产妇坠楼事件在场人员还原事情经过）
#     央视新闻客户端11月24日消息，2017年8月31日晚，在陕西省榆林市第一医院绥德院区，产妇马茸茸在待产时，从医院五楼坠亡。事发后，医院方面表示，由于家属多次拒绝剖宫产，最终导致产妇难忍疼痛跳楼。但是产妇家属却声称，曾向医生多次提出剖宫产被拒绝。
#     事情经过究竟如何，曾引起舆论纷纷，而随着时间的推移，更多的反思也留给了我们，只有解决了这起事件中暴露出的一些问题，比如患者的医疗选择权，人们对剖宫产和顺产的认识问题等，这样的悲剧才不会再次发生。央视记者找到了等待产妇的家属，主治医生，病区主任，以及当时的两位助产师，一位实习医生，希望通过他们的讲述，更准确地还原事情经过。
#     产妇待产时坠亡，事件有何疑点。公安机关经过调查，排除他杀可能，初步认定马茸茸为跳楼自杀身亡。马茸茸为何会在医院待产期间跳楼身亡，这让所有人的目光都聚焦到了榆林第一医院，这家在当地人心目中数一数二的大医院。
#     就这起事件来说，如何保障患者和家属的知情权，如何让患者和医生能够多一份实质化的沟通？这就需要与之相关的法律法规更加的细化、人性化并且充满温度。用这种温度来消除孕妇对未知的恐惧，来保障医患双方的权益，迎接新生儿平安健康地来到这个世界。'''
#     textranker = TextRank()
#     keywords = textranker.extract_keywords(text, 10)
#
#     for keyword in keywords:
#         print(keyword)
#     '''
#     ('产妇', 1.0)
#     ('医院', 0.5913681024247537)
#     ('家属', 0.5429117450097523)
#     ('事件', 0.5252165334872677)
#     ('剖宫产', 0.4323518137698726)
#     ('患者', 0.42213201850447274)
#     ('榆林', 0.3458613813882902)
#     ('温度', 0.3433894045919456)
#     ('跳楼', 0.3253241303426245)
#     ('事情', 0.30329273312129706)
#     '''
# test()