"""Baut die Installationsanleitung als PDF."""
from __future__ import annotations

import io
import os

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    KeepTogether,
    ListFlowable,
    ListItem,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

OUT = r"J:\Claude\hass-anycubic_cloud_v3\docs\Anycubic-HA-Integration-Installationsanleitung.pdf"
REPO = "https://github.com/sunnyfunny1977-alt/hass-anycubic_cloud_v3"
VERSION = io.open(r"J:\Claude\hass-anycubic_cloud_v3\Version", encoding="utf-8").read().strip()

ACCENT = colors.HexColor("#0F6FC6")
DARK = colors.HexColor("#1F2933")
MUTED = colors.HexColor("#5B6770")
RULE = colors.HexColor("#D6DBE0")
CODEBG = colors.HexColor("#F3F5F7")
WARNBG = colors.HexColor("#FFF6E5")
WARNBORDER = colors.HexColor("#E0A800")

ss = getSampleStyleSheet()


def st(name, **kw):
    base = kw.pop("parent", ss["Normal"])
    return ParagraphStyle(name, parent=base, **kw)


S_TITLE = st("t", fontName="Helvetica-Bold", fontSize=22, leading=26, textColor=DARK, spaceAfter=2)
S_SUB = st("s", fontName="Helvetica", fontSize=11.5, leading=15, textColor=MUTED, spaceAfter=10)
S_H1 = st("h1", fontName="Helvetica-Bold", fontSize=14, leading=18, textColor=ACCENT,
          spaceBefore=14, spaceAfter=5)
S_H2 = st("h2", fontName="Helvetica-Bold", fontSize=11, leading=14, textColor=DARK,
          spaceBefore=9, spaceAfter=3)
S_BODY = st("b", fontSize=9.7, leading=13.6, textColor=DARK, alignment=TA_LEFT, spaceAfter=5)
S_SMALL = st("sm", fontSize=8.6, leading=12, textColor=MUTED, spaceAfter=4)
S_CODE = st("c", fontName="Courier", fontSize=8.4, leading=11.4, textColor=DARK,
            backColor=CODEBG, borderPadding=6, spaceBefore=3, spaceAfter=6,
            leftIndent=2, rightIndent=2)
S_LI = st("li", fontSize=9.7, leading=13.4, textColor=DARK, spaceAfter=2)
S_WARN = st("w", fontSize=9.7, leading=13.6, textColor=DARK)
S_TH = st("th", fontName="Helvetica-Bold", fontSize=8.8, leading=11.5, textColor=colors.white)
S_TD = st("td", fontSize=8.8, leading=11.5, textColor=DARK)


def P(txt, style=S_BODY):
    return Paragraph(txt, style)


def code(txt):
    return Paragraph(txt.replace("&", "&amp;").replace("<", "&lt;").replace("\n", "<br/>"), S_CODE)


def bullets(items, style=S_LI):
    return ListFlowable(
        [ListItem(Paragraph(i, style), leftIndent=10) for i in items],
        bulletType="bullet", bulletFontSize=7, bulletOffsetY=1,
        leftIndent=12, spaceAfter=6,
    )


def steps(items):
    return ListFlowable(
        [ListItem(Paragraph(i, S_LI), leftIndent=12) for i in items],
        bulletType="1", bulletFormat="%s.", leftIndent=15, spaceAfter=6,
    )


def notebox(title, body_html):
    inner = [Paragraph(f"<b>{title}</b>", S_WARN), Spacer(1, 3), Paragraph(body_html, S_WARN)]
    t = Table([[inner]], colWidths=[165 * mm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), WARNBG),
        ("BOX", (0, 0), (-1, -1), 0.9, WARNBORDER),
        ("LEFTPADDING", (0, 0), (-1, -1), 9),
        ("RIGHTPADDING", (0, 0), (-1, -1), 9),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
    ]))
    return t


