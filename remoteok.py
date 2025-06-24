import requests
import pandas as pd
from datetime import datetime, timedelta

def scrape():
    url = "https://remoteok.com/api"
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers)
    data = response.json()

    keywords = [
        "genai", 
        "gen ai", 
        "generative ai", 
        "large language model", 
        "lead data",
        "data scientist", 
        "machine learning"
    ]
    keywords = [k.lower() for k in keywords]

    blocklist = [
        "ll.m", 
        "ragged", 
        "drag", 
        "language requirement"
    ]

    jobs = []
    cutoff_date = datetime.utcnow() - timedelta(days=20)

    for job in data[1:]:
        try:
            title = job.get("position") or job.get("title", "")
            company = job.get("company", "")
            tags = job.get("tags", [])
            description = job.get("description", "")
            link = job.get("url", "")
            epoch = job.get("epoch")

            if epoch:
                job_date = datetime.utcfromtimestamp(epoch)
                if job_date < cutoff_date:
                    continue
            else:
                continue

            texto = f"{title} {company} {' '.join(tags)} {description}".lower()

            if any(b in texto for b in blocklist):
                continue

            if not any(k in texto for k in keywords):
                continue

            #  Verifica se a vaga ainda está no ar
            try:
                check = requests.get(link, headers=headers)
                if check.status_code == 404:
                    continue
            except:
                continue

            print("🔹 Título:", title)
            print("   Empresa:", company)
            print("   Publicado:", job_date.strftime('%Y-%m-%d'))
            print("   Tags:", ", ".join(tags))
            print("   Link:", link)
            print("-" * 60)

            jobs.append({
                "Título": title,
                "Empresa": company,
                "Tags": ", ".join(tags),
                "Link": link,
                "Publicado em": job_date.strftime('%Y-%m-%d')
            })
        except:
            continue

    df = pd.DataFrame(jobs)
    df.to_csv("vagas_remoteok.csv", index=False)
    print(f"\n {len(jobs)} vagas *ativas e relevantes* dos últimos 20 dias salvas em vagas_remoteok.csv")

scrape()
