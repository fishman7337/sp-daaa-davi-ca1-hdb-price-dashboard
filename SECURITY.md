# Security Policy

## Supported Scope

This repository contains coursework artifacts, CSV data, notebooks, and lightweight validation scripts. Security checks focus on:

- preventing secrets from being committed;
- scanning Python helper scripts and tests;
- auditing Python development dependencies;
- documenting safe handling of data and local configuration.

## Reporting A Security Issue

If you find a security issue, contact the repository owner privately where possible. Include:

- affected file or workflow;
- steps to reproduce;
- potential impact;
- suggested mitigation, if known.

For school-related concerns, follow Singapore Polytechnic reporting channels.

## Secrets And Credentials

The project does not require secrets. Keep local settings in `.env`, based on `.env.example`, and do not commit `.env`.

## CI Security Checks

GitHub Actions runs:

- Bandit against `scripts/`;
- pip-audit against `requirements-dev.txt`, `requirements-cleaning.txt`, and `requirements-notebooks.txt`.

If a dependency vulnerability is found, update the dependency pin or replace the dependency. Avoid suppressing vulnerability findings unless there is a documented reason and no practical safer version.
