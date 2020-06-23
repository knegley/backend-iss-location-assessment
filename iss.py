#!/usr/bin/env python

__author__ = 'Kyle Negley'

import requests
import turtle
import time


def get_astonauts() -> object:
    url = "http://api.open-notify.org/astros.json"
    response = requests.get(url).json()
    # print(response["message"])
    # print(response["people"])
    return({"people": response["people"], "number": response["number"]})


def get_coordinates() -> object:
    url = "http://api.open-notify.org/iss-now.json"
    response = requests.get(url).json()
    timestamp = {"timestamp": time.ctime(response["timestamp"])}

    return {**(response["iss_position"]), **timestamp}


def screen() -> None:
    indy_lat, indy_long = 40.273502, -86.126976
    window = turtle.Screen()
    coords = get_coordinates()
    # print(get_coordinates())
    (lat, lon) = (float(coords["latitude"]), float(coords["longitude"]))
    # print(lat, lon)

    turtle.title("Kyle's Assessment")
    window.bgpic("map.gif")
    window.setup(width=720, height=360)
    window.setworldcoordinates(-180, -90, 180, 90)
    t = turtle.Turtle()
    t.color("purple")
    t.speed(1)
    # t.pendown()
    # t.stamp()
    # t.goto(180, 90)
    # t.goto(46.79844, 62.1764)
    # print(f"{lat=}")
    # print(f"{lon=}")
    t.penup()
    t.setpos(indy_long, indy_lat)
    t.pendown()
    t.shape("turtle")
    t.shapesize(.5, .5, .5)
    t.stamp()
    t.penup()
    window.addshape("iss.gif")
    t.shape("iss.gif")
    t.setpos(lon, lat)
    # print(type(lat))
    # print(type(lon))
    # t.penup()
    window.mainloop()


def is_over_indy() -> list:

    indy_lat, indy_long = 40.273502, -86.126976
    url = "http://api.open-notify.org/iss-pass.json"
    params = {"lat": str(indy_lat), "lon": str(indy_long)}
    # print(params)
    response = requests.get(url, params=params).json()["response"]
    output = [time.ctime(item["risetime"]) for item in response]
    return f"Times ISS will pass Indy:\n\t {output}"


def main():
    print(f"Astronauts: {get_astonauts()}\n")
    print(f"Iss Location: {get_coordinates()}\n")
    print(is_over_indy())
    screen()


if __name__ == '__main__':
    main()
