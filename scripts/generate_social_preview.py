#!/usr/bin/env python3
"""Generate deterministic RGB PNG exports for the repository social preview.

This temporary branch-only helper uses only the Python standard library. It is
removed before merge; the generated PNG assets remain in the final diff.
"""

from __future__ import annotations

import struct
import zlib
from pathlib import Path
from typing import Iterable

RGB = tuple[int, int, int]

BG: RGB = (18, 33, 58)
BG_PLANE: RGB = (24, 43, 73)
WHITE: RGB = (244, 248, 255)
MUTED: RGB = (184, 200, 224)
CYAN: RGB = (80, 193, 207)
BLUE: RGB = (92, 118, 238)
VIOLET: RGB = (124, 94, 210)
YELLOW: RGB = (255, 210, 92)
CORAL: RGB = (255, 137, 111)
INK: RGB = (31, 53, 89)
PALE: RGB = (222, 234, 247)

FONT: dict[str, tuple[str, ...]] = {
    "A": ("01110", "10001", "10001", "11111", "10001", "10001", "10001"),
    "D": ("11110", "10001", "10001", "10001", "10001", "10001", "11110"),
    "E": ("11111", "10000", "10000", "11110", "10000", "10000", "11111"),
    "F": ("11111", "10000", "10000", "11110", "10000", "10000", "10000"),
    "G": ("01111", "10000", "10000", "10111", "10001", "10001", "01111"),
    "I": ("11111", "00100", "00100", "00100", "00100", "00100", "11111"),
    "L": ("10000", "10000", "10000", "10000", "10000", "10000", "11111"),
    "M": ("10001", "11011", "10101", "10101", "10001", "10001", "10001"),
    "N": ("10001", "11001", "10101", "10011", "10001", "10001", "10001"),
    "O": ("01110", "10001", "10001", "10001", "10001", "10001", "01110"),
    "P": ("11110", "10001", "10001", "11110", "10000", "10000", "10000"),
    "R": ("11110", "10001", "10001", "11110", "10100", "10010", "10001"),
    "T": ("11111", "00100", "00100", "00100", "00100", "00100", "00100"),
    " ": ("00000",) * 7,
}


