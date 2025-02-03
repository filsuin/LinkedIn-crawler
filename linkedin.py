from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import urllib.parse

# Paramètres
LINKEDIN_LOGIN_URL = "https://www.linkedin.com/login"
JOB_SEARCH_URL = "https://www.linkedin.com/jobs/search/?keywords="
OUTPUT_FILE = "offres_linkedin.txt"

# Fonction de connexion
def login_to_linkedin(driver, username, password):
    driver.get(LINKEDIN_LOGIN_URL)
    time.sleep(3)  # Augmenté à 3 secondes
    
    # Vérification de la connexion
    try:
        username_field = driver.find_element(By.ID, "username")
        password_field = driver.find_element(By.ID, "password")
        
        username_field.send_keys(username)
        password_field.send_keys(password, Keys.RETURN)
        time.sleep(7)  # Augmenté à 7 secondes
        
        # Vérifier si la connexion a réussi
        if "feed" in driver.current_url:
            print("✅ Connexion réussie")
        else:
            print("❌ Échec de la connexion")
            
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
        raise

# Fonction de recherche d'offres
def search_jobs(driver, keywords):
    url = JOB_SEARCH_URL + urllib.parse.quote(keywords)
    driver.get(url)
    time.sleep(5)  # Attendre le chargement des résultats
    
    print(f"🔍 Recherche sur: {url}")
    
    job_links = []
    try:
        # Trouver les offres d'emploi
        jobs = driver.find_elements(By.CLASS_NAME, "job-card-container")
        for job in jobs:
            link = job.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
            job_links.append(link)
            
    except Exception as e:
        print(f"❌ Erreur pendant la recherche: {e}")
    
    return job_links

# Fonction principale
def main():
    username = input("Votre email LinkedIn : ")
    password = input("Votre mot de passe LinkedIn : ")
    keywords = input("Entrez les mots-clés de recherche : ")

    # Configuration de Chrome
    options = Options()
    # options.add_argument("--headless")
    
    try:
        # Installation et configuration du driver avec gestion d'erreur
        service = Service()
        driver = webdriver.Chrome(
            service=service,
            options=options
        )
        
        login_to_linkedin(driver, username, password)
        job_links = search_jobs(driver, keywords)

        # Sauvegarde des offres trouvées
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            for link in job_links:
                f.write(link + "\n")
        
        print(f"✅ {len(job_links)} offres trouvées et enregistrées dans {OUTPUT_FILE}")

    except Exception as e:
        print(f"❌ Erreur : {e}")

    finally:
        driver.quit()

if __name__ == "__main__":
    main()
