from domain.models import DashboardDaten, Studium
from repository.studien_repository import StudienRepository
from services.bewertungs_service import BewertungsService
from services.fortschritts_service import FortschrittsService
from services.noten_service import NotenService


class DashboardController:
    def __init__(
        self,
        repository: StudienRepository,
        noten_service: NotenService,
        fortschritts_service: FortschrittsService,
        bewertungs_service: BewertungsService
    ):
        self.repository = repository
        self.noten_service = noten_service
        self.fortschritts_service = fortschritts_service
        self.bewertungs_service = bewertungs_service

    def lade_studium(self) -> Studium:
        return self.repository.lade_studium()

    def speichere_studium(self, studium: Studium) -> None:
        self.repository.speichere_studium(studium)

    def lade_dashboard_daten(self) -> DashboardDaten:
        studium = self.lade_studium()

        durchschnittsnote = self.noten_service.berechne_durchschnitt(studium)

        return DashboardDaten(
            anzahl_module=len(studium.module),
            abgeschlossene_module=self.fortschritts_service.zaehle_abgeschlossene_module(
                studium
            ),
            erreichte_ects=self.fortschritts_service.berechne_erreichte_ects(studium),
            gesamt_ects=self.fortschritts_service.berechne_gesamt_ects(studium),
            fortschritt_prozent=self.fortschritts_service.berechne_fortschritt_prozent(
                studium
            ),
            durchschnittsnote=durchschnittsnote,
            ziel_erreicht=self.noten_service.pruefe_zielerreichung(studium),
            offene_bewertungen=self.bewertungs_service.ermittle_offene_bewertungen(
                studium
            )
        )