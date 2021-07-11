import time

import pytest
from django.contrib.auth import get_user_model
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from .models import Family, Genus, Country


@pytest.fixture(scope='module')
def browser():
    """Provide a selenium webdriver instance."""
    # SetUp
    options = webdriver.FirefoxOptions()

    browser_ = webdriver.Firefox(firefox_options=options)

    yield browser_

    # TearDown
    browser_.quit()


@pytest.fixture()
def country(db):
    country = Country(name='United States of America')
    country.save()
    return country


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
def test_accession_privacy(client, family, genus, country):
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
    response = client.post("/plant-database/add-seed-accession", {
        "col_fname": "User",
        "col_lname": "One",
        "add_collector_count": 1,
        "common_name": "Common name",
        "family": family.name,
        "genus": genus.name,
        "species": "species",
        "variety": "",
        "country": country.pk,
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
        "altitude_unit": 'M',
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


@pytest.mark.django_db
def test_add_seed_accession_requires_login(client):
    user_model = get_user_model()
    user_one = user_model.objects.create_user(username="test_user_one", email="test1@gmail.com", password="test_one")
    response = client.get('/plant-database/add-seed-accession')
    assert response.status_code == 302  # View should redirect to login page
    client.login(username=user_one.username, password="test_one")
    response = client.get('/plant-database/add-seed-accession')
    assert response.status_code == 200
    assert "Accession number:" in str(response.content, encoding='utf-8')


def test_add_seed_accession_form_single_collector(browser, country, live_server):
    """
    Test web form handling of the creation of a new seed accession.
    :return: None
    """
    user_model = get_user_model()
    user_one = user_model.objects.create_user(username="test_user_one", email="test1@gmail.com",
                                              password="test_one")

    browser.get(live_server + '/plant-database/add-seed-accession')
    username_el = browser.find_element_by_id('id_username')
    username_el.send_keys(user_one.username)
    password_el = browser.find_element_by_id('id_password')
    password_el.send_keys('test_one')
    browser.find_element_by_xpath('/html/body/div[2]/div[1]/div[2]/form/button').click()

    col_fname = browser.find_element_by_id('id_col_fname')
    col_lname = browser.find_element_by_id('id_col_lname')
    common_name = browser.find_element_by_id('id_common_name')
    family = browser.find_element_by_id('id_family')
    genus = browser.find_element_by_id('id_genus')
    species = browser.find_element_by_id('id_species')
    variety = browser.find_element_by_id('id_variety')
    country = browser.find_element_by_id('id_country')
    maj_country = browser.find_element_by_id('id_maj_country')
    min_country = browser.find_element_by_id('id_min_country')
    locality = browser.find_element_by_id('id_locality')
    plant_total = browser.find_element_by_id('id_plant_total')
    sample_size = browser.find_element_by_id('id_sample_size')
    percent_flowering = browser.find_element_by_id('id_percent_flowering')
    percent_fruiting = browser.find_element_by_id('id_percent_fruiting')
    storage_location = browser.find_element_by_id('id_storage_location')
    latitude = browser.find_element_by_id('id_latitude')
    longitude = browser.find_element_by_id('id_longitude')
    altitude_unit = browser.find_element_by_id('id_altitude_unit')
    altitude = browser.find_element_by_id('id_altitude')

    submit = browser.find_element_by_id('id_submit')

    col_fname.send_keys('John')
    col_lname.send_keys('Doe')
    common_name.send_keys('marijuana')
    family.send_keys('Cannabaceae')
    genus.send_keys('Cannabis')
    species.send_keys('sativa')
    variety.send_keys('sativa')

    for option in country.find_elements_by_tag_name('option'):
        if option.text == 'United States of America':
            option.click()
            break

    maj_country.send_keys('Colorado')
    min_country.send_keys('El Paso')
    locality.send_keys('Colorado Springs')
    plant_total.send_keys(30)
    sample_size.send_keys(100)
    percent_flowering.send_keys(100)
    percent_fruiting.send_keys(0)
    storage_location.send_keys('Downstairs freezer')
    latitude.send_keys('38.849263')
    longitude.send_keys('-104.825885')
    Select(altitude_unit).select_by_visible_text('Meters')
    altitude.send_keys('1846.58')

    submit.submit()

    time.sleep(1)  # Wait for page to load so page source is correct for next assertion

    assert 'Accession added to database!' in browser.page_source
