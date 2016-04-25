import bs4
import requests
import collections
import sys

OVERVIEW_FIELDS = ['founders', 'categories', 'headquarters', 'founded',
                   'funding', 'description', 'ipo', 'stock', 'status']

FundingRound = collections.namedtuple(
  'FundingRound',
  ['type', 'amount', 'date', 'investors']
)

CompanyInfo = collections.namedtuple(
  'CompanyInfo',
  OVERVIEW_FIELDS + ['name', 'funding_rounds']
)

def GetCompanyInfo(company):
  print company
  url = 'http://www.crunchbase.com/organization/%s' % company
  req = requests.get(url)
  soup = bs4.BeautifulSoup(req.text)
  overview = GetOverview(soup)
  print overview
  if not overview:
    return None
  detailed_desc = soup.find(id='description').get_text()
  funding_rounds = GetFundingRounds(soup)
  print funding_rounds
  return CompanyInfo(name=company, funding_rounds=frozenset(funding_rounds), **overview)

def GetOverview(soup):
  overview_soup = soup.find('div', class_='definition-list-container')
  if not overview_soup:
    return None
  assert overview_soup
  overview_dl = overview_soup.contents[0]
  assert len(overview_dl) % 2 == 0
  overview = {field: '' for field in OVERVIEW_FIELDS}
  for dt, dd in zip(overview_dl.contents[::2], overview_dl.contents[1::2]):
    assert dt.name == 'dt'
    assert dd.name == 'dd'
    overview[dt.get_text()[:-1].lower()] = dd.get_text()
  return overview

def GetFundingRoundInfo(amount_type_soup):
  amount = amount_type_soup.find('span', class_='funding_amount').get_text()
  f_type = amount_type_soup.find('span', class_='funding-type').get_text()
  date_soup = amount_type_soup.next_sibling
  assert 'date' in date_soup['class']
  date = str(date_soup.string)
  investors = date_soup.next_sibling.get_text() if date_soup.next_sibling else None
  return FundingRound(type=f_type, amount=amount, date=date, investors=investors)

def GetFundingRounds(soup):
  funding_round_soup = soup.find('div', class_='funding_rounds')
  return [GetFundingRoundInfo(at_soup) for at_soup in funding_round_soup.find_all('h4')]

if __name__ == '__main__':
  print sys.argv
  company = sys.argv[1]
  print GetCompanyInfo(company)