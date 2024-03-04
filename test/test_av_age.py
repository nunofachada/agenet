"""Tests for the average age of information function."""

import numpy as np
import pytest
from matplotlib import pyplot as plt

from agenet import av_age_fn


# def test_av_age_func_values():
#     assert av_age_func([2,3,4,5], [1,2,3,4]) == 1.3
@pytest.mark.parametrize("v, T, expected", [([2, 3, 4, 5], [1, 2, 3, 4], 1.3)])
def test_av_age_func_values(v, T, expected):
    """Test the av_age_func function."""
    age, _, _ = av_age_fn(v, T, 0.1)
    assert round(age, 1) == expected


@pytest.fixture()
def plot_fn():
    """Fixture to test plotting."""

    def _plot(points):
        plt.plot(points)
        yield plt.show()
        plt.close("all")

    return _plot


def test_plot_fn(plot_fn):
    """Test the plot_fn function."""
    points = [1, 2, 3]
    plot_fn(points)
    assert True


def test_zero_division():
    """Test the zero division error."""
    with pytest.raises(ZeroDivisionError):
        1 / 0


def test_av_age_fn():
    """Test the av_age_fn function."""
    # Define the expected average age of information for the example
    expected_average_age = 1.3
    # Calculate the actual average age of information for the example
    destination_times = [2, 3, 4, 5]
    generation_times = [1, 2, 3, 4]
    lambha = 0.1
    actual_average_age, _, _ = av_age_fn(destination_times, generation_times, lambha)
    # Check that the actual average age of information
    # matches the expected value
    assert np.isclose(actual_average_age, expected_average_age, rtol=1e-1)
