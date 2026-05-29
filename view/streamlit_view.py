import streamlit as st

from domain.models import DashboardDaten, Studium


class StreamlitView:
    def zeige_dashboard(
        self,
        studium: Studium,
        dashboard_daten: DashboardDaten
    ) -> None:
        st.set_page_config(
            page_title="Studienfortschritt Dashboard",
            page_icon="🎓",
            layout="wide"
        )
        
        st.markdown(
            """
            <style>
            div[data-testid="stProgress"] > div > div > div > div {
                background-color: #d946ef;
            }
            </style>
            """,
            unsafe_allow_html=True
        )
        
        st.title("Studienfortschritt Dashboard")
        st.caption("Prototyp zur Visualisierung des Studienfortschritts")

        st.subheader(studium.studiengang)
        st.write(f"Studienmodell: {studium.studienmodell.value}")
        st.write(f"Ziel: Notendurchschnitt {studium.zielnotenschnitt} oder besser")

        self.zeige_kennzahlen(dashboard_daten)
        self.zeige_erfolgsmoment(dashboard_daten)
        self.zeige_architekturhinweis()
        self.zeige_moduluebersicht(studium)
        self.zeige_offene_bewertungen(studium)
        

    def zeige_kennzahlen(self, dashboard_daten: DashboardDaten) -> None:
        st.header("Kennzahlen")

        spalte_1, spalte_2, spalte_3, spalte_4 = st.columns(4)

        spalte_1.metric(
            "Module",
            f"{dashboard_daten.abgeschlossene_module}/{dashboard_daten.anzahl_module}"
        )

        spalte_2.metric(
            "ECTS",
            f"{dashboard_daten.erreichte_ects}/{dashboard_daten.gesamt_ects}"
        )

        spalte_3.metric(
            "Studienstand",
            f"{dashboard_daten.fortschritt_prozent} %"
        )
        
        durchschnitt = dashboard_daten.durchschnittsnote
        if durchschnitt is None:
            durchschnitt_text = "Noch keine Note"
        else:
            durchschnitt_text = str(durchschnitt)

        spalte_4.metric(
            "Notenschnitt",
            durchschnitt_text
        )
        
        st.subheader("Visueller Studienfortschritt")

        fortschritt = dashboard_daten.fortschritt_prozent / 100
        st.progress(fortschritt)

        st.caption(
            f"{dashboard_daten.erreichte_ects} von "
            f"{dashboard_daten.gesamt_ects} ECTS wurden bereits erreicht."
        )
        
        if dashboard_daten.ziel_erreicht:
            st.success("Das definierte Notenziel wird aktuell erreicht.")
        else:
            st.warning("Das definierte Notenziel wird aktuell noch nicht erreicht.")

    def zeige_moduluebersicht(self, studium: Studium) -> None:
        st.header("Modulübersicht")

        tabellen_daten = []

        for modul in studium.module:
            pruefungsleistung = modul.pruefungsleistung

            if pruefungsleistung.note is None:
                note = "-"
            else:
                note = pruefungsleistung.note.wert

            tabellen_daten.append(
                {
                    "Modul": modul.modulname,
                    "ECTS": modul.ects,
                    "Status": modul.status.value,
                    "Schwierigkeit": modul.subjektive_schwierigkeit.value,
                    "Prüfungsart": pruefungsleistung.pruefungsart.value,
                    "Note": note
                }
            )

        st.dataframe(tabellen_daten, use_container_width=True)

    def zeige_offene_bewertungen(self, studium: Studium) -> None:
        st.header("Offene Bewertungen")

        offene_bewertungen = []

        for modul in studium.module:
            pruefungsleistung = modul.pruefungsleistung

            if (
                pruefungsleistung.ist_abgegeben()
                and not pruefungsleistung.ist_bewertet()
            ):
                offene_bewertungen.append((modul, pruefungsleistung))

        if len(offene_bewertungen) == 0:
            st.info("Aktuell sind keine Bewertungen offen.")
            return

        for modul, pruefungsleistung in offene_bewertungen:
            st.write(
                f"**{modul.modulname}** – "
                f"{pruefungsleistung.pruefungsart.value} – "
                f"erwartet am: {pruefungsleistung.bewertung_erwartet_am}"
            )
                
    def zeige_architekturhinweis(self) -> None:
        with st.expander("Architekturhinweis für die Bewertung"):
            st.write(
                "Dieses Dashboard ist bewusst nach einem einfachen Schichtenmodell aufgebaut. "
                "Die Benutzeroberfläche zeigt nur Daten an. Die Berechnung des Studienfortschritts, "
                "des Notendurchschnitts und der offenen Bewertungen erfolgt getrennt in Service-Klassen. "
                "Das Repository übernimmt das Laden und Speichern der JSON-Daten. "
                "Der Controller verbindet diese Komponenten und stellt der View fertige Dashboard-Daten bereit."
            )

            st.write(
                "Damit bleiben Darstellung, Fachlogik und Datenzugriff voneinander getrennt."
            )
    def zeige_erfolgsmoment(self, dashboard_daten: DashboardDaten) -> None:
        if dashboard_daten.abgeschlossene_module <= 0:
            return

        st.subheader("Erfolgsmoment")
        st.success(
            f"Es wurden bereits {dashboard_daten.abgeschlossene_module} Modul(e) erfolgreich abgeschlossen. 🏆"
        )

        if "erfolg_animation_gezeigt" not in st.session_state:
            st.session_state["erfolg_animation_gezeigt"] = False

        if not st.session_state["erfolg_animation_gezeigt"]:
            st.balloons()
            st.session_state["erfolg_animation_gezeigt"] = True