import pytest
from django.contrib.auth import get_user_model

from .models import Family, Genus


@pytest.fixture()
def family(db):
    family = Family(name="Dummae")
    family.save()
    return family


@pytest.fixture()
def genus(family, db):
    genus = Genus(family=family, name="Dummus")
    genus.save()
    return genus


@pytest.mark.django_db
def test_accession_privacy(client, family, genus):
    """
    Test that accession objects are not visible to users other
    than the user who created them.
    """
    user_model = get_user_model()
    user_one = user_model.objects.create_user(username="test_user_one", email="test1@gmail.com", password="test_one")
    user_two = user_model.objects.create_user(username="test_user_two", email="test2@gmail.com", password="test_two")

    # Login as the first test user
    client.login(username=user_one.username, password="test_one")

    # Create a new accession object
    response = client.post("/plant-database/add-accession", {
        "col_fname": "User",
        "col_lname": "One",
        "add_collector_count": 1,
        "common_name": "Common name",
        "family": family.pk,
        "genus": genus.pk,
        "species": "species",
        "variety": "",
        "county": "USA",
        "maj_country": "Utah",
        "min_country": "Salt Lake",
        "locality": "City Creek",
        "plant_total": 100,
        "sample_size": 25,
        "percent_flowering": 10,
        "percent_fruiting": 5,
        "storage_location": "Freezer",
        "latitude": 40.0,
        "longitude": -112.0,
        "altitude": 3800,
        "bank_date": "2019-05-03"
    }, follow=True)

    # Check if the newly created accession is visible to the first test user
    assert response.status_code == 200
    assert "Dummus species" in str(response.content, encoding='utf-8')

    # Login as the second user and make sure the recent accession is not visible
    client.login(username=user_two.username, password="test_two")
    response = client.get("/plant-database", follow=True)
    assert response.status_code == 200
    print(str(response.content, encoding='utf-8'))
    assert "Dummus species" not in str(response.content, encoding='utf-8')
    assert "<p>Your plant database is empty!</p>" in str(response.content, encoding='utf-8')
