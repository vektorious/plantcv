import pytest
import cv2
import numpy as np
from plantcv.plantcv import params
from plantcv.plantcv.homology import acute


@pytest.mark.parametrize("win", [0, 5])
def test_acute(win, homology_test_data):
    """Test for PlantCV."""
    params.debug = "plot"
    # Read in test data
    img = cv2.imread(homology_test_data.small_rgb_img)
    mask = cv2.imread(homology_test_data.small_bin_img, -1)
    cnt = homology_test_data.load_composed_contours(homology_test_data.small_composed_contours_file)
    homology_pts = acute(img=img, obj=cnt, mask=mask, win=win, threshold=15)
    assert all([i == j] for i, j in zip(np.shape(homology_pts), (29, 1, 2)))


@pytest.mark.parametrize("obj,win,thresh", [[np.array(([[213, 190]], [[83, 61]], [[149, 246]])), 84, 192],
                                            [np.array(([[103, 154]], [[27, 227]], [[152, 83]])), 35, 0]])
def test_acute_small_contours(obj, win, thresh, homology_test_data):
    """Test for PlantCV."""
    params.debug = "plot"
    # Read in test data
    img = cv2.imread(homology_test_data.small_rgb_img)
    mask = cv2.imread(homology_test_data.small_bin_img, -1)
    homology_pts = acute(img=img, obj=obj, mask=mask, win=win, threshold=thresh)
    assert all([i == j] for i, j in zip(np.shape(homology_pts), (29, 1, 2)))


def test_acute_flipped_contour(homology_test_data):
    """Test for PlantCV."""
    params.debug = None
    # Read in test data
    img = cv2.imread(homology_test_data.small_gray_img, -1)
    mask = cv2.imread(homology_test_data.small_bin_img, -1)
    cnt = homology_test_data.load_composed_contours(homology_test_data.small_composed_contours_file)
    cnt = np.flip(cnt)
    homology_pts = acute(img=img, obj=cnt, mask=mask, win=5, threshold=15)
    assert all([i == j] for i, j in zip(np.shape(homology_pts), (29, 1, 2)))
