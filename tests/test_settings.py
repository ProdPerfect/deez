import pytest

from deez.conf import settings


def test_can_access_existing_attributes() -> None:
    assert settings.DEBUG == True


def test_raises_attribute_error_when_attribute_nonexistent() -> None:
    with pytest.raises(AttributeError) as e:
        assert settings.HAMZA

    assert str(e.value) == "'Setting' object has no attribute 'HAMZA'"
