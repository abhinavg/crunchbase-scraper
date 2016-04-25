import bs4
import pickle
import sys

from scripts import company_info

def GetInvestments(filename):
  companies = set([])
  with open(filename) as f:
    soup = bs4.BeautifulSoup(f.read())
    for span in soup.find_all('span', class_='profile'):
      link = span.find('a')
      _, _, company = link['href'].rpartition('/')
      companies.add(company)
  return companies

def CompanyInfos(filename):
  companies = GetInvestments(filename)
  company_infos = set([])
  for company in companies:
    info = company_info.GetCompanyInfo(company)
    if info:
      company_infos.add(info)
  return company_infos

if __name__ == '__main__':
  print sys.argv
  filename = sys.argv[1]
  company_infos = CompanyInfos(filename)
  with open(filename.replace('html', 'pickle'), 'w') as info_file:
    pickle.dump(company_infos, info_file)
  print company_infos
  print len(company_infos)