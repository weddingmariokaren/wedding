#!/usr/bin/env python3
"""Generate a branded wedding QR card matching the Karen & Mario floral theme."""
import io, os, math
import qrcode
import qrcode.image.base
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
URL  = "https://weddingmariokaren.github.io/wedding/"
OUT  = os.path.join(HERE, "wedding-gift-QR.png")
PHOTO = os.path.join(HERE, "photo_web.jpeg")

# ── card dimensions (portrait, printable at ~4x6 in @300dpi) ─────────────────
W, H = 1200, 2200
CARD = Image.new("RGBA", (W, H), (253, 248, 240, 255))
draw = ImageDraw.Draw(CARD)

# ── 1. hero photo (top half) ──────────────────────────────────────────────────
photo = Image.open(PHOTO).convert("RGBA")
ph = int(H * 0.48)
pw = W
ratio = photo.width / photo.height
if pw / ph > ratio:
    pw = int(ph * ratio)
else:
    ph = int(pw / ratio)
photo = photo.resize((pw, ph), Image.LANCZOS)
# centre crop to full width
px = (W - pw) // 2
CARD.paste(photo, (px, 0), photo)

# soft gradient fade at the bottom of the photo into the card background
fade_h = 180
fade = Image.new("RGBA", (W, fade_h))
for y in range(fade_h):
    alpha = int(255 * (y / fade_h))
    fade_draw = ImageDraw.Draw(fade)
    fade_draw.line([(0, y), (W, y)], fill=(253, 248, 240, alpha))
CARD.alpha_composite(fade, (0, ph - fade_h))

# ── 2. decorative divider line ────────────────────────────────────────────────
def draw_fancy_line(draw, y, color=(214, 170, 180)):
    lx0, lx1 = 80, W - 80
    mid = W // 2
    draw.line([(lx0, y), (mid - 70, y)], fill=color, width=3)
    draw.line([(mid + 70, y), (lx1, y)], fill=color, width=3)
    r = 18
    draw.ellipse([(mid - r, y - r), (mid + r, y + r)], outline=color, width=3)
    draw.ellipse([(mid - 7, y - 7), (mid + 7, y + 7)], fill=color)

sep_y = ph + 36
draw_fancy_line(draw, sep_y)

# ── 3. "Wedding" pill tag ─────────────────────────────────────────────────────
pill_text = "Wedding"
pill_w, pill_h = 280, 72
pill_x = (W - pill_w) // 2
pill_y = sep_y + 28
draw.rounded_rectangle(
    [(pill_x, pill_y), (pill_x + pill_w, pill_y + pill_h)],
    radius=36, fill=(245, 228, 210, 255)
)

# ── font helper ───────────────────────────────────────────────────────────────
def font(size, bold=False):
    families = [
        "C:/Windows/Fonts/Georgia.ttf",
        "C:/Windows/Fonts/georgiab.ttf" if bold else "C:/Windows/Fonts/Georgia.ttf",
        "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/calibri.ttf",
    ]
    for p in families:
        if os.path.exists(p):
            try: return ImageFont.truetype(p, size)
            except: pass
    return ImageFont.load_default()

f_pill   = font(34, bold=False)
f_names  = font(62, bold=False)
f_tagline= font(36, bold=False)
f_body   = font(34, bold=False)
f_small  = font(28, bold=False)

