default:
    just --list

# Install pre-commit hooks
install-pre-commit:
    uv run pre-commit install

# Check the code with pyright
pyright:
    uv run pyright

# Test the code with pytest
test:
    uv run pytest --cov --cov-config=pyproject.toml --cov-report=xml

# Test the code with tox
tox:
    uv run tox

# Clean build artifacts
clean-build:
    rm -r dist

# Build wheel file
build: clean-build
    uvx --from build pyproject-build --installer uv

# Publish a release to PyPI
publish:
    uvx twine upload --repository-url https://upload.pypi.org/legacy/ dist/*

# Build and publish
build-and-publish: build publish
