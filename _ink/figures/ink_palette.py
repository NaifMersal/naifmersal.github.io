"""Ink palette for figure scripts.

GENERATED from brand/tokens.json by scripts/build_brand.py. Do not edit this
copy; edit the tokens and rebuild.

Usage:

    import ink_palette as ink
    ink.use()                         # style matplotlib for the current mode
    c = ink.colors()                  # role -> hex for the current mode
    fig.savefig(OUT / ink.variant("fig_x.png"))

The mode comes from the INK_MODE environment variable ("light", the default,
or "dark"), so one script makes both sets. In dark mode variant() turns
"fig_x.png" into "fig_x.dark.png", and the deck swaps that file in at night.
Run both passes with:

    python <plugin>/scripts/render_figures.py scripts/make_figures.py ...

Colour roles, the same as everywhere else in the brand:

    wash / ink3   context: prompt tokens, gridlines, the things you are not
                  asking the viewer to look at
    ink / ink2    the answer: accepted tokens, the main series
    accent        what changed, or the one value to remember. One per figure.

The module-level constants (INK, ACCENT, ...) are the LIGHT values, kept for
scripts that only ever draw light figures. Prefer colors() in new code.
"""

import os
from pathlib import Path

LIGHT = {
    "paper": "#FBFBFC",
    "wash": "#F1F2F5",
    "rule": "#E2E4E9",
    "ink": "#16181D",
    "ink2": "#4A505C",
    "ink3": "#8A909B",
    "accent": "#2347C6"
}
DARK = {
    "paper": "#121418",
    "wash": "#1A1D23",
    "rule": "#2A2E36",
    "ink": "#ECEDEF",
    "ink2": "#A3A8B2",
    "ink3": "#6B717C",
    "accent": "#8AA4FF"
}

DARK_MODE = os.environ.get("INK_MODE", "light").strip().lower() == "dark"

PAPER = LIGHT["paper"]
WASH = LIGHT["wash"]
RULE = LIGHT["rule"]
INK = LIGHT["ink"]
INK2 = LIGHT["ink2"]
INK3 = LIGHT["ink3"]
ACCENT = LIGHT["accent"]
ACCENT_ON_DARK = DARK["accent"]

FONT_SANS = [
    "IBM Plex Sans",
    "IBM Plex Sans Arabic",
    "system-ui",
    "-apple-system",
    "Segoe UI",
    "sans-serif"
]
FONT_MONO = [
    "IBM Plex Mono",
    "ui-monospace",
    "Cascadia Mono",
    "Consolas",
    "monospace"
]
TILE_RADIUS_PX = 3


FONTS_DIR = Path(__file__).resolve().parent / "fonts"
_FILES = {
    "sans": "IBMPlexSans-{w}.ttf",
    "arabic": "IBMPlexSansArabic-{w}.ttf",
    "mono": "IBMPlexMono-{w}.ttf",
}


def font_path(family: str = "sans", weight: str = "Regular") -> str:
    """Path to a bundled Plex TTF, for PIL's ImageFont.truetype.

    family: sans | arabic | mono. weight: Regular, Medium, SemiBold, Bold
    (Italic for sans only).
    """
    path = FONTS_DIR / _FILES[family].format(w=weight)
    if not path.exists():
        raise FileNotFoundError(f"{path} is not in the Ink bundle")
    return str(path)


def register_fonts() -> None:
    """Make the bundled Plex files (fonts/ next to this file) visible to matplotlib."""
    from matplotlib import font_manager

    for f in FONTS_DIR.glob("*.ttf"):
        font_manager.fontManager.addfont(str(f))


def _dark(dark):
    return DARK_MODE if dark is None else bool(dark)


def colors(dark: bool | None = None) -> dict:
    """The role -> hex map for one mode (default: the INK_MODE mode)."""
    return dict(DARK if _dark(dark) else LIGHT)


def variant(name, dark: bool | None = None):
    """'fig_x.png' -> 'fig_x.dark.png' in dark mode; unchanged in light mode.

    Accepts a str or a Path and returns the same type.
    """
    if not _dark(dark):
        return name
    p = Path(name)
    out = p.with_name(f"{p.stem}.dark{p.suffix}")
    return out if isinstance(name, Path) else str(out)


def mix(a: str, b: str, t: float) -> str:
    """Blend hex colour a into b: t=0 gives b, t=1 gives a. For flat tints
    (PIL has no alpha blending onto the page)."""
    ca = [int(a[i:i + 2], 16) for i in (1, 3, 5)]
    cb = [int(b[i:i + 2], 16) for i in (1, 3, 5)]
    return "#" + "".join(f"{round(t * x + (1 - t) * y):02X}" for x, y in zip(ca, cb))


def use(dark: bool | None = None) -> None:
    """Apply the Ink style to matplotlib's rcParams.

    Plex comes from the bundled fonts/ folder, so nothing needs installing.
    Maths uses Computer Modern to match the KaTeX on the slides.
    """
    import logging

    import matplotlib as mpl

    logging.getLogger("matplotlib.font_manager").setLevel(logging.ERROR)
    register_fonts()
    c = colors(dark)
    mpl.rcParams.update(
        {
            "figure.facecolor": c["paper"],
            "axes.facecolor": c["paper"],
            "savefig.facecolor": c["paper"],
            "axes.edgecolor": c["rule"],
            "axes.labelcolor": c["ink2"],
            "axes.titlecolor": c["ink"],
            "axes.titleweight": 600,
            "axes.titlelocation": "left",
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.grid": True,
            "axes.axisbelow": True,
            "grid.color": c["rule"],
            "grid.linewidth": 0.8,
            "xtick.color": c["ink2"],
            "ytick.color": c["ink2"],
            "xtick.major.size": 0,
            "ytick.major.size": 0,
            "text.color": c["ink"],
            "legend.labelcolor": c["ink"],
            "font.family": "sans-serif",
            "font.sans-serif": [f for f in FONT_SANS if f not in ("system-ui", "-apple-system", "sans-serif")]
            + ["DejaVu Sans"],
            "font.monospace": [f for f in FONT_MONO if f not in ("ui-monospace", "monospace")] + ["DejaVu Sans Mono"],
            "font.size": 12,
            "mathtext.fontset": "cm",
            "axes.prop_cycle": mpl.cycler(color=[c["ink"], c["ink3"], c["accent"]]),
            "lines.linewidth": 2,
            "legend.frameon": False,
            "savefig.dpi": 200,
        }
    )
