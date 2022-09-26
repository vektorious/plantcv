import pytest
import numpy as np
from plantcv.plantcv.hyperspectral import read_data, _parse_arcgis


def test_read_data_default(hyperspectral_test_data):
    """Test for PlantCV."""
    array_data = read_data(filename=hyperspectral_test_data.envi_bil_file)
    assert np.shape(array_data.array_data) == (1, 1600, 978)


def test_read_data_default_bands(hyperspectral_test_data):
    """Test for PlantCV."""
    array_data = read_data(filename=hyperspectral_test_data.envi_no_default)
    assert np.shape(array_data.array_data) == (1, 1600, 978)


def test_read_data_approx_pseudorgb(hyperspectral_test_data):
    """Test for PlantCV."""
    array_data = read_data(filename=hyperspectral_test_data.envi_appox_pseudo)
    assert np.shape(array_data.array_data) == (1, 1600, 978)


def test_read_data_bad_interleave(hyperspectral_test_data):
    """Test for PlantCV."""
    with pytest.raises(RuntimeError):
        _ = read_data(filename=hyperspectral_test_data.envi_bad_interleave)


def test_read_data_bad_filename(hyperspectral_test_data):
    """Test for PlantCV."""
    with pytest.raises(RuntimeError):
        _ = read_data(filename=hyperspectral_test_data.bad_filename)


def test_read_data_parse_arcgis(hyperspectral_test_data):
    """Test for PlantCV."""
    header_dict, wavelength_dict = _parse_arcgis(headername=hyperspectral_test_data.arcgis_hdr)
    assert len(wavelength_dict) == len(header_dict["wavelength"])
