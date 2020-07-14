#!/usr/bin/env python

__author__ = 'Kyle Negley'

import requests
import turtle
import time


def get_astonauts() -> object:

    url = "http://api.open-notify.org/astros.json"

    response = requests.get(url).json()

    return({"people": response["people"], "number": response["number"]})


def get_coordinates() -> object:

    url = "http://api.open-notify.org/iss-now.json"

    response = requests.get(url).json()

    timestamp = {"timestamp": time.ctime(response["timestamp"])}

    return {**(response["iss_position"]), **timestamp}


def iterator_factory(key: str, /) -> iter:

    def iterator_(func: callable, /):

        def wrapper(arg: str, /):

            response = get_astonauts()
            value = response[key]

            if isinstance(value, int):
                yield value

            for item in value:
                yield f'{arg}: {item[arg]}'
        return wrapper
    return iterator_


def screen() -> None:
    indy_lat, indy_long = 39.7684, -86.1581
    window = turtle.Screen()
    coords = get_coordinates()
    next_time = is_over_indy()

    (lat, lon) = (float(coords["latitude"]), float(coords["longitude"]))

    turtle.title("Kyle's Assessment")
    window.bgpic("map.gif")
    window.setup(width=720, height=360)
    window.setworldcoordinates(-180, -90, 180, 90)
    t = turtle.Turtle()
    t.color("purple")
    t.speed(1)
    t.penup()
    t.setpos(indy_long, indy_lat)
    t.shape("circle")
    t.shapesize(.07, .07, .07)
    t.stamp()

    style = ("Ariel", 10)
    t.write(arg=next(next_time), font=style)

    window.addshape("iss.gif")
    t.shape("iss.gif")
    t.setpos(lon, lat)

    window.mainloop()


def is_over_indy() -> iter:

    indy_lat, indy_long = 40.273502, -86.126976
    url = "http://api.open-notify.org/iss-pass.json"
    params = {"lat": str(indy_lat), "lon": str(indy_long)}

    response = requests.get(url, params=params).json()["response"]
    return (time.ctime(item["risetime"]) for item in response)


def unpack_coords(**kwargs) -> iter:
    return ((f"{kwarg} = {value}" for kwarg, value in kwargs.items()))


def main() -> None:
    astronauts = (astronaut for astronaut in iterator_factory(
        "people")(lambda person: person)("name"))

    number = (number for number in iterator_factory(
        "number")(lambda number: number)("number"))

    location = (location for location in iterator_factory(
        "people")(lambda name: name)("craft"))
    print("")
    print(f"{next(location)}")
    print("")
    print(f"number_in_space_station = {next(number)}")
    print("")
    print("Astronauts", *astronauts, sep="\n\t")
    print("")
    print("Coordinates", *unpack_coords(**get_coordinates()), sep="\n\t",)
    print("")
    print("Times ISS will pass Indy:", *is_over_indy(), sep="\n\t")
    screen()


if __name__ == '__main__':
    main()
