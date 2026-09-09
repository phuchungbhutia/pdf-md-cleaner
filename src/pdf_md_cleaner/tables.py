import re

from .models import TableData


def looks_like_table_line(line: str) -> bool:

    stripped = line.strip()

    if not stripped:
        return False

    if "|" in stripped:
        return True

    columns = re.split(
        r"\s{3,}",
        stripped,
    )

    return len(columns) >= 2


def split_table_line(line: str) -> list[str]:

    stripped = line.strip()

    if "|" in stripped:
        cells = [
            cell.strip()
            for cell in stripped.strip("|").split("|")
        ]

        return cells

    return [
        cell.strip()
        for cell in re.split(
            r"\s{3,}",
            stripped,
        )
    ]


def detect_simple_tables(
    text: str,
    page_number: int,
) -> list[TableData]:

    lines = text.splitlines()

    tables = []

    current_rows = []

    for line in lines:

        if looks_like_table_line(line):

            row = split_table_line(line)

            if len(row) >= 2:
                current_rows.append(row)

        else:

            if len(current_rows) >= 2:

                tables.append(
                    TableData(
                        rows=current_rows,
                        page_number=page_number,
                    )
                )

            current_rows = []

    if len(current_rows) >= 2:

        tables.append(
            TableData(
                rows=current_rows,
                page_number=page_number,
            )
        )

    return tables
