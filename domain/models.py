from dataclasses import dataclass
from datetime import date

from domain.enums import ModulStatus, Pruefungsart, Schwierigkeit, Studienmodell


@dataclass
class Note:
    wert: float
    bewertungsdatum: date


@dataclass
class Pruefungsleistung:
    pruefungsart: Pruefungsart
    geplante_abgabe: date | None
    tatsaechliche_abgabe: date | None
    bewertung_erwartet_am: date | None
    note: Note | None = None

    def ist_abgegeben(self) -> bool:
        return self.tatsaechliche_abgabe is not None

    def ist_bewertet(self) -> bool:
        return self.note is not None


@dataclass
class Modul:
    modulname: str
    ects: int
    status: ModulStatus
    subjektive_schwierigkeit: Schwierigkeit
    pruefungsleistung: Pruefungsleistung

    def ist_abgeschlossen(self) -> bool:
        return self.status == ModulStatus.BESTANDEN


@dataclass
class Studium:
    studiengang: str
    studienmodell: Studienmodell
    zielnotenschnitt: float
    module: list[Modul]


@dataclass
class DashboardDaten:
    anzahl_module: int
    abgeschlossene_module: int
    erreichte_ects: int
    gesamt_ects: int
    fortschritt_prozent: float
    durchschnittsnote: float | None
    ziel_erreicht: bool
    offene_bewertungen: list[Pruefungsleistung]