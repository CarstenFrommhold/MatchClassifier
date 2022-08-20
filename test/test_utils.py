from match_classifier.utils import map_names


def test_map_names():

    assert map_names(
        from_=["Hamburger SV", "Greuther Fuerth", "1. FC Nuernberg"],
        to=["Nuernberg", "Fuerth", "Hamburg"]
    ) == {"Hamburger SV": "Hamburg",
          "Greuther Fuerth": "Fuerth",
          "1. FC Nuernberg": "Nuernberg"}


