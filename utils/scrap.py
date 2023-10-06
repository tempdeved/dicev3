# import pandas as pd
# import requests
# from datetime import datetime, timedelta
# from dash import html
# import dash_bootstrap_components as dbc
# from requests_html import HTMLSession
# # import lxml
# from bs4 import BeautifulSoup
#
#
# class Scrap(object):
#
#     def __init__(self):
#         ...
#
#     def generic_table(self, html_table: BeautifulSoup(),
#                        id_name: str,
#                        city: str):
#         soup = BeautifulSoup(html_table, 'html.parser')
#
#         thead = soup.thead
#         tbody = soup.tbody
#
#         tbody_list = []
#         tr_thead = []
#
#         # Create Thead
#         for tr in thead.find_all('tr'):
#             th_list = []
#
#             for th in tr.find_all('th'):
#                 try:
#                     if th.text == '':
#                         content = city
#                     else:
#                         content = th.text
#                 except:
#                     # content = ''
#                     content = city
#
#                 try:
#                     attrs = th.attrs
#                     colspan = int(attrs['colspan'])
#                 except:
#                     attrs = {'colspan': 0}
#                     colspan = int(attrs['colspan'])
#
#                 th_list.append(html.Th(f'{content.upper()}', colSpan=f'{colspan}', className=''))
#                 # th_list.append(html.Th(f'{content.upper()}', colSpan=f'{colspan}', className='th-sm'))
#
#             tr_thead.append(html.Tr(th_list))
#
#         thead = [html.Thead(children=tr_thead, className='')]
#
#         # Create Tbody
#         for tr in tbody.find_all('tr'):
#             th_list = []
#
#             td_list = tr.find_all('td')
#             len(td_list)
#             for th in tr.find_all('th'):
#                 try:
#                     content = th.text
#                 except:
#                     content = ''
#
#                 try:
#                     attrs = th.attrs
#                     colspan = int(attrs['colspan'])
#                 except:
#                     attrs = {'colspan': 0}
#                     colspan = int(attrs['colspan'])
#
#                 th_list.append(html.Th(f'{content.upper()}', colSpan=f'{colspan}'))
#                 for td in td_list:
#                     try:
#                         content_td = td.text
#                     except:
#                         content_td = ''
#                     try:
#                         attrs_td = td.attrs
#                         colspan_td = int(attrs_td['colspan'])
#                     except:
#                         attrs_td = {'colspan': 0}
#                         colspan_td = int(attrs_td['colspan'])
#
#                     if content_td[-1:] == '%':
#                         if int(content_td[:-1]) < 30:
#                             th_list.append(
#                                 html.Td(f'{content_td.upper()}', colSpan=f'{colspan_td}', className='text-success'))
#                         elif int(content_td[:-1]) < 50:
#                             th_list.append(
#                                 html.Td(f'{content_td.upper()}', colSpan=f'{colspan_td}', className='text-warning'))
#                         else:
#                             th_list.append(
#                                 html.Td(f'{content_td.upper()}', colSpan=f'{colspan_td}', className='text-danger'))
#                     else:
#                         th_list.append(html.Td(f'{content_td.upper()}', colSpan=f'{colspan_td}'))
#
#             tbody_list.append(html.Tr(th_list))
#
#         # tbody = [html.Tbody()]
#         tbody = [html.Tbody(tbody_list)]
#
#         table = dbc.Table(
#             id=f'id-{id_name}',
#             children=thead + tbody,
#             class_name='table-sm'
#         )
#
#         return table
#
#     def fah_to_celc(self, temp_fahrenheit):
#         # temp_fahrenheit = 86
#         celsius = (temp_fahrenheit - 32) / 1.8
#         return int(round(celsius, 0))
#
#     def get_acao_from_google(self, id, class_id):
#         acesso = HTMLSession()  # inicie um acesso (como se fosse um navegador)
#         link = acesso.get(f'https://www.google.com/search?q={id}', verify=False)
#         html = BeautifulSoup(link.text, 'lxml')
#         valor = html.find('span', class_=class_id)
#         try:
#             acao = valor.text.replace(',', '.')
#         except:
#             acao = valor.text
#
#         return f'{acao}'
#
#     def get_weather(self, url, city):
#         print(url, city)
#         """
#         Get section from site weather.com by specific url
#         :param url: specific url informing the city
#         :return: element section and attributes
#         """
#
#         r = requests.get(url, verify=False)
#
#         if r.status_code > 400:
#             print(f'request status:{r.status_code}')
#
#         else:
#             soup = BeautifulSoup(r.text, 'html.parser')
#             # soup = BeautifulSoup(HTML, 'html.parser')
#
#             section_today = soup.find('section', {'data-testid': 'TodayWeatherModule'})
#             div_today_pct_rain = section_today.find_all('div', {'data-testid': 'SegmentPrecipPercentage'})
#
#             section_daily = soup.find('section', {'data-testid': 'DailyWeatherModule'})
#             div_daily_pct_rain = section_daily.find_all('div', {'data-testid': 'SegmentPrecipPercentage'})
#
#             temperature_today = section_today.find_all('span', {'data-testid': 'TemperatureValue'})
#             temperature_daily = section_daily.find_all('span', {'data-testid': 'TemperatureValue'})
#
#             temperature_list = []
#
#             df_today = pd.DataFrame({'Manhã': [], 'Tarde': [], 'Noite': [], 'Madrugada': []})
#             coluns = df_today.columns
#             cont = 0
#
#             for temp in temperature_today:
#                 rain = div_today_pct_rain[cont].find_all('span', {'class': 'Column--precip--3JCDO'})
#
#                 try:
#                     rain = rain[0].contents[1]
#                 except:
#                     rain = '--'
#
#                 temperature_list.append(self.fah_to_celc(int(temp.text[:-1])))
#                 df_today[coluns[cont]] = [f'{self.fah_to_celc(int(temp.text[:-1]))}º', rain]
#                 cont = cont + 1
#
#             temperature_list = []
#
#             date_ref = datetime.now()
#
#             df_daily = pd.DataFrame()
#
#             cont = 0
#             for temp in [0, 2, 4, 6, 8]:
#
#                 try:
#                     a = f'{self.fah_to_celc(int(temperature_daily[temp].text[:-1]))}º'
#                     b = f'{self.fah_to_celc(int(temperature_daily[temp + 1].text[:-1]))}º'
#                     rain = div_daily_pct_rain[cont].find_all('span', {'class': 'Column--precip--3JCDO'})
#                     rain = rain[0].contents[1]
#                 except Exception as err:
#                     a = '--'
#                     b = '--'
#                     rain = '--'
#
#                 c = {'max': a}
#                 d = {'min': b}
#
#                 # df_daily[date_ref.strftime('%d-%m')] = [a, b, rain]
#                 df_daily[date_ref.strftime('%A')] = [a, b, rain]
#
#                 temps = {date_ref.strftime('%d'): [c, d, rain]}
#
#                 date_ref = date_ref + timedelta(days=+1)
#
#                 temperature_list.append(temps)
#
#             df_today.rename(index={0: 'hoje'}, inplace=True)
#             df_today.rename(index={1: 'chuva'}, inplace=True)
#
#             df_daily.rename(index={0: 'max'}, inplace=True)
#             df_daily.rename(index={1: 'min'}, inplace=True)
#             df_daily.rename(index={2: 'chuva'}, inplace=True)
#
#             # daily_temp = {'Temperatura Diária': temperature_list}
#             # temperature_list = []
#
#             # weather_scrap = {city: [today_temp, daily_temp]}
#
#             return df_today, df_daily
#
#     def get_news(self, url, city):
#         print(url, city)
#         """
#         Get section from site weather.com by specific url
#         :param url: specific url informing the city
#         :return: element section and attributes
#         """
#
#         r = requests.get(url)
#
#         if r.status_code > 400:
#             print(f'request status:{r.status_code}')
#
#         else:
#             soup = BeautifulSoup(r.text, 'html.parser')
#             # soup = BeautifulSoup(HTML, 'html.parser')
#
#             section_today = soup.find('section', {'data-testid': 'TodayWeatherModule'})
#             div_today_pct_rain = section_today.find_all('div', {'data-testid': 'SegmentPrecipPercentage'})
#
#             section_daily = soup.find('section', {'data-testid': 'DailyWeatherModule'})
#             div_daily_pct_rain = section_daily.find_all('div', {'data-testid': 'SegmentPrecipPercentage'})
#
#             temperature_today = section_today.find_all('span', {'data-testid': 'TemperatureValue'})
#             temperature_daily = section_daily.find_all('span', {'data-testid': 'TemperatureValue'})
#
#             temperature_list = []
#
#             df_today = pd.DataFrame({'Manhã': [], 'Tarde': [], 'Noite': [], 'Madrugada': []})
#             coluns = df_today.columns
#             cont = 0
#
#             for temp in temperature_today:
#                 rain = div_today_pct_rain[cont].find_all('span', {'class': 'Column--precip--3JCDO'})
#
#                 temperature_list.append(self.fah_to_celc(int(temp.text[:-1])))
#                 df_today[coluns[cont]] = [f'{self.fah_to_celc(int(temp.text[:-1]))}º', rain[0].contents[1]]
#                 cont = cont + 1
#
#             temperature_list = []
#
#             date_ref = datetime.now()
#
#             df_daily = pd.DataFrame()
#
#             cont = 0
#             for temp in [0, 2, 4, 6, 8]:
#
#                 try:
#                     a = f'{self.fah_to_celc(int(temperature_daily[temp].text[:-1]))}º'
#                     b = f'{self.fah_to_celc(int(temperature_daily[temp + 1].text[:-1]))}º'
#                     rain = div_daily_pct_rain[cont].find_all('span', {'class': 'Column--precip--3JCDO'})
#                     rain = rain[0].contents[1]
#                 except Exception as err:
#                     a = '--'
#                     b = '--'
#                     rain = '--'
#
#                 c = {'max': a}
#                 d = {'min': b}
#
#                 # df_daily[date_ref.strftime('%d-%m')] = [a, b, rain]
#                 df_daily[date_ref.strftime('%A')] = [a, b, rain]
#
#                 temps = {date_ref.strftime('%d'): [c, d, rain]}
#
#                 date_ref = date_ref + timedelta(days=+1)
#
#                 temperature_list.append(temps)
#
#             df_today.rename(index={0: 'hoje'}, inplace=True)
#             df_today.rename(index={1: 'chuva'}, inplace=True)
#
#             df_daily.rename(index={0: 'max'}, inplace=True)
#             df_daily.rename(index={1: 'min'}, inplace=True)
#             df_daily.rename(index={2: 'chuva'}, inplace=True)
#
#             # daily_temp = {'Temperatura Diária': temperature_list}
#             # temperature_list = []
#
#             # weather_scrap = {city: [today_temp, daily_temp]}
#
#             return df_today, df_daily