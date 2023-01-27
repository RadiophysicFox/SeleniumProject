import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_show_all_pets(authorization):
    # Проверяем, что мы оказались на главной странице пользователя
    assert pytest.driver.find_element_by_tag_name('h1').text == "PetFriends"

    # Задаём неявное ожидание
    pytest.driver.implicitly_wait(10)
    images = pytest.driver.find_elements_by_css_selector('.card-deck .card-img-top')
    names = pytest.driver.find_elements_by_css_selector('.card-deck .card-title')
    descriptions = pytest.driver.find_elements_by_css_selector('.card-deck .card-text')

    for i in range(len(names)):
        assert images[i].get_attribute('src') != ''
        assert names[i].text != ''
        assert descriptions[i].text != ''
        parts = descriptions[i].text.split(", ")
        assert len(parts[0]) > 0
        assert len(parts[1]) > 0


def test_check_my_pets(authorization):
    # Переходим на страницу со своим списком питомцев с явным ожиданием элемента "Мои питомцы"
    link_mypets = WebDriverWait(pytest.driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//*[@id=\"navbarNav\"]/ul/li[1]/a")))
    link_mypets.click()
    # Проверяем, что мы оказались на странице пользователя
    assert pytest.driver.find_element_by_tag_name('h2').text == "Friday"

    profile_info = pytest.driver.find_elements_by_xpath('//div[@class=".col-sm-4 left"]')
    WebDriverWait(pytest.driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "tbody tr")))
    rows = pytest.driver.find_elements_by_css_selector('tbody tr')
    WebDriverWait(pytest.driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "tbody tr th img")))
    images = pytest.driver.find_elements_by_css_selector('tbody tr th img')
    WebDriverWait(pytest.driver, 5).until(
        EC.presence_of_element_located((By.XPATH, "//table/tbody/tr/td[1]")))
    name = pytest.driver.find_elements_by_xpath('//table/tbody/tr/td[1]')
    WebDriverWait(pytest.driver, 5).until(
        EC.presence_of_element_located((By.XPATH, "//table/tbody/tr/td[2]")))
    kind = pytest.driver.find_elements_by_xpath('//table/tbody/tr/td[2]')
    WebDriverWait(pytest.driver, 5).until(
        EC.presence_of_element_located((By.XPATH, "//table/tbody/tr/td[3]")))
    age = pytest.driver.find_elements_by_xpath('//table/tbody/tr/td[3]')

    # Достаём количество питомцев
    pets_quantity = (list(profile_info[0].text.split("\n")))[1]
    quantity = int((str(pets_quantity).split(" "))[1])

    # Проверяем что количество питомцев в профиле равно количеству строк в таблице
    assert quantity == len(rows)

    # Запускаем счётчик для подсчёта питомцев с фото и проверяем что у всех питомцев есть имя, возраст и порода
    s = 0
    for i in range(len(images)):
        if images[i].get_attribute('src') != '':
            s += 1
        assert name[i].text != ''
        assert kind[i].text != ''
        assert age[i].text != ''

    # Проверяем что хотя бы у половины питомцев в профиле есть фото
    assert s >= int(quantity)/2

    # Создаём список с именами питомцев и проверяем что нет одинаковых имён
    name_list = []
    for j in range(len(name)):
        name_list.append(name[j].text)
    assert len(name_list) == len(set(name_list))

    # Проверяем что в списке нет повторяющихся питомцев
    first_row = []
    second_row = []
    for k in range(len(name)-1):
        for m in range(k+1, len(name)):
            first_row.append(name[k].text)
            first_row.append(kind[k].text)
            first_row.append(age[k].text)
            second_row.append(name[m].text)
            second_row.append(kind[m].text)
            second_row.append(age[m].text)
            assert set(first_row) != set(second_row)
            first_row.clear()
            second_row.clear()
