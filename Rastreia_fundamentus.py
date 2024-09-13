#!/usr/bin/env python3

import re
import urllib.request
import urllib.parse
import http.cookiejar

from lxml.html import fragment_fromstring
from collections import OrderedDict
from decimal import Decimal
import os

# Testar Fórmula Mágica
# Volume Negociação > R$1.000.000
# ebit_ev (Calcular Lucro/Preço ao invés de Preço/Lucro) .rank(ascending=False) gera um ranking decrescente
# roic alto é bom


def get_data(*args, **kwargs):
    url = 'http://www.fundamentus.com.br/resultado.php'
    cookie_jar = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie_jar))
    opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201'),
                         ('Accept', 'text/html, text/plain, text/css, text/sgml, */*;q=0.01')]

    # Aqui estão os parâmetros de busca das ações
    # Estão em branco para que retorne todas as disponíveis
    data = {'pl_min': '',
            'pl_max': '',
            'pvp_min': '',
            'pvp_max' : '',
            'psr_min': '',
            'psr_max': '',
            'divy_min': '',
            'divy_max': '',
            'pativos_min': '',
            'pativos_max': '',
            'pcapgiro_min': '',
            'pcapgiro_max': '',
            'pebit_min': '',
            'pebit_max': '',
            'fgrah_min': '',
            'fgrah_max': '',
            'firma_ebit_min': '',
            'firma_ebit_max': '',
            'margemebit_min': '',
            'margemebit_max': '',
            'margemliq_min': '',
            'margemliq_max': '',
            'liqcorr_min': '',
            'liqcorr_max': '',
            'roic_min': '',
            'roic_max': '',
            'roe_min': '',
            'roe_max': '',
            'liq_min': '',
            'liq_max': '',
            'patrim_min': '',
            'patrim_max': '',
            'divbruta_min': '',
            'divbruta_max': '',
            'tx_cresc_rec_min': '',
            'tx_cresc_rec_max': '',
            'setor': '',
            'negociada': 'ON',
            'ordem': '1',
            'x': '28',
            'y': '16'}

    with opener.open(url, urllib.parse.urlencode(data).encode('UTF-8')) as link:
        content = link.read().decode('ISO-8859-1')

    pattern = re.compile('<table id="resultado".*</table>', re.DOTALL)
    content = re.findall(pattern, content)[0]
    page = fragment_fromstring(content)
    result = OrderedDict()

    for rows in page.xpath('tbody')[0].findall("tr"):
        result.update({rows.getchildren()[0][0].getchildren()[0].text: {'Cotacao': todecimal(rows.getchildren()[1].text),
                                                                        'P/L': todecimal(rows.getchildren()[2].text),
                                                                        'P/VP': todecimal(rows.getchildren()[3].text),
                                                                        'PSR': todecimal(rows.getchildren()[4].text),
                                                                        'DY': todecimal(rows.getchildren()[5].text),
                                                                        'P/Ativo': todecimal(rows.getchildren()[6].text),
                                                                        'P/Cap.Giro': todecimal(rows.getchildren()[7].text),
                                                                        'P/EBIT': todecimal(rows.getchildren()[8].text),
                                                                        'P/ACL': todecimal(rows.getchildren()[9].text),
                                                                        'EV/EBIT': todecimal(rows.getchildren()[10].text),
                                                                        'EV/EBITDA': todecimal(rows.getchildren()[11].text),
                                                                        'Mrg.Ebit': todecimal(rows.getchildren()[12].text),
                                                                        'Mrg.Liq.': todecimal(rows.getchildren()[13].text),
                                                                        'Liq.Corr.': todecimal(rows.getchildren()[14].text),
                                                                        'ROIC': todecimal(rows.getchildren()[15].text),
                                                                        'ROE': todecimal(rows.getchildren()[16].text),
                                                                        'Liq.2meses': todecimal(rows.getchildren()[17].text),
                                                                        'Pat.Liq': todecimal(rows.getchildren()[18].text),
                                                                        'Div.Brut/Pat.': todecimal(rows.getchildren()[19].text),
                                                                        'Cresc.5anos': todecimal(rows.getchildren()[20].text)}})

    return result

    
def todecimal(string):
  string = string.replace('.', '')
  string = string.replace(',', '.')

  if (string.endswith('%')):
    string = string[:-1]
    return Decimal(string) / 100
  else:
    return Decimal(string)

os.system('cls') or None

if __name__ == '__main__':
    from waitingbar import WaitingBar
    
    print('')
    print('')
    print('')
    print('')
    progress_bar = WaitingBar('[*] Baixando dados Fundamentus...')
    result = get_data()
    progress_bar.stop()

    result_format = '{0:<6} {1:<7} {2:<6} {3:<7} {4:<7} {5:<7} {6:<10} {7:<10} {8:<10} {9:<11} {10:<11} {11:<7} {12:<11} {13:<11} {14:<7} {15:<11} {16:<5} {17:<7}'
    print('')
    print('')
    print('')
    print('')
    print(result_format.format('Papel',
                               'Cotacao',
                               'P/L',
                               'P/VP',
                               #'PSR',
                               'DY',
                               'P/Ativo',
                               'P/Cap.Giro',
                               'P/EBIT',
                               'P/ACL',
                               'EV/EBIT',
                               'EV/EBITDA',
                               'Mrg.Ebit',
                               'Mrg.Liq.',
                               'Liq.Corr.',
                               'ROIC',
                               'ROE',
                               'Liq.2mês',
                               'Pat.Liq',
                               'Div.Brut/Pat.',
                               'Cresc.5anos'))

    print('-' * 170)
    i = 0
    lista_interesse = []
    for key, value in result.items():
