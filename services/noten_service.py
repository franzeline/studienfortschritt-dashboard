from domain.models import Studium


class NotenService:
    def berechne_durchschnitt(self, studium: Studium) -> float | None:
        noten = []

        for modul in studium.module:
            note = modul.pruefungsleistung.note
            if note is not None:
                noten.append(note.wert)

        if len(noten) == 0:
            return None

        return round(sum(noten) / len(noten), 2)

    def pruefe_zielerreichung(self, studium: Studium) -> bool:
        durchschnitt = self.berechne_durchschnitt(studium)

        if durchschnitt is None:
            return False

        return durchschnitt <= studium.zielnotenschnitt