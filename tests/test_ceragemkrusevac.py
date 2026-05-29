import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.cherome.options import Options

# Konstante

BASE_URL = 'http://ceragemkrusevac.com'

NAV_LINKS = {
    "Naslovna": f"{BASE_URL}/",
    "O Nama":   f"{BASE_URL}/o-nama/",
    "Cenovnik": f"{BASE_URL}/cenovnik/",
    "Galerija": f"{BASE_URL}/galerija/",
    "Kontakt":  f"{BASE_URL}/kontakt/",
}

# URL adrese usluga koje se nude - koristiti u buducim testovima
SERVICE_LINKS = [
    f"{BASE_URL}/ceragem-masaza/",
    f"{BASE_URL}/presoterapija",
    f"{BASE_URL}/kavitacija",
    f"{BASE_URL}/lice",
    f"{BASE_URL}/manikir",
]

@pytest.fixture(scope='module')  # jedan browser za sve testove u ovom fajlu (brze od scope='function')
def driver():
    """Pokrece ChromeDriver i zatvara ga po zavrsetku modula"""
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--window-size=1920,1080')

    drv = webdriver.Chrome(options=chrome_options)
    drv.implicitly_wait(10) # ceka 10 sekundi pre nego sto izbaci gresku
    yield drv # yield (ne return) omogucava da se drv.quit() izvrsi nakon testova
    drv.quit() # zatvara browser nakon sto se svi testovi zavrse

class TestNavigacija:
    """Proverava da li navigacioni meni funkcionise ispravno"""
    # dekorator, koji pokrece test za sve nav linkove iz recnika
    @pytest.mark.parametrize('naziv, url', list(NAV_LINKS.items())) # parametrize ocekuje listu
    def test_nav_linkovi_postoje(self, driver, naziv, url):
        """Svaka stavka menija treba da postojji i vodi na ispravnu URL adresu"""
        driver.get(BASE_URL) # otvaranje url adrese u pregledacu
        links = driver.find_elements(By.CSS_SELECTOR, 'nav a, header a') # trazimo listu pronadjenih elemenata, koristeci CSS selektor
        hrefs = [l.get_attribute('href') for l in links] # za svaki pronadjeni link uzima href vrednost atributa
        assert url in hrefs, f'Nav link {naziv} ({url}) nije pronadjen'

    @pytest.mark.parametrize('naziv, url', list(NAV_LINKS.items()))
    def test_nav_stranice_otvaranje(self, driver, naziv, url):
        """Svaka stranica iz navigacije treba da se ucita sa HTTP 200 (OK)"""
        driver.get(url) # otvara url iz parametrizacije
        # assert sa dva uslova, prolazi ako je bar jedan tacan
        assert driver.current_url.rstrip('/') == url.rstrip('/') or url in driver.current_url, ( # uklanja se "/" sa kraja URL-a radi poredjenja 
            f'Stranica {naziv} nije ucitana. Trenutni URL: {driver.current_url}' # ili se URL nalazi unutar trenutne URL
        )
        assert '404' not in driver.title.lower(), f'Stranica {naziv} vraca 404 (Not Found).' # proverava da 404 nije dostupan u naslovu

    def test_pozovi_nas_dugme(self, driver):
        """Pozovi Nas dugme treba da postoji"""
        driver.get(BASE_URL)
        tel_link = driver.find_element(By.CSS_SELECTOR, "a[href^='tel:']") # trazi prvi element koji odgovara selektoru, a ciji href pocinje ^=
        assert tel_link is not None, 'Telefon link nije pronadjen'
        assert tel_link.is_displayed(), 'Pozovi Nas dugme nije vidljivo' # proverava da li je element vidljiv korisniku
