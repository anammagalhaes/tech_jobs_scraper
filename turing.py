from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

def scrape():
    url = "https://careers.turing.com/"

    options = Options()
    options.headless = False  # Mantenha False para debug
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    driver.get(url)
    time.sleep(3)

    # Faz scroll até o final da página pra forçar o carregamento das vagas
    last_height = driver.execute_script("return document.body.scrollHeight")
    for _ in range(3):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    try:
        # Espera por links com "/role/" que identificam as vagas
        job_elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//a[contains(@href, '/role/')]"))
        )
    except Exception as e:
        print(" Ainda não encontrou vagas. Vamos imprimir parte do HTML pra investigar:")
        print(driver.page_source[:1500])
        driver.quit()
        return

    jobs = []
    for job in job_elements:
        try:
            title = job.find_element(By.TAG_NAME, "p").text
            link = job.get_attribute("href")
            jobs.append({
                "Título": title,
                "Link": link
            })
        except Exception as e:
            print(f"Erro ao processar uma vaga: {e}")
            continue

    driver.quit()

    if jobs:
        df = pd.DataFrame(jobs)
        df.to_csv("vagas_turing.csv", index=False)
        print(f" {len(jobs)} vagas salvas em vagas_turing.csv")
    else:
        print(" Nenhuma vaga extraída.")

scrape()
