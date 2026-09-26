# Invoice input

The generator accepts UTF-8 JSON. `invoice_date` and `items` are required by the script. The distributed profile contains placeholders; real invoices also need user-provided client, freelancer, and payment overrides as shown below. Invoice numbers are intentionally omitted from the format. Store real billing inputs outside this repository.

```json
{
  "invoice_date": "September 7, 2026",
  "items": [
    {
      "item": "Project milestone",
      "description": "Second milestone payment for the agreed project scope.",
      "amount": 25000
    }
  ]
}
```

Amounts may be JSON numbers or numeric strings, but must be non-negative and have at most two decimal places after rounding. The total is calculated by the generator.

## Profile overrides

Override only the fields that should differ from `assets/default-profile.json`:

```json
{
  "currency_code": "PHP",
  "amount_column_label": "Amount (PHP)",
  "client": {
    "name": "Wizlex Inc",
    "address_lines": ["Address line 1", "Address line 2"]
  },
  "freelancer": {
    "name": "Freelancer name",
    "role": "Freelance role",
    "address_lines": ["Country"],
    "email": "name@example.com"
  },
  "payment": {
    "method": "Bank Transfer - Bank name",
    "account_name": "ACCOUNT NAME",
    "account_number": "0000000000",
    "swift_code": "SWIFTCODE"
  },
  "disclaimer": "Custom invoice note."
}
```

Objects are merged one level deep with the defaults. For example, overriding only `payment.account_number` retains the default bank method, account name, and SWIFT code. Replace all placeholder fields and example addresses before using the output as a real invoice.
