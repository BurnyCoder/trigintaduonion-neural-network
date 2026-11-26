"""Verify that the animated counterfactual represents an actual bundle exchange."""
import numpy as np
import pytest

from trig32.movie import exchanged_objects


def test_identify_pure_reading_exchange():
    original = np.array([-.31, 1.8, .27, -.8])
    assert exchanged_objects(original, original[[0, 3, 2, 1]]) == (1, 3)
    with pytest.raises(ValueError):
        exchanged_objects(original, original + .1)
    with pytest.raises(ValueError):
        exchanged_objects(original, np.array([-.31, .9, .27, -.2]))
