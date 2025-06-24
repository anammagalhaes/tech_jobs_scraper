from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

def scrape_indeed_selenium(query="data", location="remote", paginas=3):
    options = Options()
    options.headless = False
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # Filtro antirrobô invisível
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            })
        """
    })

    jobs = []

    for pagina in range(paginas):
        start = pagina * 10
        url = f"https://www.indeed.com/jobs?q={query}&l={location}&start={start}"
        print(f" Acessando: {url}")
        driver.get(url)
        time.sleep(4)

        # Scroll pra ativar o carregamento das vagas
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)

        try:
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CLASS_NAME, "job_seen_beacon"))
            )
            cards = driver.find_elements(By.CLASS_NAME, "job_seen_beacon")
        except Exception as e:
            print(f" Nada encontrado na página {pagina + 1}. Erro: {e}")
            continue

        print(f" Página {pagina + 1} — {len(cards)} vagas")

        for card in cards:
            try:
                title = card.find_element(By.TAG_NAME, "h2").text

                try:
                    company = card.find_element(By.CLASS_NAME, "companyName").text
                except:
                    company = "Desconhecida"

                link_el = card.find_element(By.TAG_NAME, "a")
                link = link_el.get_attribute("href")

                try:
                    date = card.find_element(By.CLASS_NAME, "date").text
                except:
                    date = "Data não encontrada"

                try:
                    desc = card.find_element(By.CLASS_NAME, "job-snippet").text.strip()
                except:
                    desc = "Sem descrição"

                jobs.append({
                    "Título": title,
                    "Empresa": company,
                    "Descrição": desc,
                    "Data": date,
                    "Link": link
                })

            except Exception as e:
                print(f" Erro em uma vaga: {e}")
                continue

        time.sleep(2)

    driver.quit()

    df = pd.DataFrame(jobs)
    df.to_csv("vagas_indeed_selenium.csv", index=False)
    print(f"\n {len(jobs)} vagas salvas em vagas_indeed_selenium.csv com sucesso!")

#  
scrape_indeed_selenium(
    query="data",
    location="remote",
    paginas=3
)



