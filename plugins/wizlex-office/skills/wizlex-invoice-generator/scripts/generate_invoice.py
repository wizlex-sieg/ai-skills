#!/usr/bin/env python3
"""Generate a Wizlex freelancer invoice PDF from JSON input."""

from __future__ import annotations

import argparse
import json
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from pathlib import Path
from typing import Any

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


SKILL_DIR = Path(__file__).resolve().parent.parent
DEFAULT_PROFILE = SKILL_DIR / "assets" / "default-profile.json"
TWOPLACES = Decimal("0.01")


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as stream:
        value = json.load(stream)
    if not isinstance(value, dict):
        raise ValueError(f"Expected a JSON object in {path}")
    return value


def merge_profile(defaults: dict[str, Any], invoice: dict[str, Any]) -> dict[str, Any]:
    merged = dict(defaults)
    for key, value in invoice.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = {**merged[key], **value}
        else:
            merged[key] = value
    return merged


def require_text(data: dict[str, Any], key: str) -> str:
    value = data.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"Missing required non-empty text field: {key}")
    return value.strip()


def money(value: Any, index: int) -> Decimal:
    try:
        amount = Decimal(str(value)).quantize(TWOPLACES, rounding=ROUND_HALF_UP)
    except (InvalidOperation, ValueError) as exc:
        raise ValueError(f"Item {index} has an invalid amount: {value!r}") from exc
    if amount < 0:
        raise ValueError(f"Item {index} amount cannot be negative")
    return amount


def paragraph_lines(lines: list[str], style: ParagraphStyle) -> Paragraph:
    from xml.sax.saxutils import escape

    return Paragraph("<br/>".join(escape(str(line)) for line in lines), style)


def build_invoice(data: dict[str, Any], output_path: Path) -> None:
    from xml.sax.saxutils import escape

    invoice_date = require_text(data, "invoice_date")
    raw_items = data.get("items")
    if not isinstance(raw_items, list) or not raw_items:
        raise ValueError("items must be a non-empty array")

    normalized_items: list[tuple[str, str, Decimal]] = []
    for index, item in enumerate(raw_items, start=1):
        if not isinstance(item, dict):
            raise ValueError(f"Item {index} must be an object")
        item_name = require_text(item, "item")
        description = require_text(item, "description")
        amount = money(item.get("amount"), index)
        normalized_items.append((item_name, description, amount))

    currency_code = require_text(data, "currency_code")
    amount_label = require_text(data, "amount_column_label")
    client = data.get("client")
    freelancer = data.get("freelancer")
    payment = data.get("payment")
    if not all(isinstance(block, dict) for block in (client, freelancer, payment)):
        raise ValueError("client, freelancer, and payment must be objects")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    document = SimpleDocTemplate(
        str(output_path),
        pagesize=A4,
        rightMargin=19.5 * mm,
        leftMargin=19.5 * mm,
        topMargin=19 * mm,
        bottomMargin=18 * mm,
        title="Invoice",
        author=require_text(freelancer, "name"),
    )

    styles = getSampleStyleSheet()
    body = ParagraphStyle(
        "InvoiceBody", parent=styles["BodyText"], fontName="Helvetica",
        fontSize=10.5, leading=13, spaceAfter=0, alignment=TA_LEFT,
    )
    body_bold = ParagraphStyle("InvoiceBodyBold", parent=body, fontName="Helvetica-Bold")
    body_italic = ParagraphStyle("InvoiceBodyItalic", parent=body, fontName="Helvetica-Oblique", fontSize=9.5)
    title = ParagraphStyle(
        "InvoiceTitle", parent=body_bold, fontSize=21, leading=25,
        alignment=TA_CENTER, spaceAfter=17,
    )
    header = ParagraphStyle("TableHeader", parent=body_bold, fontSize=10)
    cell = ParagraphStyle("TableCell", parent=body, fontSize=9.7, leading=12)
    cell_bold = ParagraphStyle("TableCellBold", parent=cell, fontName="Helvetica-Bold")

    story: list[Any] = [Paragraph("INVOICE", title)]
    story.append(Paragraph(f"<b>Invoice Date:</b> {escape(invoice_date)}", body))
    story.append(Spacer(1, 10))

    client_lines = [require_text(client, "name")] + [str(v) for v in client.get("address_lines", [])]
    story.append(Paragraph("Billed To:", body_bold))
    story.append(paragraph_lines(client_lines, body))
    story.append(Spacer(1, 8))

    freelancer_lines = [require_text(freelancer, "name"), require_text(freelancer, "role")]
    freelancer_lines.extend(str(v) for v in freelancer.get("address_lines", []))
    freelancer_lines.append(f"Email: {require_text(freelancer, 'email')}")
    story.append(Paragraph("Billed From:", body_bold))
    story.append(paragraph_lines(freelancer_lines, body))
    story.append(Spacer(1, 15))

    table_data: list[list[Any]] = [[
        Paragraph("Item", header),
        Paragraph("Description", header),
        Paragraph(escape(amount_label), header),
    ]]
    for item_name, description, amount in normalized_items:
        table_data.append([
            Paragraph(escape(item_name), cell_bold),
            Paragraph(escape(description), cell),
            Paragraph(f"{amount:,.2f}", cell),
        ])

    table = Table(table_data, colWidths=[58 * mm, 78 * mm, 37 * mm], repeatRows=1, hAlign="LEFT")
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#D9D9D9")),
        ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#8F8F8F")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))
    story.append(table)
    story.append(Spacer(1, 13))

    total = sum((row[2] for row in normalized_items), Decimal("0.00"))
    story.append(Paragraph(f"Total Amount Due: {escape(currency_code)}&nbsp;{total:,.2f}", body_bold))
    story.append(Spacer(1, 11))
    story.append(Paragraph("Payment Details:", body_bold))
    payment_lines = [
        require_text(payment, "method"),
        f"Account Name: {require_text(payment, 'account_name')}",
        f"Account Number: {require_text(payment, 'account_number')}",
        f"SWIFT Code: {require_text(payment, 'swift_code')}",
    ]
    story.append(paragraph_lines(payment_lines, body))
    story.append(Spacer(1, 17))
    story.append(Paragraph(escape(require_text(data, "disclaimer")), body_italic))
    document.build(story)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path, help="Invoice JSON input")
    parser.add_argument("--output", required=True, type=Path, help="Destination PDF")
    args = parser.parse_args()

    defaults = load_json(DEFAULT_PROFILE)
    invoice = load_json(args.input)
    build_invoice(merge_profile(defaults, invoice), args.output.resolve())
    print(args.output.resolve())


if __name__ == "__main__":
    main()
