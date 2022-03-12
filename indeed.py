import requests
from bs4 import BeautifulSoup
import csv

location = 'india'
keyword = 'solar'
total_jobs = 100
def make_request():
    page_no = 00
    links = []
    while True:
        try:
            if(len(links)<=total_jobs):
                url = f'https://in.indeed.com/jobs?q={keyword}&l={location}&start={page_no}'
                res = requests.get(url)
                soup = BeautifulSoup(res.content, 'lxml')
                td_tag = soup.find('div', id = 'mosaic-zone-jobcards' , class_= 'mosaic-zone')
                a_tags = td_tag.find_all('a', rel = 'nofollow' , target='_blank')
                for a_tag in a_tags:
                    links.append('https://in.indeed.com'+a_tag['href'])
                page_no = page_no +10
            else:
                break
        except Exception as e:
            #print(e)
            break
    return links

def get_data(urls):
    csvFile = open('indeed.csv', mode='w', encoding='utf-8')
    try:
        writer = csv.writer(csvFile)
        #columns names
        writer.writerow(('Sr','Job Title', 'Company Name','Salary','Location','Job Url'))
        
        for i in range(0,total_jobs):
            sr_no = str(i+1)
            job_url = urls[i]
            job_title = "Not Available"
            company_name = "Not Available"
            location = "Not Available"
            salary = "Not Available"
            res = requests.get(urls[i])
            soup = BeautifulSoup(res.content, 'lxml')
            top_card = soup.find('div', class_='jobsearch-DesktopStickyContainer')
            job_title_tag = top_card.find('div',class_='jobsearch-JobInfoHeader-title-container')
            other_info = top_card.find('div' , class_='icl-u-xs-mt--xs icl-u-textColor--secondary jobsearch-JobInfoHeader-subtitle jobsearch-DesktopStickyContainer-subtitle')
            divs_tags = other_info.find_all('div',class_='')
            salary_tag = top_card.find('div',class_='jobsearch-JobMetadataHeader-item')

            if(job_title_tag != None):
                job_title = job_title_tag.text
            if(divs_tags[0]!=None):
                company_name = divs_tags[0].text
            if(divs_tags[2]!=None):
                location = divs_tags[2].text
            if(salary_tag != None):
                salary = salary_tag.text
                
            print("Sr No: "+sr_no)
            print("Job Url: " + job_url)
            print('Job Title:'+ job_title)
            print('Company Name:' +company_name)
            print('Location:' + location)
            print("Salary: "+salary)
            print(" ")
            writer.writerow((sr_no,job_title,company_name,salary,location,job_url))
            i = i+1
            
    except Exception as e:
        print(e)
        
    finally:
        csvFile.close()
    
def main():
    links = make_request()
    get_data(links)

if __name__ == '__main__':
    main()