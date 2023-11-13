from acoes.config.config import Config
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.firefox.options import Options

"""
CHROME CONFIG
"""
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument(r"user-data-dir=C:\Users\edson.santos\AppData\Local\Google\Chrome\User Data\Default\Profile 1")
CHROME_LOCATION = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
chrome_options.binary_location = CHROME_LOCATION

# cmd_line = r'"C:\Program Files\Google\Chrome\Application\chrome.exe" --flag-switches-begin --flag-switches-end --origin-trial-disabled-features=WebGPU'

config = Config().config


def abrir_abas():

    # chrome = webdriver.Firefox(options=chrome_options, keep_alive=True)
    chrome = webdriver.Chrome(options=chrome_options, keep_alive=True)
    chrome.get(config['tradingview']['url_base'])


    for x, acao in enumerate(config['b3']['acoes_monitorar']):

        # https://br.tradingview.com/chart/?symbol=BMFBOVESPA%3AVALE3
        symbol = config['b3']['acoes_monitorar'][acao]['symbol']

        url = f"{config['tradingview']['url_base']}/{config['tradingview']['endpoint']['symbols']['url']}/?symbol=BMFBOVESPA%3A{symbol}"

        # https://statusinvest.com.br/acoes/csrn3

        chrome.get(url)

        chrome.execute_script(f"window.open('');")

        chrome.switch_to.window(chrome.window_handles[x+1])


    chrome.switch_to.window(chrome.window_handles[0])

    print('')

if __name__ == '__main__':
    abrir_abas()
    print('')