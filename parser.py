import requests
import csv
from bs4 import BeautifulSoup as bs


headers = {
    'accept': '*/*',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'
}

base_url = 'https://izhevsk.hh.ru/search/vacancy?L_is_autosearch=false&area=96&clusters=true&enable_snippets=true&search_period=30&text=python&page=1'

def hh_parse(base_url, headers):
    jobs = []
    urls = []
    urls.append(base_url)
    session = requests.Session()
    request = session.get(base_url, headers = headers)
    if request.status_code == 200:
        soup = bs(request.content, 'lxml')
        try:
            pagination = soup.find_all('a', attrs={'data-qa': 'pager-page'})
            count = int(pagination[-1].text)
            for i in range(count):
                url = f'https://izhevsk.hh.ru/search/vacancy?L_is_autosearch=false&area=96&clusters=true&enable_snippets=true&search_period=30&text=python&page={i}'
                if url not in urls:
                    urls.append(url)   
        except:
            pass
    for url in urls:
        request = session.get(url, headers = headers)
        soup = bs(request.content, 'lxml')
        divs = soup.find_all('div' , attrs={'data-qa': 'vacancy-serp__vacancy'})
        for div in divs:
            try:
                title = div.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-title'}).text
                href = div.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-title'})['href']
                company = div.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-employer'}).text
                text1 = div.find('div', attrs={'data-qa': 'vacancy-serp__vacancy_snippet_responsibility'}).text
                text2 = div.find('div', attrs={'data-qa': 'vacancy-serp__vacancy_snippet_requirement'}).text
                content = text1 + ' ' + text2
                jobs.append({
                'title': title,
                'href' : href,
                'company': company,
                'content': content
                })
            except:
                pass
        print (len(jobs))
           
         
    else:
        print('Error or Done')
    return jobs
def files_writer(jobs):
    with open('parsed_jobs.csv', 'w') as file:
        pen = csv.writer(file)
        pen.writerow((['Название вакансии', 'URL', 'Название компании', 'Описание']))
        for job in jobs:
            pen.writerow(([job['title'], job['href'], job['company'], job['content']]))
jobs = hh_parse(base_url, headers)
files_writer(jobs)