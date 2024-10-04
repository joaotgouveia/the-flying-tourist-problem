from pysat.examples.rc2 import RC2Stratified
from pysat.formula import WCNF
from pysat.card import CardEnc, EncType
import datetime

def parse():
    # Number of cities to visit
    n = int(input())

    # Dictionary of cities to visit, the key is the airport code.
    base = input().split()
    cities = {base[1]: {"name": base[0], "arrivals":[], "departures": []}}
    for _ in range(n - 1):
        city = input().split()
        cities[city[1]] = {
            "name": city[0],
            "stay": datetime.timedelta(days=int(city[2])),
            "arrivals": [],
            "departures": [],
        }

    # Number of flights available
    m = int(input())

    for i in range(m):
        line = input().split()

        # Parsing the date
        date = line[0].split("/")

        flight = {
            "date": datetime.date(2024, int(date[1]), int(date[0])),
            "departure": line[1],
            "arrival": line[2],
            "departureTime": line[3],
            "arrivalTime": line[4],
            "cost": int(line[5]),
            "id": i + 1
        }

        cities[line[1]]["departures"].append(flight)
        cities[line[2]]["arrivals"].append(flight)

    return base, cities

def printModel(model, cities):
    if model != None:
        cost = 0
        takenFlights = []
        for airport in cities.keys():
            for flight in cities[airport]["arrivals"]:
                if model[flight["id"] - 1] > 0:
                    takenFlights.append(flight)

        takenFlights.sort(key=(lambda x: x["date"]))
        for flight in takenFlights:
            print((f"{flight['date'].strftime('%d/%m')} "
            f"{cities[flight['departure']]['name']} "
            f"{cities[flight['arrival']]['name']} "
            f"{flight['departureTime']} {flight['cost']}"))

def encode(base, cities):
    formula = WCNF()

    # We can't have a flight before our departure from the base.
    for departure in cities[base[1]]["departures"]:
        for airport in cities.keys():
            if airport != base[1]:
                for flight in cities[airport]["departures"]:
                    if not flight["date"] > departure["date"]:
                        formula.append([-departure["id"], -flight["id"]])

    # After arriving in a city, we must depart exactly K days later.
    for airport in cities.keys():
        # We do not care about arrivals in the base
        if airport != base[1]:
            for arrival in cities[airport]["arrivals"]:
                clause = [-arrival["id"]]
                departureDate = arrival["date"] + cities[airport]["stay"]
                for departure in cities[airport]["departures"]:
                    if departure["date"] == departureDate:
                        clause.append(departure["id"])
                formula.append(clause)

    # We must arrive and depart from each city exactly once.
    for airport in cities.keys():
        arrivalIds = list(map(lambda x: x["id"], cities[airport]["arrivals"]))
        for clause in CardEnc.equals(lits=arrivalIds, top_id=formula.nv, encoding=EncType.bitwise):
            formula.append(clause)

        departureIds = list(map(lambda x: x["id"], cities[airport]["departures"]))
        for clause in CardEnc.equals(lits=departureIds, top_id=formula.nv, encoding=EncType.bitwise):
            formula.append(clause)

    # Soft clauses
    for airport in cities.keys():
        for flight in cities[airport]["departures"]:
            formula.append([-flight["id"]], flight["cost"])

    return formula

if __name__ == "__main__":
    base, cities = parse()
    formula = encode(base, cities)
    solver = RC2Stratified(formula, blo='full')
    model = solver.compute()
    print(solver.cost)
    printModel(model, cities)
