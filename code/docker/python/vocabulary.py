# -*- coding:utf-8 -*-
# !/usr/bin/python3

from scipy.cluster.vq import *
from numpy import vstack
from numpy import zeros
from numpy import sum
from numpy import log
import sift


class Vocabulary(object):
    """
    Get the Image word vocabulary
    """
    def __init__(self, name):
        """

        """
        self.name = name
        self.voc = []
        self.idf = []
        self.trainingdata = []
        self.nbr_words = 0

    def train(self, featurefiles, k=100, subsampling=10):
        """
        Train image data
        :param featurefiles:
        :param k:
        :param subsampling:
        :return:
        """
        nbr_images = len(featurefiles)
        descr = []
        descr.append(sift.read_features_from_file(featurefiles[0])[1])
        descriptors = descr[0]
        for i in range(1, nbr_images):
            descr.append(sift.read_features_from_file(featurefiles[1])[1])
            descriptors = vstack((descriptors, descr[i]))

        self.voc, description = kmeans(descriptors[::subsampling,:], k, 1)
        self.nbr_words = self.voc.shape[0]

        imwords = zeros((nbr_images, self.nbr_words))
        for i in range(nbr_images):
            imwords[i] = self.project(descr[i])


        nbr_occurences = sum((imwords > 0)*1, axis=0)

        print(nbr_occurences)
        print(nbr_images)
        self.idf = log((1.0*nbr_images) / (1.0 * nbr_occurences))
        self.trainingdata = featurefiles

    def project(self, descriptors):
        """
        Mapping the descriptor to vacabuary and
        Make the histogram
        :param descriptors:
        :return:
        """
        imhist = zeros((self.nbr_words))
        words, distance = vq(descriptors, self.voc)
        for w in words:
            imhist[w] += 1

        return imhist
