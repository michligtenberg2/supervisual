# 🎬 Supervisual MegaTool Suite

**Supervisual MegaTool Suite** is een desktopapplicatie voor het maken van audio-reactieve video’s en beelden. Alles wat je nodig hebt zit in één app, met overzichtelijke tabbladen en een live preview-optie.

## 🚀 Features

* **🎛️ GUI met meerdere workflows**: Eén applicatie met tabbladen voor:

  * Video Effecten
  * Foto Spectrogrammen
  * MP4 Previews
  * MP4 Samenvoegen
* **🎨 Audio-reactieve effecten**: Visuele effecten die reageren op audio.
* **🖼️ Voor foto en video**: Ondersteunt zowel stilstaand beeld als video met externe audio.
* **⚡ Live preview**: Bekijk snel een korte versie van je gekozen effect en instellingen.
* **🛠️ Parameters instellen**: Verander kleur, transparantie, intensiteit en meer via sliders en kleurkiezers.
* **📂 Output beheren**: Kies je eigen bestandsnaam en outputlocatie.
* **🔄 Batch of interactief**: Render één video of meerdere tegelijk.
* **📊 Voortgang en log**: Altijd zicht op wat de app doet.

## 🖥️ Tabbladen

* **🎬 Video Effect**: Voeg een audio-reactief effect toe aan een video. Kies kleur, intensiteit en bijbehorende audio.
* **🖼️ Photo Spectrogram**: Genereer een korte video van een foto met spectrogram en optionele vervorming.
* **🎞️ MP4 Preview**: Maak een korte MP4 met een voorbeeld van het gekozen effect.
* **➕ MP4 Samenvoegen**: Combineer meerdere MP4’s tot één doorlopende video.

## 🧩 Beschikbare effecten

* Lissajous
* Waveform Rings
* Oscilloscope
* Fractal Flames
* Spectrogram
* Pulse Flashes
* ASCII
* Matrix Rain
* Rotating Shapes
* Photo Spectrogram (met face warping)

## ⚙️ Installatie

1. Clone de repository:

   ```bash
   git clone <repo-url>
   ```
2. Maak een virtuele omgeving aan:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. Installeer de vereiste dependencies:

   ```bash
   pip install -r requirements.txt
   ```
4. Start de applicatie:

   ```bash
   python3 main.py
   ```

## 📁 Mappenstructuur

* `gui/` – GUI-bestanden (PyQt6)
* `engine/` – De logica voor rendering en verwerking
* `effects/` – Alle losse visuele effecten
* `output/` – Gerenderde bestanden
* `previews/` – Previewbestanden

## 📝 Overig

* Outputbestanden worden standaard opgeslagen in de juiste map (tenzij je zelf een andere kiest).
* Voortgangsbalk en logvenster zijn altijd zichtbaar onderin.
---

Veel succes (en misschien wat plezier) met Supervisual.

*Voor bugs of ideeën: open een issue op GitHub.*

---

Laat gerust weten als je nog een bepaalde stijl of toon zoekt (serieuzer, technischer, of juist informeler).
