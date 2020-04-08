import os

import pytest
import stripe
from django.contrib.auth import get_user_model

from .models import INTERVAL_CHOICES


@pytest.fixture(scope="module")
def stripe_token():
    stripe.api_key = os.environ["STRIPE_SECRET_KEY"]

    token = stripe.Token.create(
      card={
        'number': '4242424242424242',
        'exp_month': 12,
        'exp_year': 2020,
        'cvc': '123',
      },
    )
    return token


@pytest.mark.django_db
def test_multi_email_donor_view(stripe_token, client):
    """
    Originally CTSDonor objects were checked based on their
    provided receipt email. This could fail if they supplied
    different emails for subsequent donations.
    """
    user_model = get_user_model()
    donor = user_model.objects.create_user(username="Test", email="test@email.com", password="secret")
    assert client.login(username=donor.username, password="secret") is True

    # Test donor using same receipt email as user email
    response = client.post("/fundraising/donate/", {
        "amount": 1,
        "interval": INTERVAL_CHOICES[0][0],
        "receipt_email": donor.email,
        "stripe_token": stripe_token.id,
        "token_type": stripe_token.type,
    })
    assert response.status_code == 200
    assert response.json()["success"] is True
