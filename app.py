from controller.dashboard_controller import DashboardController
from repository.studien_repository import StudienRepository
from services.bewertungs_service import BewertungsService
from services.fortschritts_service import FortschrittsService
from services.noten_service import NotenService
from view.streamlit_view import StreamlitView


class DashboardApp:
    def __init__(self):
        repository = StudienRepository("data/studium.json")
        noten_service = NotenService()
        fortschritts_service = FortschrittsService()
        bewertungs_service = BewertungsService()

        self.controller = DashboardController(
            repository=repository,
            noten_service=noten_service,
            fortschritts_service=fortschritts_service,
            bewertungs_service=bewertungs_service
        )

        self.view = StreamlitView()

    def start(self) -> None:
        studium = self.controller.lade_studium()
        dashboard_daten = self.controller.lade_dashboard_daten()

        self.view.zeige_dashboard(studium, dashboard_daten)


app = DashboardApp()
app.start()