################# Estratégia de filtro #################
        if (#(key == 'ABEV3' ) |(key == 'AERI3' ) |  (key == 'BBSE3' ) | (key == 'EGIE3' ) |
           #(key == 'FLRY3' ) | (key == 'ITSA3' ) | (key == 'ITSA4' ) | (key == 'KEPL3' ) |
           #(key == 'KLBN3' ) | (key == 'MGLU3' ) | (key == 'NVDC34' ) | (key == 'PETR4' ) |
           #(key == 'RANI3' ) | (key == 'ROMI3' ) | (key == 'SAPR4' ) |  (key == 'TOTS3' ) |
           #(key == 'WEGE3' )):
          (value['P/L'] <= 10) # P/L = em quantos anos se paga
          & (value['P/VP'] >= 0) & (value['P/VP'] <= 2) # P/VP mais próximo de 1. Quanto menor, mais barato
          & (value['DY'] >= 6 /100) & (value['DY'] < 100 /100) # DY em %; No mínimo 6% pela Luise Barsi
          & (value['ROE'] >= 10.50 /100) # ROE em % ; Valor Próximo a SELIC atual
          & (value['EV/EBITDA'] <= 3) # Dívida Liq. Ebitda no máximo 3x
          & (value['Cotacao'] >= 0) & (value['Cotacao'] <= 1000) # Valor da Ação
          & (value['P/EBIT'] >= 0) # Um P/EBIT negativo mostra que há alguma falha nas operações de uma empresa
          ):
          #print('')
          lista_interesse.append({'acao': key, 
                                  'cotacao': value['Cotacao'],
                                  'P/L': value['P/L'],
                                  'P/VP': value['P/VP'],
                                  'dividendo': value['DY']*100
                                  })
          #print('')
          #print(lista_interesse)
          #print('')
          print(result_format.format(key,
                                    value['Cotacao'],
                                    value['P/L'], 
                                    value['P/VP'],
                                    #value['PSR'],
                                    ('{0:.1f}%'.format(value['DY']*100)),
                                    value['P/Ativo'],
                                    value['P/Cap.Giro'],
                                    value['P/EBIT'],
                                    value['P/ACL'],# Preço da Ação / Ativo Circulante.Como interpretar capital circulante líquido? Quando uma empresa possui o seu Capital Circulante Líquido positivo indica que o seu crescimento é duradouro, e que ela está utilizando de forma correta o seu capital. Já um Capital Circulante Líquido negativo poderá indicar que a empresa está passando por dificuldades.
                                    value['EV/EBIT'],
                                    value['EV/EBITDA'],
                                    ('{0:.1f}%'.format(value['Mrg.Ebit']*100)),
                                    ('{0:.1f}%'.format(value['Mrg.Liq.']*100)),
                                    value['Liq.Corr.'],
                                    ('{0:.1f}%'.format(value['ROIC']*100)),
                                    ('{0:.1f}%'.format(value['ROE']*100)),
                                    ('{0:.1f}mi'.format(value['Liq.2meses']/1000000)),
                                    ('{0:.1f}bi'.format(value['Pat.Liq']/1000000000)),
                                    value['Div.Brut/Pat.'],
                                    ('{0:.2f}%'.format(value['Cresc.5anos']*100))))
          i= i +1
          #print('')
          print('-' * 170)
print('')

def sort_cotacao(e):
   return e['cotacao']
lista_interesse.sort(key=sort_cotacao)
print('')
print('- COTAÇÃO')
print('')
print('------------------------------------ COTAÇÃO')
print('')
for j in range(0, len(lista_interesse)):
   print(lista_interesse[j])
   print('---------------------------------------------------------------------------------------------------------------------------------')
print('')
print('')

def sort_PL(e):
   return e['P/L']
lista_interesse.sort(key=sort_PL)
print('')
print('- P/L - Em quantos ANOS se paga')
print('')
print('--------------------------------------------------------------- P/L')
print('')
for j in range(0, len(lista_interesse)):
   print(lista_interesse[j])
   print('---------------------------------------------------------------------------------------------------------------------------------')
print('')
print('')

def sort_PVP(e):
   return e['P/VP']
lista_interesse.sort(key=sort_PVP)
print('')
print('- P/VP - Quanto menor, mais Barato!')
print('')
print('-------------------------------------------------------------------------------------- P/VP')
print('')
for j in range(0, len(lista_interesse)):
   print(lista_interesse[j])
   print('---------------------------------------------------------------------------------------------------------------------------------')
print('')
print('')


def sort_DY(e):
   return e['dividendo']
lista_interesse.sort(reverse=True, key=sort_DY)
print('')
print('- DIVIDENDO - Recomendado no mínimo 6%')
print('')
print('---------------------------------------------------------------------------------------------------------------------- DY')
print('')
for j in range(0, len(lista_interesse)):
   print(lista_interesse[j])
   print('---------------------------------------------------------------------------------------------------------------------------------')
print('')
print('')

print('Ativos:')
print(i)
print('')