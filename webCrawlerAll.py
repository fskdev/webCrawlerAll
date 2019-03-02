from bs4 import BeautifulSoup
import requests, datetime

global sitesAcessados
sitesAcessados = 0
linkAvaliar = input("Insira o link inicial: ")


def extract_title(content):
    soup = BeautifulSoup(content, "lxml")
    tag = soup.find("title", text=True)

    if not tag:
        return None
    
    return tag.string.strip()

def extract_links(content):
    soup = BeautifulSoup(content, "lxml")
    links = set()

    for tag in soup.find_all("a", href=True):
        if tag["href"].startswith("http"):
            links.add(tag["href"])

    return links

def crawl(start_url):
    seen_urls = set([start_url])
    available_urls = set([start_url])

    while available_urls:
        global sitesAcessados
        url = available_urls.pop()

        try:
            content = requests.get(url, timeout=1).text

        except Exception:
            continue

        title = extract_title(content)

        if title:
            print("\n")
            print(title)
            print(url)
            print("\n")
            sitesAcessados+=1

        for link in extract_links(content):
            if link not in seen_urls:
                seen_urls.add(link)
                available_urls.add(link)


try:
    dataAtual = datetime.datetime.now()
    global horaIniciado
    horaIniciado = dataAtual.hour
    crawl(linkAvaliar)


except KeyboardInterrupt:
    dataAtual2 = datetime.datetime.now()
    horaAtual = dataAtual2.hour
    horasUsadas = horaAtual - horaIniciado
    print()
    print("\n\nParando....")
    print("\n<<  Estatisticas da sessao  >>\n")
    print("Sites acessados: {}".format(sitesAcessados))
    print("\n{} sites acessados em {} hora(s)".format(sitesAcessados, float(horasUsadas)))
    input("\n\nAperte ENTER para fechar o programa.")