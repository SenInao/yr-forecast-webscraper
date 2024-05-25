import requests
from bs4 import BeautifulSoup

def searchPlace(city: str, day: int) -> str:
    if (day > 9 or day < 0):
        raise Exception(f"Day cannot be {day}. 0 <= day <= 9")

    result = requests.get(f"https://www.yr.no/nb/s%C3%B8k?q={city}")
    soup = BeautifulSoup(result.text, "html.parser")

    try:
        link = soup.find_all(class_="search-results-list__item-anchor")[0].get("href")
    except IndexError:
        raise Exception(f"City {city} does not exist")

    link = link.replace("daglig", "time")

    return "https://www.yr.no" + link + f"?i={day}"

def retrieveSource(city: str, day: int) -> str:
    link = searchPlace(city, day)

    result = requests.get(link)
    return result.text

def getForecast(city: str, daysInFutue: int) -> list:
    source = retrieveSource(city, daysInFutue)

    soup = BeautifulSoup(source, "html.parser")

    forecast = []
    rows = soup.find_all(class_="fluid-table__row")
    for row in rows:
        time = row.find_all(class_="hourly-weather-table__time")
        weather = row.find_all(class_="hourly-weather-table__weather")
        degrees = row.find_all(class_="temperature temperature--warm-primary")
        wind = row.find_all(class_="wind__container")

        for i in range(len(time)):
            hourCast = {"hour":time[i].text, "degrees":degrees[i-1].text, "weather":weather[i].img["alt"], "wind":wind[i].text}
            forecast.append(hourCast)

    return forecast
