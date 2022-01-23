from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unittest


user_email = "kseniakireeva+eobuwie@gmail.com"
user_password = "uPEsC%d7Sp#8E6K"
logout_btn_loc = "//a[@href='https://www.eobuwie.com.pl/customer/account/logout/']"
search_form_loc = '//*[@id="top"]/body/header/div[4]/div[1]/form/input'
search_form_item1 = "WL373CP2 Beżowy"
search_button = '//*[@id="top"]/body/header/div[4]/div[1]/form/button[1]'


class eobuwieTests(unittest.TestCase):
    def setUp(self):
        # Warunki wstępne
        # Otwarcie przeglądarki
        self.driver = webdriver.Chrome()
        # Pobierz (otwórz) stronę główną
        self.driver.get("https://www.eobuwie.com.pl/")
        # Maksymalizacja okna
        self.driver.maximize_window()

    def tearDown(self):
        # "Sprzątanie" po teście
        # Zamknięcie przeglądarki
        self.driver.quit()

    def testAddToCart(self):
        # Test
        driver = self.driver

        # Akceptacja cookies
        driver.find_element_by_xpath('//button[@data-testid="permission-popup-accept"]').click()

        # Explicit Wait for Login button
        wait = WebDriverWait(driver, 10)
        wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@data-testid="header-link-login"]'))).click()

        # Enter email
        email = driver.find_element_by_xpath('//input[@data-testid="login-input-email"]')
        email.send_keys(user_email)
        # Enter password
        password = driver.find_element_by_xpath('//input[@data-testid="login-input-password"]')
        password.send_keys(user_password)

        # Click login
        click_login = driver.find_element_by_xpath('//button[@data-testid="login-submit-button"]')
        click_login.click()

        # Test czy jestes zalogowany
        wait.until(EC.element_to_be_clickable((By.XPATH, logout_btn_loc)))
        logout_btn = driver.find_element(By.XPATH, logout_btn_loc)
        if logout_btn.is_displayed():
            print("Login PASS")
        else:
            raise Exception("User is not logged in")

        # Add first item
        driver = self.driver
        wait = WebDriverWait(driver, 10)

        # Znajdz forme do wyszukiwania
        search_form = driver.find_element(By.XPATH, search_form_loc)

        # Wpisz co chcesz wyszukac i nacisnij przycisk wyszukiwania
        search_form.send_keys(search_form_item1)
        start_search = driver.find_element(By.XPATH, search_button)
        start_search.click()

        # Zaczekaj az element bedzie widoczny na stronie. Nastepnie kliknij w produkt i wybierz rozmiar butow
        wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@class='products-list__link']")))
        driver.find_element(By.XPATH, "//*[@class='products-list__link']").click()
        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'e-size-picker__select')))
        driver.find_element(By.CLASS_NAME, 'e-size-picker__select').click()

        wait.until(EC.visibility_of_element_located(
            (By.XPATH, "//*[@class='sidebar__heading-text' and normalize-space()='Wybierz rozmiar']")))

        size_select = driver.find_element(
            By.XPATH, "//*[@class='e-size-picker-option__label' and normalize-space()='38']")
        size_select.click()

        # Dodaj buty do koszyka
        add_to_cart = driver.find_element(By.XPATH, '//button[@data-testid="product-add-to-cart-button"]')
        add_to_cart.click()

        # Zaczekaj na element i kliknij w Kontynuuj zakupy
        wait.until(EC.visibility_of_element_located(
            (By.XPATH, "//*[@type='button' and normalize-space()='Kontynuuj zakupy']")))
        continue_purchasing = driver.find_element(By.XPATH,
                                                  "//*[@type='button' and normalize-space()='Kontynuuj zakupy']")
        continue_purchasing.click()

        # Wejdz do koszyka
        driver.find_element(By.CLASS_NAME, 'e-header-cart-button__text').click()

        # Sprawdz czy buty w koszyku sa te same co wyszukiwalismy

        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'products')))

        cart_item1 = driver.find_element(
            By.XPATH, "//*[@class='cart-item__name-second' and normalize-space()='WL373CP2 Beżowy']").text
        self.assertEqual(cart_item1, search_form_item1, "WL373CP2 is not added to the cart")
