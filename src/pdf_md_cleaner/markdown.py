from .models import DocumentResult, PageResult
from .structure import extract_headings, markdownize_structure


def escape_table_cell(value: str) -> str:

    return (
        value
        .replace("|", "\\|")
        .replace("\n", " ")
        .strip()
    )


def table_to_markdown(rows: list[list[str]]) -> str:

    if not rows:
        return ""

    width = max(
        len(row)
        for row in rows
    )

    normalized = []

    for row in rows:

        row = row + [""] * (
            width - len(row)
        )

        normalized.append(row)

    header = normalized[0]

    output = []

    output.append(
        "| "
        + " | ".join(
            escape_table_cell(cell)
            for cell in header
        )
        + " |"
    )

    output.append(
        "| "
        + " | ".join(
            "---"
            for _ in range(width)
        )
        + " |"
    )

    for row in normalized[1:]:

        output.append(
            "| "
            + " | ".join(
                escape_table_cell(cell)
                for cell in row
            )
            + " |"
        )

    return "\n".join(output)


def generate_toc(
    pages: list[PageResult],
) -> str:

    lines = [
        "## Table of Contents",
        "",
    ]

    for page in pages:

        headings = extract_headings(
            page.text
        )

        for heading in headings:

            anchor = (
                heading.lower()
                .replace(" ", "-")
            )

            lines.append(
                f"- [{heading}](#{anchor}) "
                f"*(page {page.page_number})*"
            )

    lines.append("")

    return "\n".join(lines)


def render_page(
    page: PageResult,
    preserve_page_markers: bool = True,
) -> str:

    output = []

    if preserve_page_markers:

        output.append(
            f"<!-- Source page "
            f"{page.page_number} -->"
        )

    if page.review_required:

        output.append(
            "> **REVIEW REQUIRED:** "
            f"OCR confidence "
            f"{page.ocr_confidence:.1f}%."
        )

    if page.text:

        structured = markdownize_structure(
            page.text
        )

        output.append(structured)

    for table in page.tables:

        table_md = table_to_markdown(
            table.rows
        )

        if table_md:

            output.append("")

            output.append(
                "<!-- Detected table -->"
            )

            output.append(table_md)

    return "\n\n".join(output)


def document_to_markdown(
    document: DocumentResult,
    generate_toc_enabled: bool = True,
    preserve_page_markers: bool = True,
) -> str:

    output = []

    output.append(
        f"# {document.title}"
    )

    output.append("")

    if generate_toc_enabled:

        output.append(
            generate_toc(
                document.pages
            )
        )

    for page in document.pages:

        output.append(
            render_page(
                page,
                preserve_page_markers,
            )
        )

        output.append("")

        output.append("---")

        output.append("")

    return "\n".join(output).strip() + "\n"