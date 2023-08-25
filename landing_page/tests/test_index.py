import pytest
from django.test import Client
from mainpage.models import Enrollment


@pytest.mark.django_db
def test__index__shows_up(client: Client, active_enrollment: Enrollment) -> None:
    response = client.get('/')
    assert response.status_code == 200
