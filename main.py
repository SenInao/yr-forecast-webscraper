from getForecast import getForecast

city = input("City: ")
day = int(input("Day, 0=today, 1=tomorrow ...: "))

forecast = getForecast(city, day)

for hourCast in forecast:
    print(hourCast)
