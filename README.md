# 🎬 Supervisual MegaTool Suite

**Supervisual MegaTool Suite** is een desktopapp voor het maken van audio-reactieve video’s en beelden. Alles zit in één overzichtelijke interface, verdeeld over meerdere tabbladen met live preview.

> 🇬🇧 [Read this in English](README.en.md)

## Features

- **Meerdere workflows in één app**  
  Tabbladen voor:
  - Video-effecten
  - Spectrogrammen op foto’s
  - MP4-previews
  - MP4’s samenvoegen

- **Audio-reactieve visuals**  
  Effecten reageren op het geluid dat je kiest.

- **Voor zowel video als beeld**  
  Werkt met stilstaand beeld of video, beide met audio.

- **Live preview**  
  Bekijk direct een korte versie van je instellingen.

- **Effectinstellingen aanpassen**  
  Kleur, intensiteit, transparantie, etc. via sliders en kleurkiezers.

- **Batch of handmatig renderen**  
  Eén bestand of meerdere tegelijk.

- **Output en voortgang**  
  Stel bestandsnaam en map in, voortgangsbalk en log zichtbaar.

## Tabbladen

- **Video Effect** – Voeg een visueel effect toe aan een video.
- **Photo Spectrogram** – Maak een korte video van een foto + spectrogram.
- **MP4 Preview** – Snelvoorbeeld van een effect.
- **MP4 Samenvoegen** – Voeg meerdere MP4’s samen tot één video.

## Beschikbare effecten

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

## Installatie

```bash
git clone https://github.com/michligtenberg2/supervisual.git
cd supervisual
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 main.py
```

## Mappenstructuur

- `gui/` – GUI-code (PyQt6)  
- `engine/` – Render- en verwerkingslogica  
- `effects/` – Losse effecten  
- `output/` – Gerenderde video’s  
- `previews/` – Previewfragmenten

## Overig

- Output gaat automatisch naar de juiste map (tenzij je iets anders kiest).
- Log en voortgang zijn altijd zichtbaar onderin het scherm.

---

Gebruik je het, vind je een bug, of heb je een idee? Open gerust een issue op GitHub.
