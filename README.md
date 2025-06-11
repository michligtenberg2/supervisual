# 🌀 Supervisual Engine – Projectoverzicht

## 🎯 Doel
Een modulaire, visueel veelzijdige audio-reactieve video-engine bouwen die uiteindelijk kan worden uitgebreid met een GUI, presets, en een volledige visuele stijl per audio/video.

---

python main.py jouwvideo.mp4 --effects waveform_rings --color "#FF00AA" --opacity 0.6


## 📁 Structuur

```
supervisual/
├── main.py                 # CLI entrypoint
├── engine.py               # Visual orchestratie
├── audio.py                # Beatdetectie, RMS, extractie
├── video.py                # Rendering en compositing
├── effects/
│   ├── lissajous.py 
│   ├── waveform_rings.py
│   ├── oscilloscope.py
│   ├── fractal_flames.py
│   ├── spectrogram.py
│   ├── pulse_flashes.py
│   ├── ascii.py
│   ├── rotating_shapes.py
│   ├── color_explosions.py
│   └── matrix_rain.py
```

---

## 🧩 Effecten (10 totaal)
✅ - ✅ Lissajous           
✅ - 🔄 Waveform-rings
✅ - 🔁 Oscilloscope met glow
✅ - 🔥 Fractal audio flames
✅ - 📈 Spectrogram scroll
✅ - ⚡ Pulse flashes (beat synced)
✅ - 🔤 ASCII shapes
✅ - 📐 Geometrische rotaties
✅ - 💥 Kleurexplosies op pieken
✅ - 🧬 Matrix regen

---

## 🖥️ GUI (later)
Gebaseerd op **Dear PyGui** met:
- Video-preview
- Effect-selectie
- Sliders voor transparantie en instellingen
- Render/exportknop
- Brutalistische stijl (zwart, wit, monospace)

---

## 📦 Export
- Output: `final_output.mp4`
- Transparantie: `--opacity`
- Effecten: `--effects lissajous,ascii`
- Framerate: `--fps 30`

---

## 🧱 Volgende stappen
- [ ] Effectmodules 1–10 implementeren
- [ ] Engine koppelen
- [ ] CLI testbaar maken
- [ ] Daarna: GUI bouwen

---

Gemaakt met ❤️ door M.L. Lentz + A.B. Iskander
