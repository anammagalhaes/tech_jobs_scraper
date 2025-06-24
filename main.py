
from remoteok import scrape as scrape_remoteok
from ycombinator import scrape as scrape_yc
from turing import scrape as scrape_turing
from wellfound import scrape as scrape_wellfound

def main():
    print(" Buscando vagas no RemoteOK...")
    scrape_remoteok()

    #print("\n Buscando vagas no Y Combinator Jobs...")
    #scrape_yc()

    print("\n Buscando vagas no Turing...")
    scrape_turing()

    #print("\n Buscando vagas no Wellfound...")
    #scrape_wellfound()

if __name__ == "__main__":
    main()
