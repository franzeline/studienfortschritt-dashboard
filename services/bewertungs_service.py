from domain.models import Pruefungsleistung, Studium


class BewertungsService:
    def ermittle_offene_bewertungen(
        self,
        studium: Studium
    ) -> list[Pruefungsleistung]:
        offene_bewertungen = []

        for modul in studium.module:
            pruefungsleistung = modul.pruefungsleistung

            if (
                pruefungsleistung.ist_abgegeben()
                and not pruefungsleistung.ist_bewertet()
            ):
                offene_bewertungen.append(pruefungsleistung)

        return offene_bewertungen