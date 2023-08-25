import datetime

import pytest
from mainpage.models import Enrollment


@pytest.fixture
def active_enrollment() -> Enrollment:
    now = datetime.datetime.now()
    return Enrollment.objects.create(
        timepad_event_id="123",
        start_date=now + datetime.timedelta(days=3),
        end_date=now + datetime.timedelta(days=10),
        end_registration_date=now + datetime.timedelta(days=1),
        early_price_rub=100,
        late_price_rub=200,
        early_price_date_to=now,
        late_price_date_from=now,
    )
