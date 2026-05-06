# Contributing to pyvenezuela

Thanks for your interest in contributing! This guide will help you get started.

## Development setup

1. Fork and clone the repository:

   ```bash
   git clone https://github.com/<your-username>/pyvenezuela.git
   cd pyvenezuela
   ```

2. Install dependencies with [uv](https://docs.astral.sh/uv/):

   ```bash
   make setup
   # or directly: uv sync --locked
   ```

## Running checks

| Command         | Description                  |
| --------------- | ---------------------------- |
| `make test`     | Run the test suite           |
| `make check`    | Run linting and type checks  |
| `make format`   | Auto-format code with ruff   |
| `make coverage` | Run tests with coverage      |

## Submitting a pull request

1. Create a feature branch from `main`:

   ```bash
   git checkout -b my-feature
   ```

2. Make your changes and add tests if applicable.

3. Run formatting, linting, and tests:

   ```bash
   make format
   make check
   make test
   ```

4. Commit your changes with a clear, descriptive message.

5. Push to your fork and open a pull request against `main`.

6. Ensure CI passes on your PR.

## Code style

Code style is enforced by [ruff](https://docs.astral.sh/ruff/). Run `make format` before submitting and the formatter will take care of the rest. No need to worry about style nits in code review.

## Questions?

Feel free to open an issue if something is unclear. We are happy to help!
