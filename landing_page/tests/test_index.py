import pytest
from django.test import Client


@pytest.mark.django_db
def test__index__shows_up(client: Client) -> None:
    response = client.get('/')
    assert response.status_code == 200
