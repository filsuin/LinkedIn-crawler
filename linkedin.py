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

def generate_keyword_variations(keyword):
    variations = set()
    
    # Variations de base
    variations.add(keyword.lower())
    variations.add(keyword.capitalize())
    variations.add(keyword.upper())
    
    # Variations avec tirets et espaces
    if ' ' in keyword:
        # Mot composé avec espace
        no_space = keyword.replace(' ', '')
        with_hyphen = keyword.replace(' ', '-')
        variations.update([no_space, with_hyphen])
    
    if '-' in keyword:
        # Mot composé avec tiret
        no_hyphen = keyword.replace('-', '')
        with_space = keyword.replace('-', ' ')
        variations.update([no_hyphen, with_space])
    
    # Variations courantes en français/anglais
    common_variations = {
        'cyber': ['cybersecurity', 'cyber security', 'cyber-security', 'cybersécurité', 'cyber sécurité'],
        'développeur': ['developer', 'dev', 'developpeur'],
        'sécurité': ['security', 'securite'],
        'système': ['system', 'systeme'],
        'réseau': ['network', 'reseaux'],
        'fullstack': ['full stack', 'full-stack'],
        'backend': ['back end', 'back-end'],
        'frontend': ['front end', 'front-end'],
        'javascript': ['js'],
        'typescript': ['ts'],
        'python': ['py'],
        'manager': ['management', 'manageur'],
        'senior': ['sr', 'sr.'],
        'junior': ['jr', 'jr.'],
        'ingénieur': ['engineer', 'ingenieur'],
    }
    
    # Ajouter les variations courantes si le mot-clé est dans le dictionnaire
    for base_word, word_variations in common_variations.items():
        if base_word in keyword.lower():
            variations.update(word_variations)
    
    return variations

def search_jobs(driver, keywords_input):
    base_keywords = keywords_input.split()
    all_keywords = set()
    
    for keyword in base_keywords:
        variations = generate_keyword_variations(keyword)
        all_keywords.update(variations)
    
    print(f"📝 Variations générées: {', '.join(all_keywords)}")
    
    # Construire la requête OR pour LinkedIn
    search_query = ' OR '.join(f'"{kw}"' for kw in all_keywords)
    url = JOB_SEARCH_URL + urllib.parse.quote(search_query)
    
    print(f"🔍 Recherche avec les mots-clés: {', '.join(all_keywords)}")
    
    driver.get(url)
    time.sleep(5)
    
    job_links = []
    try:
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
    keywords = input("Entrez les mots-clés séparés par des espaces : ")

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
