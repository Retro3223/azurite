import pytest


@pytest.fixture(scope='function')
def motors():
    import frc3223_azurite.motors
    return frc3223_azurite.motors


@pytest.fixture(scope='function')
def conversions():
    import frc3223_azurite.conversions
    return frc3223_azurite.conversions
