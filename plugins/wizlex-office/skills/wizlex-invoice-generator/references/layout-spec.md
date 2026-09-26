# Wizlex invoice layout

The retained reference is a one-page portrait A4 PDF created with ReportLab.

- Page: A4 portrait, white background, approximately 55 pt left and right margins.
- Typography: Helvetica family, black text.
- Title: centered `INVOICE`, bold, approximately 21 pt.
- Metadata: left-aligned invoice date only; the label is bold. Do not include an invoice number.
- Parties: `Billed To:` followed by the client, then `Billed From:` followed by the freelancer. Section labels are bold.
- Table: full content width with columns Item, Description, and Amount (PHP). Header row has a light-gray fill. Grid lines are thin gray. Item names are bold; descriptions and amounts are regular weight.
- Total: bold `Total Amount Due: PHP 0.00` below the table.
- Payment: bold `Payment Details:` followed by method, account name, account number, and SWIFT code.
- Disclaimer: italic line below the payment block.

Keep the design restrained and businesslike. Allow rows and pages to grow naturally for long content; repeat the table header on later pages. Avoid shrinking body text merely to force a single page.