def table(rows, widths):
    data = [[Paragraph(c, S_TH) for c in rows[0]]]
    data += [[Paragraph(c, S_TD) for c in r] for r in rows[1:]]
    t = Table(data, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), ACCENT),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F7F9FA")]),
        ("GRID", (0, 0), (-1, -1), 0.4, RULE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    return t


def decorate(canvas, doc):
    canvas.saveState()
    w, h = A4
    canvas.setStrokeColor(RULE)
    canvas.setLineWidth(0.6)
    canvas.line(22 * mm, h - 16 * mm, w - 22 * mm, h - 16 * mm)
    canvas.setFont("Helvetica", 7.6)
    canvas.setFillColor(MUTED)
    canvas.drawString(22 * mm, h - 13.5 * mm, "Anycubic Home Assistant Integration - Installationsanleitung")
    canvas.drawRightString(w - 22 * mm, h - 13.5 * mm, f"Version {VERSION}")
    canvas.line(22 * mm, 15 * mm, w - 22 * mm, 15 * mm)
    canvas.drawString(22 * mm, 11 * mm, REPO)
    canvas.drawRightString(w - 22 * mm, 11 * mm, f"Seite {doc.page}")
    canvas.restoreState()


story = []
A = story.append

A(P("Anycubic Home Assistant Integration", S_TITLE))
A(P(f"Installationsanleitung fuer den Fork von sunnyfunny1977-alt &middot; Version {VERSION}", S_SUB))

A(P(f'<b>Repository:</b> <font color="#0F6FC6"><a href="{REPO}">{REPO}</a></font>', S_BODY))
A(P("Diese Anleitung beschreibt Installation, Einrichtung und die Uebernahme des mitgelieferten "
    "Muster-Dashboards. Sie richtet sich an Anwender mit einer laufenden Home-Assistant-Installation.", S_BODY))

# 1
A(P("1. Herkunft und Danksagung", S_H1))
A(P("Diese Integration ist ein Fork. Sie ist nicht in Eigenleistung entstanden, sondern baut auf der "
    "Arbeit anderer auf. Der Dank gilt:", S_BODY))
A(bullets([
    '<b>WaresWichall</b> &ndash; Original-Entwicklung der Anycubic-Cloud-Integration '
    '(<font color="#0F6FC6"><a href="https://github.com/WaresWichall/hass-anycubic_cloud">'
    'github.com/WaresWichall/hass-anycubic_cloud</a></font>) sowie der zugehoerigen Dashboard-Card.',
    '<b>ljschmitt</b> &ndash; der Fork, auf dem dieser aufbaut, mit Fehlerkorrekturen, deutschen Texten '
    'und MQTT-Erweiterungen '
    '(<font color="#0F6FC6"><a href="https://github.com/ljschmitt/hass-anycubic_cloud_v3">'
    'github.com/ljschmitt/hass-anycubic_cloud_v3</a></font>).',
    '<b>sunnyfunny1977-alt</b> &ndash; dieser Fork, mit den ACE-Erweiterungen: ein Sensor je Filament-Slot '
    'und die dauerhafte Anzeige des aktiven Filaments.',
]))
A(P("Lizenz: GNU General Public License v3.0, wie bei den Vorgaengern.", S_SMALL))
A(notebox(
    "Eigene Versionslinie",
    "Dieses Repository zaehlt seit 1.0.0 eigenstaendig. Releases mit gleicher Nummer aus "
    "<b>ljschmitt/hass-anycubic_cloud_v3</b> enthalten <b>nicht</b> denselben Code. Bei Fragen oder "
    "Problemen bitte immer angeben, aus welchem Repository die Installation stammt."))

# 2
A(P("2. Voraussetzungen", S_H1))
A(table([
    ["Was", "Anforderung"],
    ["Home Assistant", "2025.10.0 oder neuer. Getestet mit 2026.6.1."],
    ["HACS", "Fuer die empfohlene Installation als benutzerdefiniertes Repository."],
    ["Anycubic-Konto", "Dasselbe Konto, mit dem der Drucker in der Anycubic Cloud registriert ist."],
    ["Zugriffstoken", "Fuer MQTT-Echtzeitupdates wird der Access-Token von <b>Slicer Next (Windows)</b> "
                      "benoetigt. Ohne ihn funktioniert die Integration nur mit Cloud-Abfrage im "
                      "Minutentakt."],
    ["button-card", "HACS-Frontend-Card, nur fuer das Muster-Dashboard erforderlich."],
], [38 * mm, 127 * mm]))

# 3
A(P("3. Installation ueber HACS (empfohlen)", S_H1))
A(steps([
    "In Home Assistant <b>HACS</b> oeffnen, dann <b>Integrationen</b>.",
    "Ueber das Drei-Punkte-Menue <b>Benutzerdefinierte Repositories</b> waehlen.",
    f"Als Repository <font face='Courier'>{REPO}</font> eintragen, als Kategorie <b>Integration</b>.",
    "Hinzufuegen, danach in HACS nach <b>Anycubic HA Integration</b> suchen und installieren.",
    "Home Assistant <b>neu starten</b>.",
]))

A(KeepTogether([
    P("Manuelle Installation (Alternative)", S_H2),
    P("Wer HACS nicht nutzt, kopiert den Ordner aus dem Repository direkt in die Konfiguration und "
      "startet Home Assistant neu:", S_BODY),
    code("custom_components/anycubic_ha_integration/\n  ->  <HA-Konfiguration>/custom_components/anycubic_ha_integration/"),
]))
A(P("Wichtig: den Ordner immer <b>vollstaendig</b> kopieren. Eine unvollstaendige Kopie, bei der "
    "beispielsweise die Uebersetzungsdateien fehlen, fuehrt zu Entitaeten ohne Namen und zu "
    "unbrauchbaren Entity-IDs.", S_SMALL))

# 4
A(P("4. Zugriffstoken auslesen", S_H1))
A(P("Fuer MQTT-Echtzeitupdates wird der Access-Token aus Anycubic Slicer Next benoetigt. Das "
    "Repository enthaelt dafuer ein PowerShell-Skript:", S_BODY))
A(code("scripts/anycubic-token.ps1"))
A(P("Slicer Next starten und eingeloggt lassen, dann das Skript in PowerShell ausfuehren. Es "
    "durchsucht alle Logdateien, waehlt den zeitlich neuesten Token, legt ihn in die Zwischenablage "
    "und meldet Quelldatei, Zeitstempel und Zeichenzahl. Wird kein Token gefunden, bricht es mit einer "
    "klaren Meldung ab.", S_BODY))
A(P("Alternativ gibt es den Web-Login ueber die Anycubic Cloud. Dieser Weg unterstuetzt <b>kein</b> "
    "MQTT und liefert nur Aktualisierungen im Minutentakt.", S_SMALL))

# 5
A(P("5. Integration einrichten", S_H1))
A(steps([
    "<b>Einstellungen -> Geraete &amp; Dienste -> Integration hinzufuegen</b>.",
    "<b>Anycubic HA Integration</b> auswaehlen.",
    "Als Authentifizierungsmodus <b>Slicer Next (Windows)</b> waehlen und den Token einfuegen.",
    "Die zu ueberwachenden Drucker auswaehlen.",
]))
A(P("Nach dem Abschluss legt die Integration ein Geraet je Drucker an, mit Sensoren fuer Status, "
    "Temperaturen, Druckfortschritt, Luefter sowie ACE-Slots und aktivem Filament.", S_BODY))

# 6
A(P("6. Muster-Dashboard einbinden", S_H1))
A(P("Das Repository enthaelt ein vollstaendiges Beispiel-Dashboard:", S_BODY))
A(code("examples/dashboard-kobra-s1.yaml"))
A(P("Es zeigt Kamerabild, Druckfortschritt, Temperaturen, die vier ACE-Slots mit Farbringen, das "
    "aktive Filament, Luefter, Geschwindigkeit und Firmware-Stand.", S_BODY))
A(P("Vorbereitung", S_H2))
A(bullets([
    "In HACS die Frontend-Card <b>button-card</b> installieren. Ohne sie bleiben die meisten Karten leer.",
    "Optional drei Template-Helfer fuer die Einblendung im Kamerabild und zwei "
    "<font face='Courier'>input_number</font>-Helfer fuer die Temperatur-Feinjustierung. "
    "Die genauen Namen stehen im Kopf der YAML-Datei.",
]))
A(P("Uebernehmen", S_H2))
A(steps([
    "Dashboard oeffnen, oben rechts auf den <b>Stift</b>.",
    "Drei-Punkte-Menue -> <b>Raw-Konfigurationseditor</b>.",
    "Den Inhalt der YAML-Datei unter <font face='Courier'>views:</font> einhaengen und speichern.",
]))

A(notebox(
    "Das Dashboard muss angepasst werden",
    "Es ist eine <b>Vorlage</b>, kein fertiges Produkt. Vor der Nutzung sind mindestens zwei Dinge "
    "anzupassen:<br/><br/>"
    "<b>1. Entity-IDs.</b> Die IDs enthalten den Druckernamen, in der Vorlage "
    "<font face='Courier'>anycubic_kobra_s1</font>. Heisst der Drucker anders, diesen Teil vor dem "
    "Einfuegen per Suchen-und-Ersetzen austauschen.<br/><br/>"
    "<b>2. Die Kamera.</b> Siehe naechster Abschnitt."))

# 7
A(P("7. Die Kamera ist eine externe Kamera", S_H1))
A(P("Das ist der Punkt, der am haeufigsten missverstanden wird: <b>Die Kameraflaeche im Muster-Dashboard "
    "zeigt nicht den Anycubic-Cloudstream.</b>", S_BODY))
A(P("Der Cloudstream laeuft ueber Agora-RTC, ist verschluesselt und benoetigt das Agora-Browser-SDK. "
    "Er laesst sich technisch nicht als Home-Assistant-<font face='Courier'>camera</font>-Entity "
    "abbilden und bleibt deshalb dem mitgelieferten Anycubic-Panel vorbehalten. Auf einem normalen "
    "Dashboard ist er nicht verfuegbar.", S_BODY))
A(P("Im Originalaufbau haengt an dieser Stelle daher eine <b>separate Kamera: eine SONOFF CAM-S1</b>, "
    "die als eigene Entity in Home Assistant eingebunden ist und auf den Drucker gerichtet steht. "
    "Jede beliebige Kamera funktioniert genauso, solange sie eine "
    "<font face='Courier'>camera</font>-Entity bereitstellt, etwa eine MJPEG- oder RTSP-Kamera oder die "
    "integrierte Drucker-Webcam unter alternativer Firmware wie Rinkhals.", S_BODY))
A(P("In der YAML-Datei steht dafuer der Platzhalter:", S_BODY))
A(code("camera.drucker_kamera"))
A(P("Diesen durch die eigene Kamera-Entity ersetzen. Ohne passende Entity bleibt die Flaeche leer; der "
    "Rest des Dashboards funktioniert davon unabhaengig weiter.", S_BODY))

# 8
A(P("8. Bewusst nur Anzeige, keine Bedienung", S_H1))
A(P("Das Muster-Dashboard ist absichtlich als <b>Anzeigetafel</b> ausgelegt. Nahezu alle Karten sind mit "
    "<font face='Courier'>tap_action: none</font> konfiguriert und reagieren nicht auf Beruehrung. Ein "
    "versehentlicher Fingertipp auf dem Tablet kann am Drucker also nichts verstellen: Es laesst sich "
    "kein Druck starten, pausieren oder abbrechen und keine Temperatur an den Drucker senden.", S_BODY))
A(P("Was tatsaechlich bedienbar ist:", S_H2))
A(table([
    ["Element", "Verhalten"],
    ["Kamera-Licht", "Echter Schalter. Schaltet das Licht am Drucker."],
    ["Firmware-Kacheln", "Oeffnen den Home-Assistant-Update-Dialog. Von dort liesse sich eine "
                         "Firmware-Aktualisierung anstossen."],
    ["Temperatur-Feinjustierung", "Aendert nur lokale Home-Assistant-Helfer. Ohne eigene Automation, "
                                  "die diese Werte weiterreicht, passiert am Drucker nichts. Solche "
                                  "Automationen sind im Muster <b>nicht</b> enthalten."],
    ["Job-Vorschau, ETA", "Oeffnen lediglich das Detailfenster der Entitaet."],
    ["Alles Uebrige", "Reine Anzeige, ohne Funktion bei Beruehrung."],
], [42 * mm, 123 * mm]))

# 9
A(P("9. Jeder darf es umbauen", S_H1))
A(P("Die Beschraenkung auf Anzeige ist eine <b>persoenliche Entscheidung</b> des Autors dieses Musters, "
    "keine Vorgabe und keine technische Grenze der Integration. Wer Bedienelemente moechte, baut sie "
    "ein.", S_BODY))
A(P("Um eine Karte bedienbar zu machen, genuegt es, ihre Aktion zu aendern:", S_BODY))
A(code("tap_action:\n  action: none        # gesperrt\n\ntap_action:\n  action: toggle      # schaltet\n  # oder: more-info, perform-action, navigate"))
A(P("Die Integration selbst stellt Dienste fuer Druckstart, Pause, Fortsetzen, Abbruch, ACE-Slot-"
    "Verwaltung und Spulentrocknung bereit. Sie lassen sich ueber Schaltflaechen, Automationen oder "
    "Skripte nutzen. Das Muster-Dashboard schoepft das bewusst nicht aus.", S_BODY))
A(P("Ebenso frei sind Farben, Anordnung und Umfang. Nicht benoetigte Abschnitte koennen ersatzlos "
    "geloescht werden, die Abschnitte sind voneinander unabhaengig.", S_BODY))

# 10
A(P("10. Hinweise und Haftung", S_H1))
A(bullets([
    "Die Integration kommuniziert mit den Anycubic-Cloud-Diensten und kann Druckerfunktionen steuern. "
    "Nutzung auf eigene Gefahr, Steuerfunktionen bitte kontrolliert testen.",
    "Tokens, Zugangsdaten, Drucker-IDs, Seriennummern, MAC-Adressen und private IP-Adressen niemals in "
    "oeffentlichen Issues veroeffentlichen.",
    "Ein Drucker sollte nicht unbeaufsichtigt betrieben werden, unabhaengig von der Fernueberwachung.",
]))
A(Spacer(1, 6))
A(P(f'Fragen, Fehlerberichte und Verbesserungen: <font color="#0F6FC6">'
    f'<a href="{REPO}/issues">{REPO}/issues</a></font>', S_BODY))

os.makedirs(os.path.dirname(OUT), exist_ok=True)
doc = BaseDocTemplate(OUT, pagesize=A4,
                      leftMargin=22 * mm, rightMargin=22 * mm,
                      topMargin=22 * mm, bottomMargin=20 * mm,
                      title="Anycubic HA Integration - Installationsanleitung",
                      author="sunnyfunny1977-alt", subject="Installation und Muster-Dashboard")
frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="f")
doc.addPageTemplates([PageTemplate(id="main", frames=[frame], onPage=decorate)])
doc.build(story)
print("PDF geschrieben:", OUT)
