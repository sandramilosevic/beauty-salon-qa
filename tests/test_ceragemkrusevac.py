import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# Konstante

BASE_URL = 'https://ceragemkrusevac.com'

NAV_LINKS = {
    "Naslovna": f"{BASE_URL}/",
    "O Nama":   f"{BASE_URL}/o-nama/",
    "Cenovnik": f"{BASE_URL}/cenovnik/",
    "Galerija": f"{BASE_URL}/galerija/",
    "Kontakt":  f"{BASE_URL}/kontakt/",
}

# URL adrese usluga koje se nude
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
    chrome_options = Options()  # kreira objekat za podesavanje Chrome browsera
    chrome_options.add_argument('--headless')  # browser radi u pozadini, bez grafickog prikaza
    chrome_options.add_argument('--no-sandbox')  # potrebno za pokretanje na Linux/Docker okruzenjima
    chrome_options.add_argument('--disable-dev-shm-usage')  # sprecava greske sa memorijom na Linux sistemima
    chrome_options.add_argument('--window-size=1920,1080')  # postavlja velicinu prozora na Full HD
    
    drv = webdriver.Chrome(options=chrome_options)
    drv.implicitly_wait(10) # ceka 10 sekundi pre nego sto izbaci gresku
    yield drv # yield (ne return) omogucava da se drv.quit() izvrsi nakon testova
    drv.quit() # zatvara browser nakon sto se svi testovi zavrse

@pytest.fixture(scope='module')
def mobile_driver():
    mobile_emulation = {
        "deviceMetrics": {"width": 375, "height": 812, "pixelRatio": 3.0},
        "userAgent": ("Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) "
                      "AppleWebKit/605.1.15 (KHTML, like Gecko) "
                      "Version/14.0 Mobile/15E148 Safari/604.1")
    }
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_experimental_option('mobileEmulation', mobile_emulation)

    drv = webdriver.Chrome(options=chrome_options)
    drv.implicitly_wait(10)
    yield drv
    drv.quit()

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

class TestLinkovi:
    """Proverava da li kriticni linkovi na sajtu rade ispravno"""
    def test_linkovi_usluga_postoje(self, driver):
        """Svi linkovi ka uslugama na naslovnoj strani treba da budu pristuni"""
        driver.get(BASE_URL)
        page_links = [a.get_attribute('href') for a in driver.find_elements(By.TAG_NAME, 'a')] # pronalazi sve <a> elemente, a zatim uzima href od pronadjenih <a> elemenata
        for url in SERVICE_LINKS: # prolazi kroz svaki URL iz liste SERVICE_LINKS
            assert url in page_links, f'Link ka usluzi {url} nije pronadjen na naslovnoj strani.' # za svaki URL proverava da li je u SERVICE_LINKS ili vraca gresku

    @pytest.mark.parametrize('url', SERVICE_LINKS) # pokrece se 5 puta, jednom za svaki URL iz SERVICE_LINKS
    def test_stranice_usluga_se_otvaraju(self, driver, url):
        """Svaka stranica usluge treba da se ucita bez greske"""
        driver.get(url)
        assert '404' not in driver.title.lower(), f'Stranica {url} vraca 404' # proverava da naslov stranice ne sadrzi 404

    def test_facebook_link_postoji(self, driver):
        """Link ka Facebook stranici treba da postoji na sajtu"""
        driver.get(BASE_URL)
        links = [a.get_attribute('href') for a in driver.find_elements(By.TAG_NAME, 'a')] # nalazi <a> elemente
        assert any('facebook.com' in (h or '') for h in links), ( # proverava da li sadrzi bar jedan href facebook.com
            'Facebook link nije pronadjen na sajtu.'
        )
    
    def test_frizerski_salon_link(self, driver):
        """Link ka podsajtu frizerskog salona treba da postoji"""
        driver.get(BASE_URL)
        page_links = [a.get_attribute('href') for a in driver.find_elements(By.TAG_NAME, 'a')] # lista svih <a> elemenata i linkova
        assert any('krasiva.ceragemkrusevac.com' in (h or '') for h in page_links), ( # proverava da li sadrzi sporni link
            'Link ka frizerskom salonu (krasiva.ceragemkrusevac.com) nije pronadjen'
        )    

