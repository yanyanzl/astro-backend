import swisseph as swe
from datetime import datetime

swe.set_ephe_path("./ephemeris")

PLANETS = {
    "Sun": swe.SUN,
    "Moon": swe.MOON,
    "Mercury": swe.MERCURY,
    "Venus": swe.VENUS,
    "Mars": swe.MARS,
    "Jupiter": swe.JUPITER,
    "Saturn": swe.SATURN,
    "Uranus": swe.URANUS,
    "Neptune": swe.NEPTUNE,
    "Pluto": swe.PLUTO,
}

def calculate_chart(dt, lat, lon):
    jd = swe.julday(
        dt.year,
        dt.month,
        dt.day,
        dt.hour + dt.minute / 60.0
    )

    swe.set_topo(lon, lat, 0)

    planets = {}
    for name, pid in PLANETS.items():
        lon_deg, lat, dist, speed = swe.calc_ut(jd, pid)
        planets[name] = {
            "degree": lon_deg,
            "retrograde": speed < 0
        }

    houses, ascmc = swe.houses(jd, lat, lon)

    return {
        "planets": planets,
        "houses": houses.tolist(),
        "ascendant": ascmc[0],
        "mc": ascmc[1]
    }
