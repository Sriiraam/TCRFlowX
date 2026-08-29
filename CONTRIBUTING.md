# Contributing to TCRFlowX

Contributions, bug reports, and suggestions are welcome.

## Development Setup

Clone the repository:

```bash
git clone https://github.com/Sriiraam/TCRFlowX.git
cd TCRFlowX
```

Create and activate the Python environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Testing

Run automated tests:

```bash
pytest -v tests/
```

Validate the Nextflow configuration:

```bash
nextflow config -profile local
```

## Development Guidelines

- Keep Nextflow processes modular.
- Avoid hard-coded absolute paths.
- Keep generated outputs out of version control.
- Document new parameters and execution profiles.
- Add tests for new functionality where appropriate.
- Never commit credentials, API keys, license keys, passwords, or sensitive patient data.

## Pull Requests

Pull requests should describe:

- The problem being addressed.
- The proposed change.
- How the change was tested.
- Any effect on workflow outputs or reproducibility.