class Canvas:
    def __init__(self, width: int, height: int, background: RGB) -> None:
        self.width = width
        self.height = height
        self.pixels = bytearray(background * (width * height))

    def set(self, x: int, y: int, color: RGB) -> None:
        if 0 <= x < self.width and 0 <= y < self.height:
            offset = (y * self.width + x) * 3
            self.pixels[offset : offset + 3] = bytes(color)

    def rect(self, x0: int, y0: int, x1: int, y1: int, color: RGB) -> None:
        x0 = max(0, x0)
        y0 = max(0, y0)
        x1 = min(self.width, x1)
        y1 = min(self.height, y1)
        if x0 >= x1 or y0 >= y1:
            return
        row = bytes(color) * (x1 - x0)
        for y in range(y0, y1):
            offset = (y * self.width + x0) * 3
            self.pixels[offset : offset + len(row)] = row

    def circle(self, cx: int, cy: int, radius: int, color: RGB) -> None:
        rr = radius * radius
        for y in range(max(0, cy - radius), min(self.height, cy + radius + 1)):
            dy = y - cy
            span = int((rr - dy * dy) ** 0.5)
            self.rect(cx - span, y, cx + span + 1, y + 1, color)

    def line(self, x0: int, y0: int, x1: int, y1: int, width: int, color: RGB) -> None:
        dx = abs(x1 - x0)
        sx = 1 if x0 < x1 else -1
        dy = -abs(y1 - y0)
        sy = 1 if y0 < y1 else -1
        error = dx + dy
        radius = max(0, width // 2)
        while True:
            self.rect(x0 - radius, y0 - radius, x0 + radius + 1, y0 + radius + 1, color)
            if x0 == x1 and y0 == y1:
                break
            twice = 2 * error
            if twice >= dy:
                error += dy
                x0 += sx
            if twice <= dx:
                error += dx
                y0 += sy

    def polygon(self, points: Iterable[tuple[int, int]], color: RGB) -> None:
        pts = list(points)
        if len(pts) < 3:
            return
        min_y = max(0, min(y for _, y in pts))
        max_y = min(self.height - 1, max(y for _, y in pts))
        for y in range(min_y, max_y + 1):
            intersections: list[int] = []
            previous = pts[-1]
            for current in pts:
                x1, y1 = previous
                x2, y2 = current
                if (y1 <= y < y2) or (y2 <= y < y1):
                    x = x1 + (y - y1) * (x2 - x1) // (y2 - y1)
                    intersections.append(x)
                previous = current
            intersections.sort()
            for index in range(0, len(intersections) - 1, 2):
                self.rect(intersections[index], y, intersections[index + 1] + 1, y + 1, color)

    def pixel_text(self, text: str, x: int, y: int, scale: int, color: RGB, gap: int = 1) -> int:
        cursor = x
        for character in text:
            pattern = FONT[character]
            for row_index, row in enumerate(pattern):
                for column_index, value in enumerate(row):
                    if value == "1":
                        self.rect(
                            cursor + column_index * scale,
                            y + row_index * scale,
                            cursor + (column_index + 1) * scale,
                            y + (row_index + 1) * scale,
                            color,
                        )
            cursor += (5 + gap) * scale
        return cursor

    def save_png(self, path: Path) -> None:
        def chunk(name: bytes, data: bytes) -> bytes:
            return struct.pack(">I", len(data)) + name + data + struct.pack(">I", zlib.crc32(name + data) & 0xFFFFFFFF)

        scanlines = bytearray()
        stride = self.width * 3
        for y in range(self.height):
            scanlines.append(0)
            start = y * stride
            scanlines.extend(self.pixels[start : start + stride])
        png = b"\x89PNG\r\n\x1a\n"
        png += chunk(b"IHDR", struct.pack(">IIBBBBB", self.width, self.height, 8, 2, 0, 0, 0))
        png += chunk(b"IDAT", zlib.compress(bytes(scanlines), 9))
        png += chunk(b"IEND", b"")
        path.write_bytes(png)


def draw_preview(width: int, height: int) -> Canvas:
    factor = width / 1280

    def s(value: int) -> int:
        return max(1, round(value * factor))

    canvas = Canvas(width, height, BG)
    canvas.circle(s(1165), s(70), s(180), BG_PLANE)
    canvas.circle(s(930), s(650), s(220), BG_PLANE)

    # Project mark
    canvas.rect(s(64), s(56), s(120), s(112), BLUE)
    canvas.line(s(77), s(94), s(88), s(83), s(5), WHITE)
    canvas.line(s(88), s(83), s(97), s(91), s(5), WHITE)
    canvas.line(s(97), s(91), s(109), s(75), s(5), WHITE)
    canvas.circle(s(109), s(75), s(4), YELLOW)

    title_scale = max(2, s(12))
    canvas.pixel_text("MODERN FLAT", s(64), s(158), title_scale, WHITE)
    canvas.pixel_text("IMAGE PIPELINE", s(64), s(278), title_scale, WHITE)

    # Four controlled stages. Bars are intentionally language-neutral at thumbnail size.
    canvas.rect(s(64), s(410), s(610), s(452), INK)
    stage_x = [s(82), s(214), s(346), s(478)]
    stage_colors = [CYAN, BLUE, CORAL, YELLOW]
    for index, (x, color) in enumerate(zip(stage_x, stage_colors, strict=True)):
        canvas.circle(x, s(431), s(9), color)
        canvas.rect(x + s(18), s(422), x + s(83), s(427), MUTED)
        canvas.rect(x + s(18), s(435), x + s(68), s(440), MUTED)
        if index < 3:
            canvas.line(x + s(93), s(431), x + s(113), s(431), s(3), (94, 122, 166))
            canvas.polygon(
                [(x + s(110), s(425)), (x + s(118), s(431)), (x + s(110), s(437))],
                (94, 122, 166),
            )

    # Input reference card
    canvas.rect(s(760), s(170), s(900), s(350), WHITE)
    canvas.rect(s(776), s(186), s(884), s(305), PALE)
    canvas.circle(s(858), s(216), s(11), YELLOW)
    canvas.polygon(
        [(s(776), s(293)), (s(808), s(250)), (s(832), s(274)), (s(858), s(235)), (s(884), s(268)), (s(884), s(305)), (s(776), s(305))],
        (115, 134, 164),
    )
    canvas.rect(s(788), s(323), s(872), s(331), (206, 218, 234))

    # Scene-contract stack
    for x, y, color in ((910, 145, BLUE), (936, 160, VIOLET), (962, 176, CYAN)):
        canvas.rect(s(x), s(y), s(x + 132), s(y + 180), color)
        canvas.rect(s(x + 19), s(y + 28), s(x + 110), s(y + 36), WHITE)
        canvas.rect(s(x + 19), s(y + 52), s(x + 94), s(y + 60), WHITE)
        canvas.rect(s(x + 19), s(y + 76), s(x + 104), s(y + 84), WHITE)

    # Direction arrow
    canvas.line(s(1099), s(245), s(1134), s(245), s(5), (121, 202, 255))
    canvas.polygon([(s(1128), s(234)), (s(1143), s(245)), (s(1128), s(256))], (121, 202, 255))

    # Checked Modern Flat output
    canvas.rect(s(1142), s(145), s(1230), s(356), WHITE)
    canvas.rect(s(1153), s(157), s(1219), s(320), (220, 243, 250))
    canvas.circle(s(1197), s(187), s(9), YELLOW)
    canvas.polygon(
        [(s(1153), s(288)), (s(1172), s(237)), (s(1188), s(259)), (s(1203), s(216)), (s(1219), s(250)), (s(1219), s(320)), (s(1153), s(320))],
        BLUE,
    )
    canvas.polygon(
        [(s(1153), s(306)), (s(1172), s(274)), (s(1188), s(290)), (s(1204), s(258)), (s(1219), s(281)), (s(1219), s(320)), (s(1153), s(320))],
        CYAN,
    )
    canvas.rect(s(1163), s(334), s(1210), s(342), (206, 218, 234))

    # Safe-area footer accent
    canvas.rect(s(64), s(548), s(1216), s(556), CYAN)
    return canvas


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    assets = root / "assets"
    assets.mkdir(parents=True, exist_ok=True)
    draw_preview(1280, 640).save_png(assets / "repository-social-preview.png")
    draw_preview(320, 160).save_png(assets / "repository-social-preview-thumbnail.png")


if __name__ == "__main__":
    main()
