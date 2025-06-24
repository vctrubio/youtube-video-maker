.PHONY: check-python install clean help

# Default target
help:
	@echo "Available targets:"
	@echo "  install      - Check Python and install dependencies"
	@echo "  check-python - Check if Python 3 is installed"
	@echo "  clean        - Remove __pycache__ directories"
	@echo "  help         - Show this help message"

# Check if Python 3 is installed
check-python:
	@echo "Checking for Python 3..."
	@which python3 > /dev/null || (echo "Error: Python 3 is not installed. Please download and install Python 3 from https://www.python.org/downloads/" && exit 1)
	@python3 --version
	@echo "Python 3 is installed ✓"

# Install dependencies
install: check-python
	@echo "Installing dependencies..."
	python3 -m pip install --upgrade pip
	python3 -m pip install -r requirements.txt
	@echo "Installation complete ✓"

# Clean up cache files
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc" -delete 2>/dev/null || true
	@echo "Cleaned up cache files ✓"