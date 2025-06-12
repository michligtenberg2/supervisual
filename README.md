# 🎬 Supervisual MegaTool Suite

Welkom bij **Supervisual MegaTool Suite** – dé alles-in-één desktopapplicatie voor audio-reactieve video- en foto-effecten! Met een moderne, gebruiksvriendelijke interface en krachtige batch- en preview-workflows.

## 🚀 Belangrijkste Features

- **🎛️ MegaTool GUI**: Eén overzichtelijke app met tabbladen voor alle workflows:
  - Video Effecten
  - Foto Spectrogrammen
  - MP4 Previews
  - MP4 Samenvoegen
- **🎨 Audio-reactieve effecten**: Kies uit diverse visuele effecten die reageren op muziek of geluid.
- **🖼️ Foto & Video**: Overlay effecten op zowel foto's als video's, met ondersteuning voor externe audio.
- **⚡ Live Preview**: Bekijk direct een korte preview van je gekozen effect en instellingen.
- **🛠️ Effect Parameters**: Pas sterkte, kleur, transparantie en meer aan met sliders en kleurkiezers.
- **📂 Outputbeheer**: Kies eenvoudig je output-bestand en alle resultaten worden netjes opgeslagen.
- **🔄 Batch & Interactief**: Zowel snelle previews als volledige video-rendering mogelijk.
- **📊 Voortgangsbalk & Log**: Altijd zicht op de voortgang en log van je bewerkingen.

## 🖥️ Tabbladen in de MegaTool

- **🎬 Video Effect**: Voeg audio-reactieve overlays toe aan video's. Kies effect, kleur, audio, output en effectsterkte.
- **🖼️ Photo Spectrogram**: Maak een MP4 van een foto met spectrogram-overlay en audio-reactieve vervorming.
- **🎞️ MP4 Preview**: Genereer snel een korte MP4-preview van een effect op audio.
- **➕ MP4 Concatenation**: Plak meerdere MP4-bestanden samen tot één video.

## 🧩 Effecten

- Lissajous
- Waveform Rings
- Oscilloscope
- Fractal Flames
- Spectrogram
- Pulse Flashes
- ASCII
- Matrix Rain
- Rotating Shapes
- Photo Spectrogram (met face warping)

## ⚙️ Installatie

1. **Clone de repo**
2. Maak een virtuele omgeving aan:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. Installeer de vereiste packages:
   ```bash
   pip install -r requirements.txt
   ```
4. Start de MegaTool:
   ```bash
   python3 main.py
   ```

## 📁 Mappenstructuur

- `gui/` – Alle PyQt6 GUI modules
- `engine/` – Kernlogica voor rendering en audio/video verwerking
- `effects/` – Alle losse effectmodules
- `output/` – Renderresultaten
- `previews/` – Previewvideo's

## 📝 Overig

- Alle output wordt standaard opgeslagen in de juiste map, tenzij je zelf een pad kiest.
- De voortgangsbalk en log zijn altijd zichtbaar onderin de app.
- De app is volledig Nederlandstalig en geschikt voor zowel beginners als gevorderden.

---

Veel plezier met Supervisual! 🎉

*Vragen, bugs of feature requests? Maak een issue aan op GitHub!*
