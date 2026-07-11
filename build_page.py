#!/usr/bin/env python3
"""Generate a self-contained wedding gift info page (single HTML file)."""
import base64, io, os
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "photo_web.jpeg")
OUT = os.path.join(HERE, "wedding-gifts.html")

EMAIL = "weddingmariokaren@gmail.com"

# --- optimize the hero photo for fast mobile loading ---
img = Image.open(SRC).convert("RGB")
max_w = 900
if img.width > max_w:
    img = img.resize((max_w, round(img.height * max_w / img.width)), Image.LANCZOS)
buf = io.BytesIO()
img.save(buf, format="JPEG", quality=82, optimize=True)
b64 = base64.b64encode(buf.getvalue()).decode("ascii")
data_uri = f"data:image/jpeg;base64,{b64}"
print(f"Embedded photo: {len(buf.getvalue())//1024} KB")

HTML = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Karen &amp; Mario &mdash; Wedding Gift Contributions</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600&family=Dancing+Script:wght@600;700&family=Poppins:wght@300;400;500&display=swap" rel="stylesheet">
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    font-family: 'Poppins', sans-serif;
    background: #fbf3ea;
    background: linear-gradient(160deg, #fbf3ea 0%, #f4ead9 100%);
    color: #4a3b35; line-height: 1.6;
    display: flex; justify-content: center;
    padding: 24px 14px 48px; min-height: 100vh;
  }}
  .card {{
    width: 100%; max-width: 560px; background: #fffdf9;
    border-radius: 26px; overflow: hidden;
    box-shadow: 0 18px 50px rgba(120, 80, 60, 0.16);
    border: 1px solid #f0e2cf;
  }}
  .hero {{ width: 100%; display: block; }}
  .body {{ padding: 30px 26px 34px; text-align: center; }}
  .eyebrow {{
    display: inline-block; letter-spacing: 3px; text-transform: uppercase;
    font-size: 12px; font-weight: 500; color: #b06a86;
    background: #f7e6ec; padding: 7px 18px; border-radius: 999px; margin-bottom: 18px;
  }}
  .names {{ font-family: 'Dancing Script', cursive; font-size: 46px; color: #d94f87; line-height: 1.1; }}
  .date {{ font-family: 'Cormorant Garamond', serif; font-size: 20px; letter-spacing: 4px; color: #7a8b5f; margin-top: 4px; }}
  .rule {{ width: 64px; height: 2px; background: #e7b8ca; border: none; margin: 22px auto; border-radius: 2px; }}
  h1 {{ font-family: 'Cormorant Garamond', serif; font-size: 27px; font-weight: 600; color: #5a463f; margin-bottom: 10px; }}
  .lede {{ font-size: 15px; font-weight: 300; color: #6b5a52; max-width: 420px; margin: 0 auto 26px; }}
  .email-label {{ font-size: 12px; letter-spacing: 2px; text-transform: uppercase; color: #b06a86; margin-bottom: 8px; }}
  .email-box {{
    display: flex; align-items: center; justify-content: center; gap: 10px; flex-wrap: wrap;
    background: #f7f3ec; border: 1.5px dashed #d9b98f; border-radius: 16px;
    padding: 16px 18px; margin: 0 auto 12px; max-width: 440px;
  }}
  .email {{ font-size: 17px; font-weight: 500; color: #4a3b35; word-break: break-all; }}
  .copy-btn {{
    font-family: 'Poppins', sans-serif; font-size: 13px; font-weight: 500; cursor: pointer;
    background: #d94f87; color: #fff; border: none; border-radius: 999px; padding: 9px 18px;
    transition: background .2s, transform .1s;
  }}
  .copy-btn:hover {{ background: #c53d75; }}
  .copy-btn:active {{ transform: scale(.96); }}
  .copied {{ background: #7a8b5f !important; }}
  .note {{
    background: #eef3e6; border-radius: 14px; padding: 14px 18px; margin: 20px auto 0;
    max-width: 440px; font-size: 13.5px; color: #5c6b45;
  }}
  .note b {{ color: #46551f; }}
  .steps {{ text-align: left; max-width: 440px; margin: 26px auto 0; }}
  .steps h2 {{ font-family: 'Cormorant Garamond', serif; font-size: 20px; color: #5a463f; text-align: center; margin-bottom: 14px; }}
  .step {{ display: flex; gap: 12px; margin-bottom: 12px; font-size: 14px; font-weight: 300; color: #5a4a42; }}
  .num {{
    flex: 0 0 26px; height: 26px; background: #f7e6ec; color: #d94f87; border-radius: 50%;
    display: flex; align-items: center; justify-content: center; font-size: 13px; font-weight: 500;
  }}
  .thanks {{ font-family: 'Dancing Script', cursive; font-size: 26px; color: #d94f87; margin-top: 30px; }}
  .foot {{ font-size: 11px; color: #b6a99e; margin-top: 6px; }}
</style>
</head>
<body>
  <div class="card">
    <img class="hero" src="{data_uri}" alt="Karen and Mario - Save the Date, 02.08.2026">
    <div class="body">
      <span class="eyebrow">Wedding Gift Contributions</span>
      <div class="names">Karen &amp; Mario</div>
      <div class="date">02 . 08 . 2026</div>
      <hr class="rule">
      <h1>With love &amp; gratitude</h1>
      <p class="lede">Your presence is the greatest gift of all. For those who have kindly asked, contributions toward our new life together can be sent by Interac e-Transfer.</p>

      <div class="email-label">Send your e-Transfer to</div>
      <div class="email-box">
        <span class="email" id="email">{EMAIL}</span>
        <button class="copy-btn" id="copyBtn" onclick="copyEmail()">Copy</button>
      </div>

      <div class="note">
        <b>Autodeposit is enabled</b> &mdash; no security question needed, and there are <b>no fees</b>. Your transfer is deposited automatically and safely.
      </div>

      <div class="steps">
        <h2>How to send</h2>
        <div class="step"><span class="num">1</span><span>Open your banking app and choose <b>Interac e-Transfer</b> &rarr; Send Money.</span></div>
        <div class="step"><span class="num">2</span><span>Add <b>{EMAIL}</b> as the recipient (tap Copy above).</span></div>
        <div class="step"><span class="num">3</span><span>Enter your amount and send &mdash; no security question required.</span></div>
      </div>

      <div class="thanks">Thank you!</div>
      <div class="foot">Karen &amp; Mario &bull; 02.08.2026</div>
    </div>
  </div>

<script>
  function copyEmail() {{
    var email = document.getElementById('email').textContent.trim();
    var btn = document.getElementById('copyBtn');
    function done() {{ btn.textContent = 'Copied!'; btn.classList.add('copied'); setTimeout(function() {{ btn.textContent = 'Copy'; btn.classList.remove('copied'); }}, 1800); }}
    if (navigator.clipboard && navigator.clipboard.writeText) {{
      navigator.clipboard.writeText(email).then(done).catch(fallback);
    }} else {{ fallback(); }}
    function fallback() {{
      var t = document.createElement('textarea'); t.value = email; document.body.appendChild(t);
      t.select(); try {{ document.execCommand('copy'); }} catch(e) {{}} document.body.removeChild(t); done();
    }}
  }}
</script>
</body>
</html>"""

with open(OUT, "w", encoding="utf-8") as f:
    f.write(HTML)
print(f"Wrote: {OUT}  ({os.path.getsize(OUT)//1024} KB)")