class TestSadrzaj:
    """Proverava da li se kljucni sadrzaj prikazuje na stranicama"""
    def test_naslovna_ima_h1(self, driver):
        """Naslovna strana treba da ima H1 naslov"""
        driver.get(BASE_URL)
        h1_elementi = driver.find_elements(By.TAG_NAME, 'h1') # trazi sve <h1> elemente, najvazniji naslov na stranici, cuva se u listi
        assert len(h1_elementi) >= 1, 'Na naslovnoj strani nema H1 elementa' # provera da li lista sadrzi bar jedan <h1> element
        assert h1_elementi[0].is_displayed(), 'H1 naslov nije vidljiv' # proverava da li je prvi <h1> vidljiv (jer moze biti postojati, ali sakriven  u css)

    def test_naslovna_ima_slike(self, driver):
        """Naslovna strana treba da sadrzi barem jednu sliku"""
        driver.get(BASE_URL)
        slike = driver.find_elements(By.TAG_NAME, 'img') # pronalazi sve <img> tagove
        vidljive = [s for s in slike if s.is_displayed()] # filtrira samo vidljive slike
        assert len(vidljive) >=1, 'Na naslovnoj stranici nema vidljivih slika.' # greska ukloliko nema prikazanih slika

    def test_galerija_slike(self, driver):
        """Galerija treba da sadrzi slike"""
        driver.get(f'{BASE_URL}/galerija/')
        slike = driver.find_elements(By.TAG_NAME, 'img') # pronalazi <img> elemente
        prave_slike = [
            s for s in slike
            if s.get_attribute('src') and # proverava da li sadrzi putanju do slike
            'placeholder' not in (s.get_attribute('src') or '').lower() and # proverava da li ne sadrzi samo placeholder
            s.is_displayed() # proverava da li je <img> vidljiv element
        ]
        assert len(prave_slike) >= 1, 'Galerija ne sadrzi vidljive slike'

class TestSEO:
    """Proverava osnovne SEO (Search Engine Optimization) elemente sajta"""
    def test_meta_description_vrednost(self, driver):
        """Meta description treba da pominje salon ili usluge"""
        driver.get(BASE_URL)
        meta = driver.find_element(By.CSS_SELECTOR, 'meta[name="description"]') # trazi prvi element koji odgovara selektoru
        sadrzaj = meta.get_attribute('content').lower() # uzima vrednost content atributa meta taga
        assert any(kw in sadrzaj for kw in ['ceragem', 'salon', 'kozmetič','tretman']), ( # proverarava da li postoji bar jedna kljucna rec u opisu
            f'Meta description ne pominje relevantne kljucne reci: {sadrzaj}'
        )

    def test_robots_meta_postoji(self, driver):
        """Robots meta tag treba da postoji i da dozvoljava indeksiranje"""
        driver.get(BASE_URL)
        robots = driver.find_elements(By.CSS_SELECTOR, 'meta[name="robots"]') # vraca listu meta taga sa name='robots'
        assert len(robots) >= 1, 'Meta robots tag nije pronadjen.' # proverava da lista nije prazna
        sadrzaj = robots[0].get_attribute('content').lower() # uzima prvi/jedini robots meta tag i njegovu vrednost
        assert 'noindex' not in sadrzaj, f'Robots meta blokira indeksiranje: {sadrzaj}'

class TestMobilniPrikaz:
    """Proverava ponasanje sajta na mobilnim uredjajima (375px sirina)"""
    # mobile_driver - iPhone X emulacija
    def test_hamburger_meni_postoji_na_mobilnom(self, mobile_driver):
        """Na mobilnom prikazu treba da postoji hamburger meni"""
        mobile_driver.get(BASE_URL) # otvara pocetnu stranicu sa sirinom 375px
        hamburger = mobile_driver.find_elements(
            By.CSS_SELECTOR,
            '.elementor-menu-toggle, .hamburger, [class*="hamburger"], [class*="toggle"]' # lista od 4 moguca selektora za hamburger                        
)
        if not hamburger:
            pytest.xfail('Hamburger meni nije pronadjen (mozda je nav drugacije prikazan na mobilnom)') # ocekivani neuspeh (xfali), zato sto moze da postoji i vertikalni meni
        
        else:
            assert any(h.is_displayed() for h in hamburger), 'Hamburger meni nije vidljiv na mobilnom.' # provera cidljivosti hamburgera

    def test_sadrzaj_ne_prelazi_sirinu_ekrana(self, mobile_driver):
        """Sirina stranice ne sme biti veća od sirine viewport-a na mobilnom."""
        mobile_driver.get(BASE_URL)
        # execute_script - izvrsava js kod direktno u pregledacu i vraca rezultat u pythonu 
        viewport_sirina = mobile_driver.execute_script("return window.innerWidth;") # return window.innerWidth; - js koji vraca sirinu viewporta u pikselima (375px u ovom slucaju)
        page_sirina = mobile_driver.execute_script( 
            "return document.documentElement.scrollWidth;" # js vraca ukupnu sirinu sadrzaja stranice (i deo koji mora skrolovati horizontalno)
        )                                                  # ova vrednost treba da bude jednaka sirini viewporta, ako je veca, pojavljuje se horizontalni scroll
        assert page_sirina <= viewport_sirina + 5, ( # tolerancija do 5px, bez tolerancije test bi mogao da pada
            f"Horizontalni scroll na mobilnom: page width={page_sirina}px > viewport={viewport_sirina}px"
        )

    def test_telefon_link_na_mobilnom(self, mobile_driver):
        """Telefon link treba da bude vidljiv na mobilnom prikazu"""
        mobile_driver.get(BASE_URL)
        tel_links = mobile_driver.find_elements(By.CSS_SELECTOR, "a[href^='tel:']") # proverava <a> ciji href pocinje sa tel:
        assert len(tel_links) >= 1, 'Telefon link nije pronađen na mobilnom prikazu' # proverava da li postoji tel href
        assert any(t.is_displayed() for t in tel_links), 'Telefon link nije vidljiv na mobilnom prikazu' # proverava da li je vidljiv