#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy
import cv2
import random


def basic(image, lessgreater=[0, 255], limiar=127):
    """Apply basic dithering."""
    if len(image.shape) == 2:
        result = numpy.zeros((image.shape[0], image.shape[1]), numpy.uint8)
        for row in range(1, image.shape[0]):
            for column in range(1, image.shape[1]):
                result[row, column] = lessgreater[0] \
                    if image[row, column] <= limiar else lessgreater[1]
    else:
        result = numpy.zeros(
            (image.shape[0], image.shape[1], image.shape[2]), numpy.uint8)
        for row in range(1, image.shape[0]):
            for column in range(1, image.shape[1]):
                for channel in range(0, image.shape[2]):
                    result[row, column, channel] = lessgreater[0] \
                        if image[row, column, channel] <= limiar \
                        else lessgreater[1]
    return result


def aleatory(image, interval=(-100, 0)):
    """Aleatory dithering."""
    if len(image.shape) == 2:
        result = numpy.zeros((image.shape[0], image.shape[1]), numpy.uint8)
        for row in range(1, image.shape[0]):
            for column in range(1, image.shape[1]):
                temp = image[row, column] + \
                    random.randrange(interval[0], interval[1])
                if temp <= 127:
                    result[row, column] = 0
                else:
                    result[row, column] = 255

    else:
        result = numpy.zeros(
            (image.shape[0], image.shape[1], image.shape[2]), numpy.uint8)
        for row in range(1, image.shape[0]):
            for column in range(1, image.shape[1]):
                for channel in range(0, image.shape[2]):
                    temp = image[row, column, channel] + \
                        random.randrange(interval[0], interval[1])
                    if temp <= 127:
                        result[row, column, channel] = 0
                    else:
                        result[row, column, channel] = 255
    return result


def periodic(image):
    """Periodic dithering."""
    if len(image.shape) == 2:
        result = numpy.array(image)
        for row in range(1, image.shape[0]):
            for column in range(1, image.shape[1]):
                i = row % 3
                j = column % 3
                if (image[row, column] > image[i, j]):
                    result[row, column] = 0
                else:
                    result[row, column] = 255
    else:
        result = numpy.zeros((image.shape[0],
                              image.shape[1],
                              image.shape[2]),
                             numpy.uint8)

        for row in range(1, image.shape[0]):
            for column in range(1, image.shape[1]):
                for channel in range(0, image.shape[2]):
                    i = row % 3
                    j = column % 3
                    if (image[row, column, channel] > image[i, j, channel]):
                        result[row, column, channel] = 0
                    else:
                        result[row, column] = 255
    return result


def aperiodic(image):
    """Aperiodic dithering."""
    black = 0
    white = 255
    threshold = (black+white)/2
    if len(image.shape) == 2:
        result = numpy.array(image)
        for row in range(1, image.shape[0]-1):
            for column in range(1, image.shape[1]-1):
                if (image[row, column] < threshold):
                    result[row, column] = black
                else:
                    result[row, column] = white
                error = float(image[row, column]) - float(result[row, column])
                image[row+1, column] += int((3.0/8.0)*error)
                image[row, column+1] += int((3.0/8.0)*error)
                image[row+1, column+1] += int((2.0/8.0)*error)
    return result


def show(image):
    """Show a image untill ENTER key is pressed."""
    cv2.imshow('press ENTER to close', image)
    cv2.waitKey(0)


if (__name__ == '__main__'):
    image = cv2.imread('images/sapo.png', cv2.IMREAD_GRAYSCALE)
    show(periodic(image))
    show(basic(image))
    show(aleatory(image))
    show(periodic(image))
    show(aperiodic(image))
