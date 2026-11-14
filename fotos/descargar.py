# Descarga las fotos listadas en fotos/lista.txt (slug|Archivo_en_Wikimedia_Commons)
# y las guarda como fotos/<slug>.jpg (máx. 800 px). Se ejecuta en GitHub Actions.
import io, time, urllib.parse, urllib.request, pathlib
from PIL import Image
UA = "ElMercaditoCatalogo/1.0 (GitHub Actions)"
fotos = pathlib.Path("fotos")
for linea in (fotos / "lista.txt").read_text(encoding="utf-8").splitlines():
    if "|" not in linea: continue
    slug, archivo = [x.strip() for x in linea.split("|", 1)]
    destino = fotos / f"{slug}.jpg"
    if destino.exists(): continue
    url = "https://commons.wikimedia.org/wiki/Special:FilePath/" + urllib.parse.quote(archivo) + "?width=800"
    for intento in range(3):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            img = Image.open(io.BytesIO(urllib.request.urlopen(req, timeout=60).read()))
            if img.mode in ("RGBA", "LA", "P"):
                img = img.convert("RGBA"); fondo = Image.new("RGB", img.size, "white")
                fondo.paste(img, mask=img.split()[-1]); img = fondo
            img = img.convert("RGB"); img.thumbnail((800, 800))
            img.save(destino, "JPEG", quality=80, optimize=True)
            print("ok", slug); break
        except Exception as e:
            print("reintento", slug, e); time.sleep(5)
    time.sleep(1)
