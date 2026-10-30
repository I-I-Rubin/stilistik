import os
import re
import sys
import json


PAGE_MARGIN_X = ".4in"
PAGE_MARGIN_Y = ".4in"
BASE_FONT_SIZE = "18pt"
LEFT_FONT_SIZE = "9.8pt"
RIGHT_FONT_SIZE = "18.5pt"
LEFT_LEADING = ".60em"
RIGHT_LEADING = ".60em"
LEFT_COLUMN = "24fr"
RIGHT_COLUMN = "76fr"
COLUMN_GUTTER = "14pt"
CELL_INSET = "0pt"
BREAK_ROWS = "true"
BODY_ABOVE = "0pt"
BODY_BELOW = ".32em"
HEADING_ABOVE = ".28em"
HEADING_BELOW = ".16em"


def typst_string(text):
    return json.dumps(text, ensure_ascii=False)


INLINE_PATTERN = re.compile(
    r"(`[^`\n]+`|\*\*[^*\n]+\*\*|\*[^*\n]+\*|\[[^\]\n]+\]\([^) \n]+(?: [^)]+)?\))"
)
LINK_PATTERN = re.compile(r"\[([^\]\n]+)\]\(([^)\n]+)\)")


def inline_markup(markdown_text):
    out = []
    pos = 0

    for match in INLINE_PATTERN.finditer(markdown_text):
        if match.start() > pos:
            out.append(f"#text({typst_string(markdown_text[pos:match.start()])})")

        token = match.group(0)
        link = LINK_PATTERN.fullmatch(token)

        if token.startswith("`") and token.endswith("`"):
            out.append(
                f"#text(font: \"Courier\", size: .88em)[#text({typst_string(token[1:-1])})]"
            )
        elif token.startswith("**") and token.endswith("**"):
            out.append(f"#strong[#text({typst_string(token[2:-2])})]")
        elif token.startswith("*") and token.endswith("*"):
            out.append(f"#emph[#text({typst_string(token[1:-1])})]")
        elif link:
            label, url = link.groups()
            out.append(f"#link({typst_string(url)})[#text({typst_string(label)})]")
        else:
            out.append(f"#text({typst_string(token)})")

        pos = match.end()

    if pos < len(markdown_text):
        out.append(f"#text({typst_string(markdown_text[pos:])})")

    return "".join(out) or "#text(\"\")"


def block_markup(line, side):
    stripped = line.strip()
    if not stripped:
        return "[]"

    heading = re.match(r"^(#+)\s+(.*)$", stripped)
    if heading:
        level = len(heading.group(1))
        body = inline_markup(heading.group(2))
        size = "1.22em" if level == 1 else "1.08em"
        return f"[#block(above: {HEADING_ABOVE}, below: {HEADING_BELOW})[#text(weight: \"bold\", size: {size})[{body}]]]"

    body = inline_markup(stripped)
    leading = LEFT_LEADING if side == "left" else RIGHT_LEADING
    return f"[#block(above: {BODY_ABOVE}, below: {BODY_BELOW})[#set par(leading: {leading}); {body}]]"


def read_lines(path):
    with open(path, "r", encoding="utf-8") as f:
        return [line.rstrip("\n") for line in f]


def create_typst_table(prefix):
    left_path = f"{prefix}_de.md"
    right_path = f"{prefix}_en.md"
    output_path = f"{prefix}.typ"

    if not (os.path.isfile(left_path) and os.path.isfile(right_path)):
        raise FileNotFoundError(f"Missing {left_path} or {right_path}")

    left_lines = read_lines(left_path)
    right_lines = read_lines(right_path)

    if len(left_lines) != len(right_lines):
        raise ValueError(
            f"Line count mismatch: {left_path} has {len(left_lines)}, "
            f"{right_path} has {len(right_lines)}"
        )

    rows = []
    for left, right in zip(left_lines, right_lines):
        if not left.strip() and not right.strip():
            continue
        rows.append((block_markup(left, "left"), block_markup(right, "right")))

    row_tables = []
    for left, right in rows:
        row_tables.append(f"#pair(\n  {left},\n  {right},\n)")

    content = f"""#set page(
  paper: "us-letter",
  margin: (x: {PAGE_MARGIN_X}, y: {PAGE_MARGIN_Y}),
)
#set text(font: "Crimson Text", size: {BASE_FONT_SIZE})
#set par(justify: true)

#let left-column = {LEFT_COLUMN}
#let right-column = {RIGHT_COLUMN}
#let column-gap = {COLUMN_GUTTER}
#let cell-inset = {CELL_INSET}
#let rows-break = {BREAK_ROWS}

#show table.cell.where(x: 0): set text(size: {LEFT_FONT_SIZE})
#show table.cell.where(x: 1): set text(size: {RIGHT_FONT_SIZE})

#let pair(left, right) = block(breakable: rows-break)[
  #table(
    columns: (left-column, right-column),
    column-gutter: column-gap,
    row-gutter: 0pt,
    stroke: none,
    inset: cell-inset,
    left,
    right,
  )
]

{chr(10).join(row_tables)}
"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Wrote {output_path}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python typst_table.py PREFIX")
        raise SystemExit(2)

    create_typst_table(sys.argv[1])
