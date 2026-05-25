# MODEL.md

## Overview

This project is an ESG data ingestion and review system. It ingests activity data from three sources:

1. SAP fuel/procurement data
2. Utility electricity data
3. Travel data

The system normalizes these records into a common `ActivityRow` model so reviewers can approve, reject, or delete rows before they are used for emissions reporting.

---

## Main Data Models

### IngestionBatch

Represents one ingestion run.

Fields:

- `source_type` — SAP, UTILITY, or TRAVEL
- `file_name` — source file name
- `total_rows` — total rows processed
- `failed_rows` — invalid rows
- `suspicious_rows` — rows needing review
- `created_at` — ingestion time

Why:

This tracks which file/source produced rows and when the ingestion happened.

---

### ActivityRow

Represents one normalized ESG activity record.

Fields:

- `batch` — links row to ingestion batch
- `source_type` — SAP / UTILITY / TRAVEL
- `raw_data` — original row exactly as received
- `normalized_data` — cleaned structured version
- `scope` — SCOPE_1 / SCOPE_2 / SCOPE_3
- `activity_type` — fuel_procurement, electricity, flight, hotel, ground_transport
- `quantity` — normalized numeric quantity
- `unit` — L, KG, kWh, km, nights
- `status` — PENDING, FAILED, SUSPICIOUS, APPROVED, REJECTED
- `error_reason` — reason for failed rows
- `suspicious_reason` — reason for suspicious rows
- `is_locked` — approved rows are locked
- `created_at` — row creation time
- `approved_at` — approval time
- `rejected_at` — rejection time

Why:

This gives one common review table for all three source systems.

---

### AuditLog

Tracks reviewer actions.

Fields:

- `row` — related activity row
- `action` — APPROVED or REJECTED
- `note` — action description
- `created_at` — action time

Why:

ESG systems need auditability. Every approval or rejection should be traceable.

---

## Multi-Tenancy

In a production system, every table should include:

- `tenant_id`
- `organization_id`
- `created_by`

This assignment currently uses a single-tenant design for simplicity.

Future design:

- Each company would have its own tenant.
- Every ingestion batch and activity row would belong to one tenant.
- Reviewers would only see rows for their tenant.

---

## Scope Categorization

### Scope 1

SAP fuel/procurement rows are categorized as Scope 1 because fuel usage can directly create emissions owned or controlled by the company.

Example:

- Diesel
- Petrol
- LPG
- Lubricant

### Scope 2

Utility electricity rows are categorized as Scope 2 because purchased electricity creates indirect energy emissions.

Example:

- Electricity usage in kWh

### Scope 3

Travel rows are categorized as Scope 3 because employee travel and hotel stays are indirect value-chain emissions.

Example:

- Flights
- Hotels
- Ground transport

---

## Source-of-Truth Tracking

The system stores both:

1. `raw_data`
2. `normalized_data`

This is important because:

- `raw_data` preserves the original source row.
- `normalized_data` stores cleaned fields used by the app.
- `batch` tracks which file/source created the row.
- `created_at` tracks when it entered the system.
- `status` tracks whether it was reviewed.

If a row is edited in future, the system should store:

- previous value
- new value
- edited_by
- edited_at
- edit_reason

---

## Unit Normalization

Current supported units:

- SAP: `L`, `KG`
- Utility: `kWh`
- Travel: `km`, `nights`

Current project validates numeric quantity but does not fully convert all units.

Future production system should include:

- unit conversion table
- material-specific conversion factors
- emission factor mapping
- currency normalization
- timezone/date normalization

---

## Validation Rules

### SAP

Failed when:

- quantity is missing
- quantity is not numeric

Suspicious when:

- plant code is unknown
- quantity is unusually high

### Utility

Failed when:

- usage is missing
- usage is not numeric

Suspicious when:

- electricity usage is unusually high

### Travel

Failed when:

- required distance is missing for flight

Suspicious when:

- ground transport distance is unusually high

---

## Audit Trail

Audit logs are created when reviewers approve or reject rows.

This supports:

- compliance
- traceability
- reviewer accountability
- later investigation

Approved rows are locked using `is_locked = true`.

---

## Why This Model

This model was chosen because it separates:

- ingestion batch metadata
- individual activity rows
- audit history

This makes the system easier to extend for:

- more source systems
- more tenants
- more validation rules
- emissions calculations
- reviewer workflows