def centre_text(draw, text, y, fnt, color):
    bb = draw.textbbox((0, 0), text, font=fnt)
    tw = bb[2] - bb[0]
    draw.text(((W - tw) // 2, y), text, font=fnt, fill=color)
    return bb[3] - bb[1]  # height

centre_text(draw, pill_text, pill_y + 18, f_pill, (90, 60, 50))

# ── 4. Names banner ───────────────────────────────────────────────────────────
banner_y = pill_y + pill_h + 30
banner_h = 100
draw.rounded_rectangle(
    [(60, banner_y), (W - 60, banner_y + banner_h)],
    radius=28, fill=(248, 234, 228, 255)
)
centre_text(draw, "Karen & Mario's Wedding Day", banner_y + 20, f_names, (70, 44, 38))

# ── 5. QR code ────────────────────────────────────────────────────────────────
qr = qrcode.QRCode(
    version=None,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=12,
    border=2,
)
qr.add_data(URL)
qr.make(fit=True)
qr_img = qr.make_image(fill_color=(55, 36, 30), back_color=(255, 255, 255)).convert("RGBA")

# white card behind QR
qr_size = 520
qr_img = qr_img.resize((qr_size, qr_size), Image.NEAREST)
card_pad = 28
qr_card_size = qr_size + card_pad * 2
qr_bg = Image.new("RGBA", (qr_card_size, qr_card_size), (255, 255, 255, 255))
# rounded corners mask
mask = Image.new("L", (qr_card_size, qr_card_size), 0)
ImageDraw.Draw(mask).rounded_rectangle(
    [(0, 0), (qr_card_size - 1, qr_card_size - 1)], radius=32, fill=255
)
rounded_bg = Image.new("RGBA", (qr_card_size, qr_card_size), (0, 0, 0, 0))
rounded_bg.paste(qr_bg, mask=mask)
qr_bg_draw = ImageDraw.Draw(rounded_bg)

# shadow
shadow = Image.new("RGBA", (qr_card_size + 20, qr_card_size + 20), (0, 0, 0, 0))
shadow_draw = ImageDraw.Draw(shadow)
shadow_draw.rounded_rectangle(
    [(10, 10), (qr_card_size + 9, qr_card_size + 9)], radius=36, fill=(0, 0, 0, 60)
)
shadow = shadow.filter(ImageFilter.GaussianBlur(10))

qr_x = (W - qr_card_size) // 2
qr_y = banner_y + banner_h + 50
CARD.alpha_composite(shadow, (qr_x - 10, qr_y - 10))
CARD.alpha_composite(rounded_bg, (qr_x, qr_y))
CARD.alpha_composite(qr_img, (qr_x + card_pad, qr_y + card_pad))

# ── 6. Scan prompt pill ───────────────────────────────────────────────────────
scan_text = "Scan QR To Send Gifts & Wishes"
scan_y = qr_y + qr_card_size + 36
scan_pill_w, scan_pill_h = 760, 76
scan_x = (W - scan_pill_w) // 2
draw.rounded_rectangle(
    [(scan_x, scan_y), (scan_x + scan_pill_w, scan_y + scan_pill_h)],
    radius=38, fill=(245, 228, 210, 255)
)
bb = draw.textbbox((0, 0), scan_text, font=f_tagline)
tw = bb[2] - bb[0]
draw.text(((W - tw) // 2, scan_y + 20), scan_text, font=f_tagline, fill=(70, 44, 38))

# ── 7. "Hosted by" line ───────────────────────────────────────────────────────
host_y = scan_y + scan_pill_h + 42
centre_text(draw, "HOSTED BY MARIO & KAREN", host_y, f_body, (60, 45, 38))

# ── 8. URL footnote ───────────────────────────────────────────────────────────
url_y = host_y + 56
centre_text(draw, URL, url_y, f_small, (160, 130, 120))

# ── 9. Bottom floral accent (simple coloured dots) ───────────────────────────
accent_y = url_y + 68
colors = [(217, 79, 135), (124, 139, 95), (217, 79, 135), (124, 139, 95), (217, 79, 135)]
positions = [W//2 - 80, W//2 - 40, W//2, W//2 + 40, W//2 + 80]
for cx, col in zip(positions, colors):
    r = 8
    draw.ellipse([(cx - r, accent_y - r), (cx + r, accent_y + r)], fill=col)

# ── save ──────────────────────────────────────────────────────────────────────
final = CARD.convert("RGB")
final.save(OUT, "PNG", dpi=(300, 300), optimize=True)
print(f"Saved: {OUT}  ({os.path.getsize(OUT)//1024} KB)")
