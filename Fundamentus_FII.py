import re
import urllib.request
import urllib.parse
import http.cookiejar

from lxml.html import fragment_fromstring
from collections import OrderedDict
from decimal import Decimal
import os

# Base URL for REIT search on Fundamentus
BASE_URL = 'http://www.fundamentus.com.br/fii_resultado.php'


def get_data(fiis='ON'):
  """Fetches REIT data from Fundamentus.

  Args:
      fiis (str, optional): REIT type to search for. Defaults to 'ON'.

  Returns:
      OrderedDict: A dictionary containing REIT data.
  """

  # Set cookie jar
  cookie_jar = http.cookiejar.CookieJar()
  opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie_jar))
  opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201'),
                       ('Accept', 'text/html, text/plain, text/css, text/sgml, */*;q=0.01')]

  # Search parameters
  data = {
      'setor': 'FII',  # REIT sector
      'negociada': fiis,  # REIT type (ON or PN)
      'ordem': '1',  # Order results by code
      'x': '28',
      'y': '16'
  }

  # Send request and parse response
  with opener.open(BASE_URL, urllib.parse.urlencode(data).encode('UTF-8')) as link:
    content = link.read().decode('ISO-8859-1')
    pattern = re.compile('<table id="tabelaResultado".*</table>', re.DOTALL)
    content = re.findall(pattern, content)[0]
    page = fragment_fromstring(content)
    result = OrderedDict()

    # Extract data from each row
    for row in page.xpath('tbody')[0].findall("tr"):
      
    #   for i in range(13):
    #     print(i, row.getchildren()[i].text)
      

      code = row.getchildren()[0][0].getchildren()[0].text

      data = {
          'Codigo': code,
          #'Cotacao': todecimal(row.getchildren()[1].text),
          'Cotacao': row.getchildren()[2].text,
          'P/VP': row.getchildren()[5].text,
          'Dividend Yield': row.getchildren()[4].text,
          'Vacancy Rate': row.getchildren()[12].text if row.getchildren()[12].text else None,
      }
      result[code] = data

  return result


def todecimal(string):
  """Converts string to Decimal, handling percentages and commas."""

  string = string.replace('.', '')
  string = string.replace(',', '.')

  if string.endswith('%'):
    string = string[:-1]
  return Decimal(string) / 100 if '%' in string else Decimal(string)


def main():
  """Fetches and displays REIT data."""

  os.system('cls') or None

  print('Baixando dados Fundamentus...')
  data = get_data()

  # Define output format
  result_format = '{0:<6} {1:<10} {2:<7} {3:<15} {4:<15}'
  print('\n')
  print(result_format.format('Codigo', 'Cotacao', 'P/VP', 'Dividend Yield', 'Vacancy Rate'))
  print('-' * 80)

  # Display data for each REIT
  for code, info in data.items():
    #print(info)
    #vacancy_rate = '{0:.2f}%'.format(info['Vacancy Rate']) if info['Vacancy Rate'] else 'N/A'
    #vacancy_rate = info['Vacancy Rate']
    # print(result_format.format(code, info['Cotacao'], info['P/VP'],'{0:.2f}%'.format(info['Dividend Yield'] * 100), vacancy_rate))
    #print(result_format.format(code, info['Cotacao'], info['P/VP'],info['Dividend Yield'], info['Vacancy Rate']))
    print(code, info['Cotacao'], info['P/VP'],info['Dividend Yield'], info['Vacancy Rate'])


if __name__ == '__main__':
  main()