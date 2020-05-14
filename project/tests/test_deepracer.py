import math
from src.reward import rwd
import pytest
from tests.params_construct import manyparams, outputs

@pytest.mark.parametrize("par, output", list(zip(manyparams, outputs))) 
def test_inputs(par, output):
    print('\n\nparams: ', par)
    print('\noutput:', output)
    assert rwd(par) == output