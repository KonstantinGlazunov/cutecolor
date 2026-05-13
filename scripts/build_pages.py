#!/usr/bin/env python3
from pathlib import Path
import re
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
BASE_URL = "https://konstantinglazunov.github.io/cutecolor"
ORIGIN = "https://cutecolors.tilda.ws"
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"


def fetch(url: str) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read().decode("utf-8", errors="ignore")


def rewrite_home(html: str) -> str:
    html = html.replace('/assets/tilda/', 'assets/tilda/')
    html = html.replace('href="/kit"', 'href="./kit/"')
    html = html.replace('href="/lisichka"', 'href="./lisichka/"')
    html = html.replace('href="/blog"', 'href="./blog/"')
    html = html.replace('content="http://cutecolors.tilda.ws"', f'content="{BASE_URL}/"')
    html = html.replace('href="http://cutecolors.tilda.ws"', f'href="{BASE_URL}/"')
    html = html.replace('content="/"', f'content="{BASE_URL}/"', 1)
    html = html.replace('href="/"', f'href="{BASE_URL}/"', 1)
    html = re.sub(r'(["\'])/tilda-blocks-page', rf'\1{ORIGIN}/tilda-blocks-page', html)
    return html


def rewrite_inner(html: str, slug: str) -> str:
    html = html.replace('/assets/tilda/', '../assets/tilda/')
    html = html.replace('href="/#portfolio"', 'href="../#portfolio"')
    html = html.replace('href="/#services"', 'href="../#services"')
    html = html.replace('href="/#blog"', 'href="../#blog"')
    html = html.replace('href="/kit"', 'href="../kit/"')
    html = html.replace('href="/lisichka"', 'href="../lisichka/"')
    html = html.replace('href="/blog"', 'href="../blog/"')
    html = html.replace(f'content="http://cutecolors.tilda.ws/{slug}"', f'content="{BASE_URL}/{slug}/"')
    html = html.replace(f'href="http://cutecolors.tilda.ws/{slug}"', f'href="{BASE_URL}/{slug}/"')
    html = html.replace(f'content="http://cutecolors.tilda.ws/{slug}/"', f'content="{BASE_URL}/{slug}/"')
    html = html.replace(f'href="http://cutecolors.tilda.ws/{slug}/"', f'href="{BASE_URL}/{slug}/"')
    html = re.sub(r'(["\'])/tilda-blocks-page', rf'\1{ORIGIN}/tilda-blocks-page', html)
    return html


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    home = rewrite_home(fetch(f"{ORIGIN}/"))
    write(PUBLIC / "index.html", home)

    lisichka = rewrite_inner(fetch(f"{ORIGIN}/lisichka"), "lisichka")
    write(PUBLIC / "lisichka" / "index.html", lisichka)

    kit = rewrite_inner(fetch(f"{ORIGIN}/kit"), "kit")
    write(PUBLIC / "kit" / "index.html", kit)

    write(
        PUBLIC / "404.html",
        "<!doctype html><html lang='ru'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>Page Not Found</title></head><body style='font-family:sans-serif;background:#f5f1f0;color:#1a1a1a;display:grid;place-items:center;min-height:100vh;margin:0'><main style='text-align:center;padding:24px'><h1>Page Not Found</h1><p><a href='/' style='color:inherit'>Вернуться на главную</a></p></main></body></html>",
    )


if __name__ == "__main__":
    main()
