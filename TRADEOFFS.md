# TRADEOFFS.md

## Overview

This document lists three important things deliberately not built in this version and why.

---

## 1. Full Authentication and Role-Based Access Control

### Not built

I did not implement login, user accounts, reviewer roles, or admin permissions.

### Why

The assignment focus was ingestion, normalization, review workflow, and auditability. Adding authentication would increase setup complexity and reduce time available for data modeling and source handling.

### Production approach

In production, I would add:

- user login
- organization/tenant membership
- reviewer/admin roles
- action-level permissions
- audit logs with user identity

---

## 2. Real Emissions Calculation Engine

### Not built

I did not calculate final CO2e emissions.

### Why

Accurate emissions calculation requires emission factors by:

- country
- year
- fuel type
- electricity grid
- transport mode
- hotel region
- methodology

Using fake factors could produce misleading results. I chose to focus on clean source-of-truth activity data first.

### Production approach

In production, I would add:

- emission factor tables
- factor versioning
- region/year matching
- calculation explanation
- recalculation when factors change

---

## 3. Advanced Source Integrations

### Not built

I did not integrate directly with SAP APIs, utility provider APIs, or travel management systems.

### Why

Real integrations require credentials, API contracts, rate limits, authentication flows, and customer-specific mapping. For the assignment, sample files provide a controlled way to demonstrate ingestion logic.

### Production approach

In production, I would add:

- SAP OData/BAPI connector
- utility provider connector
- travel system API connector
- scheduled ingestion jobs
- retry and failure monitoring
- source mapping configuration UI