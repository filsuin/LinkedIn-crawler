from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import urllib.parse
import random
from datetime import datetime

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

def normalize_location(location):
    """Normalise les noms de régions et villes"""
    location_mapping = {
        "idf": "Île-de-France",
        "ile de france": "Île-de-France",
        "ile-de-france": "Île-de-France",
        "région parisienne": "Île-de-France",
        "paris region": "Île-de-France",
        "paca": "Provence-Alpes-Côte d'Azur",
        "aura": "Auvergne-Rhône-Alpes"
    }
    
    location = location.lower().strip()
    return location_mapping.get(location, location)

def verify_location(driver, location):
    """Vérifie si LinkedIn a bien pris en compte la localisation"""
    try:
        time.sleep(3)  # Attendre le chargement des pills
        location_pills = driver.find_elements(By.CLASS_NAME, "search-reusables__pill-button")
        
        if not location_pills:
            return True  # Si pas de pills, on considère que c'est OK
            
        for pill in location_pills:
            pill_text = pill.text.lower()
            if (location.lower() in pill_text or 
                "île-de-france" in pill_text and location.lower() in ["idf", "ile de france", "région parisienne"]):
                return True
        return False
        
    except Exception as e:
        print(f"⚠️ Erreur lors de la vérification de localisation: {e}")
        return True  # En cas d'erreur, on continue

def load_existing_links():
    """Charge les liens existants du fichier"""
    try:
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            return set(line.strip() for line in f if line.strip())
    except FileNotFoundError:
        return set()

def save_new_links(new_links):
    """Ajoute uniquement les nouveaux liens au fichier"""
    existing_links = load_existing_links()
    truly_new_links = set(new_links) - existing_links
    
    if truly_new_links:
        with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
            for link in truly_new_links:
                f.write(f"{link}\n")
        print(f"✅ {len(truly_new_links)} nouvelles offres ajoutées")
    return truly_new_links

def random_delay(min_seconds=2, max_seconds=5):
    """Attend un temps aléatoire entre min_seconds et max_seconds"""
    delay = random.uniform(min_seconds, max_seconds)
    time.sleep(delay)

def search_jobs(driver, query, location):
    normalized_location = normalize_location(location)
    base_url = JOB_SEARCH_URL + urllib.parse.quote(query)
    base_url += f"&location={urllib.parse.quote(normalized_location)}"
    
    driver.get(base_url)
    random_delay(3, 6)  # Délai initial aléatoire

    job_links = set()
    last_height = 0
    scroll_count = 0
    
    while True:
        # Scroll progressif et aléatoire
        current_scroll = random.randint(500, 1000)
        driver.execute_script(f"window.scrollBy(0, {current_scroll});")
        random_delay(1.5, 3)
        
        scroll_count += 1
        if scroll_count % 5 == 0:  # Pause plus longue tous les 5 scrolls
            random_delay(5, 8)
            print("⏳ Pause courte pour éviter les limitations...")
        
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
        
        try:
            new_jobs = driver.find_elements(By.CLASS_NAME, "job-card-container")
            current_batch = set()
            
            for job in new_jobs:
                random_delay(0.5, 1)  # Petit délai entre chaque offre
                link = job.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
                if link not in job_links:
                    current_batch.add(link)
            
            if current_batch:
                save_new_links(current_batch)
                job_links.update(current_batch)
                print(f"📊 Total: {len(job_links)} offres trouvées", end="\r")
                
        except Exception as e:
            print(f"❌ Erreur pendant la recherche: {e}")
            
        if "Aucun autre résultat" in driver.page_source:
            break
            
        # Si plus de 100 offres, pause longue
        if len(job_links) > 0 and len(job_links) % 100 == 0:
            print("\n💤 Pause longue pour éviter les limitations...")
            random_delay(10, 15)
    
    return list(job_links)

# Fonction principale
def main():
    username = input("Votre email LinkedIn : ")
    password = input("Votre mot de passe LinkedIn : ")
    required_keywords = input("Mots-clés OBLIGATOIRES (séparés par espaces) : ")
    optional_keywords = input("Mots-clés OPTIONNELS (séparés par espaces) : ")
    location = input("Lieu de recherche (ville ou pays) OBLIGATOIRE : ")

    if not location.strip():
        print("❌ Le lieu de recherche est obligatoire")
        return
    
    try:
        options = Options()
        options.add_argument("--headless")
        service = Service()
        driver = webdriver.Chrome(service=service, options=options)
        
        login_to_linkedin(driver, username, password)

        required_variations = set()
        optional_variations = set()

        for keyword in required_keywords.split():
            required_variations.update(generate_keyword_variations(keyword))

        for keyword in optional_keywords.split():
            optional_variations.update(generate_keyword_variations(keyword))

        required_base = ' AND '.join(f'"{kw}"' for kw in required_keywords.split())
        
        # Pour chaque mot-clé requis, ajouter ses variations en OR
        variations_queries = []
        for keyword in required_keywords.split():
            variations = generate_keyword_variations(keyword)
            if variations:
                variations_query = ' OR '.join(f'"{v}"' for v in variations)
                variations_queries.append(f"({variations_query})")
        
        # Ajout des mots-clés optionnels
        optional_variations = set()
        for keyword in optional_keywords.split():
            optional_variations.update(generate_keyword_variations(keyword))
        
        # Construction de la requête finale
        final_query = required_base
        if variations_queries:
            final_query += f" AND ({' AND '.join(variations_queries)})"
        if optional_variations:
            optional_query = ' OR '.join(f'"{kw}"' for kw in optional_variations)
            final_query += f" AND ({optional_query})"

        print(f"🔍 Recherche: {final_query}")
        if location:
            print(f"📍 Lieu: {location}")
        
        job_links = search_jobs(driver, final_query, location)
        save_new_links(job_links)
        
    except Exception as e:
        print(f"❌ Erreur : {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
