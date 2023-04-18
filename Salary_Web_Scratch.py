import requests
from bs4 import BeautifulSoup
import pandas as pd

url= "https://uk.jobted.com/salary"
response= requests.get(url)
response= response.content

soup=BeautifulSoup(response, 'lxml')
block=soup.find_all('div',class_='salary-home-block')[-1]

groups= block.find_all('div',class_='salary-cat-group')

items= soup.find_all('div',class_='salary-cat-item')

itemss=[]
for i in items:
    if i != '':
        itemss.append(i)

heads=[]
header=block.find_all('div',class_='salary-cat-header')
for i in header:
    heads.append(i.get_text())


jobs_list=[]
salary_list=[]
head_list=[]

for group in groups:
    job= group.find_all('a')
    for j in job:
        jobs_list.append(j.get_text())

for group in groups:
    salary= group.find_all('div',class_='salary-cat-item-value')
    for i in salary:
        salary_list.append(i.get_text().replace('/',' ').split()[0])

numbers=[]
for group in groups:
    salary= group.find_all('div',class_='salary-cat-item-value')
    numbers.append(len(salary))

head_list=[c for c, i in zip(heads,numbers) for _ in range(i)]

salary=groups.find_all('div',class_='salary-cat-item-value')
for i in salary:
    print(i.get_text().replace('/',' ').split()[0])


Average_Salary=pd.DataFrame.from_dict(
    {'Job_Sector': head_list,
    'Job_Title': jobs_list,
    'Salary': salary_list}, orient='index').T

Average_Salary.to_csv('Average_Salary.csv')

