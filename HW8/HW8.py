import csv


def mapper(city_weather):
    for row in city_weather:
        city = row['city']
        day_temperature = float(row['day_temperatre'])
        night_temperature = float(row['night_temperature'])
        yield city, day_temperature, night_temperature, 1


def reducer(sorted_mapped_data):
    prev_city = None
    total_temp = 0
    count = 0
    for city, day_temp, night_temp, num in sorted_mapped_data:
        if prev_city != city:
            if prev_city is not None:
                yield prev_city, total_temp / (2 * count)
            prev_city = city
            total_temp = 0
            count = 0
        total_temp += day_temp + night_temp
        count += num

    if count > 0:
        yield prev_city, total_temp / (2 * count)


with open('hw/city_weather.csv', 'r') as city_weather_file:
    city_weather = csv.DictReader(city_weather_file, delimiter=',')
    mapped_data = list(mapper(city_weather))
    sorted_mapped_data = sorted(mapped_data, key=lambda x: x[0])
    reduced_data = reducer(sorted_mapped_data)
    for ans_city, city_temp in reduced_data:
        print(f'{ans_city}. AVG temp = {city_temp:.2f}')
