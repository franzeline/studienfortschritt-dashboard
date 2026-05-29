from domain.enums import ModulStatus
from domain.models import Studium


class FortschrittsService:
    def berechne_gesamt_ects(self, studium: Studium) -> int:
        gesamt_ects = 0

        for modul in studium.module:
            gesamt_ects += modul.ects

        return gesamt_ects

    def berechne_erreichte_ects(self, studium: Studium) -> int:
        erreichte_ects = 0

        for modul in studium.module:
            if modul.status == ModulStatus.BESTANDEN:
                erreichte_ects += modul.ects

        return erreichte_ects

    def zaehle_abgeschlossene_module(self, studium: Studium) -> int:
        anzahl = 0

        for modul in studium.module:
            if modul.status == ModulStatus.BESTANDEN:
                anzahl += 1

        return anzahl

    def berechne_fortschritt_prozent(self, studium: Studium) -> float:
        gesamt_ects = self.berechne_gesamt_ects(studium)

        if gesamt_ects == 0:
            return 0.0

        erreichte_ects = self.berechne_erreichte_ects(studium)

        return round((erreichte_ects / gesamt_ects) * 100, 2)