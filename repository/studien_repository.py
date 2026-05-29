import json
from datetime import date
from pathlib import Path

from domain.enums import ModulStatus, Pruefungsart, Schwierigkeit, Studienmodell
from domain.models import Modul, Note, Pruefungsleistung, Studium


class StudienRepository:
    def __init__(self, dateipfad: str):
        self.dateipfad = Path(dateipfad)

    def lade_studium(self) -> Studium:
        with open(self.dateipfad, "r", encoding="utf-8") as datei:
            daten = json.load(datei)

        module = [
            self._erstelle_modul(modul_daten)
            for modul_daten in daten["module"]
        ]

        return Studium(
            studiengang=daten["studiengang"],
            studienmodell=Studienmodell[daten["studienmodell"]],
            zielnotenschnitt=daten["zielnotenschnitt"],
            module=module
        )

    def speichere_studium(self, studium: Studium) -> None:
        daten = {
            "studiengang": studium.studiengang,
            "studienmodell": studium.studienmodell.name,
            "zielnotenschnitt": studium.zielnotenschnitt,
            "module": [
                self._modul_zu_dict(modul)
                for modul in studium.module
            ]
        }

        with open(self.dateipfad, "w", encoding="utf-8") as datei:
            json.dump(daten, datei, ensure_ascii=False, indent=2)

    def _erstelle_modul(self, daten: dict) -> Modul:
        pruefungsleistung = self._erstelle_pruefungsleistung(
            daten["pruefungsleistung"]
        )

        return Modul(
            modulname=daten["modulname"],
            ects=daten["ects"],
            status=ModulStatus[daten["status"]],
            subjektive_schwierigkeit=Schwierigkeit[daten["subjektive_schwierigkeit"]],
            pruefungsleistung=pruefungsleistung
        )

    def _erstelle_pruefungsleistung(self, daten: dict) -> Pruefungsleistung:
        note = None
        if daten["note"] is not None:
            note = Note(
                wert=daten["note"]["wert"],
                bewertungsdatum=self._parse_datum(daten["note"]["bewertungsdatum"])
            )

        return Pruefungsleistung(
            pruefungsart=Pruefungsart[daten["pruefungsart"]],
            geplante_abgabe=self._parse_datum(daten["geplante_abgabe"]),
            tatsaechliche_abgabe=self._parse_datum(daten["tatsaechliche_abgabe"]),
            bewertung_erwartet_am=self._parse_datum(daten["bewertung_erwartet_am"]),
            note=note
        )

    def _modul_zu_dict(self, modul: Modul) -> dict:
        return {
            "modulname": modul.modulname,
            "ects": modul.ects,
            "status": modul.status.name,
            "subjektive_schwierigkeit": modul.subjektive_schwierigkeit.name,
            "pruefungsleistung": self._pruefungsleistung_zu_dict(
                modul.pruefungsleistung
            )
        }

    def _pruefungsleistung_zu_dict(self, pruefungsleistung: Pruefungsleistung) -> dict:
        note = None
        if pruefungsleistung.note is not None:
            note = {
                "wert": pruefungsleistung.note.wert,
                "bewertungsdatum": self._datum_zu_text(
                    pruefungsleistung.note.bewertungsdatum
                )
            }

        return {
            "pruefungsart": pruefungsleistung.pruefungsart.name,
            "geplante_abgabe": self._datum_zu_text(pruefungsleistung.geplante_abgabe),
            "tatsaechliche_abgabe": self._datum_zu_text(
                pruefungsleistung.tatsaechliche_abgabe
            ),
            "bewertung_erwartet_am": self._datum_zu_text(
                pruefungsleistung.bewertung_erwartet_am
            ),
            "note": note
        }

    def _parse_datum(self, wert: str | None) -> date | None:
        if wert is None:
            return None

        return date.fromisoformat(wert)

    def _datum_zu_text(self, wert: date | None) -> str | None:
        if wert is None:
            return None

        return wert.isoformat()