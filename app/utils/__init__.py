import requests
from bs4 import BeautifulSoup

months = {
    1: "mes_enero",
    2: "mes_febrero",
    3: "mes_marzo",
    4: "mes_abril",
    5: "mes_mayo",
    6: "mes_junio",
    7: "mes_julio",
    8: "mes_agosto",
    9: "mes_septiembre",
    10: "mes_octubre",
    11: "mes_noviembre",
    12: "mes_diciembre"
}


def get_uf_value(date):
    year = date.year
    url = f'https://www.sii.cl/valores_y_fechas/uf/uf{year}.htm'

    return get_value_from_web(url, date)


def get_value_from_web(url, date):
    try:
        response = requests.get(url)

        # Raise an exception if the response status code is not 200 (OK)
        response.raise_for_status()
    except requests.exceptions.RequestException:
        # Return an error message if the request fails due to a network error
        return {'error': 'CONNECTION_ERROR', 'message': 'Unable to retrieve UF value due to a network error.'}

    # Parse the HTML with BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the div element with id the required month
    month_div = soup.find("div", id=months[date.month])

    # Find the th element with a value of the required day inside a strong element
    strong_th = month_div.find('strong', text=date.day).parent

    # Find the td element that is a child of the strong_th element
    td = strong_th.find_next_sibling('td')

    # Extract the text value of the td element
    uf_value = td.text.strip()

    return uf_value
