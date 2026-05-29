from enum import Enum


class Studienmodell(Enum):
    VOLLZEIT = "Vollzeit"
    TEILZEIT_I = "Teilzeit I"
    TEILZEIT_II = "Teilzeit II"


class ModulStatus(Enum):
    NICHT_GESTARTET = "nicht gestartet"
    IN_BEARBEITUNG = "in Bearbeitung"
    ABGEGEBEN = "abgegeben"
    BESTANDEN = "bestanden"
    PAUSIERT = "pausiert"


class Schwierigkeit(Enum):
    LEICHT = "leicht"
    MITTEL = "mittel"
    SCHWER = "schwer"


class Pruefungsart(Enum):
    KLAUSUR = "Klausur"
    PORTFOLIO = "Portfolio"
    FALLSTUDIE = "Fallstudie"
    SEMINARARBEIT = "Seminararbeit"