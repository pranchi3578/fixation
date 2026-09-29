#!/usr/bin/env python3
"""Print the letter to a PDF and to a JPEG.

The page is the master; these two are what actually gets sent. The PDF is
the card at its true size — six inches by nine, no browser margin — for
the printer or an attachment; the JPEG is what goes into a WhatsApp
message, where a PDF arrives as a grey file card nobody opens.

Usage:  python3 tools/export_letter.py
Output: assets/joel-sandra-invitation.pdf
        assets/joel-sandra-invitation.jpg
"""

import asyncio
import pathlib

from playwright.async_api import async_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
PDF = ROOT / "assets" / "joel-sandra-invitation.pdf"
JPG = ROOT / "assets" / "joel-sandra-invitation.jpg"


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(executable_path=CHROME)
        # Three device pixels per CSS pixel puts the JPEG at about 290dpi
        # for a 6 × 9 card, which is a printable image rather than a preview.
        page = await browser.new_page(viewport={"width": 1100, "height": 1500},
                                      device_scale_factor=3)
        problems = []
        page.on("pageerror", lambda e: problems.append(str(e)))
        await page.goto((ROOT / "letter.html").as_uri())
        # The faces are local, but the browser still has to parse them, and a
        # PDF made a beat early is a PDF set in Times.
        await page.evaluate("document.fonts.ready")
        await page.wait_for_timeout(600)

        fonts = await page.evaluate(
            "[...document.fonts].filter(f => f.status === 'loaded').length")
        if fonts < 3:
            raise SystemExit("only %d faces loaded — refusing to export" % fonts)

        # 6 × 9 inches, which is what the stylesheet draws.
        await page.pdf(path=str(PDF), width="6in", height="9in", print_background=True,
                       margin={"top": "0", "right": "0", "bottom": "0", "left": "0"})

        sheet = await page.query_selector(".sheet")
        await sheet.screenshot(path=str(JPG), type="jpeg", quality=92)

        await browser.close()

    if problems:
        raise SystemExit("page errors: %s" % problems)
    for f in (PDF, JPG):
        print("  %-44s %6.1f KB" % (f.relative_to(ROOT), f.stat().st_size / 1024))


if __name__ == "__main__":
    asyncio.run(main())
