# Simple Makefile

MAIN = conchfetch.py
TEST = distro_test.py
NAME = conchfetch
TESTNAME = conchfetch-test
PROJECT_DIR = $(realpath .)

.PHONY: help install uninstall run test clean

help:
	@echo "make install   - Install $(NAME) & $(TESTNAME)"
	@echo "make uninstall - Uninstall both commands"
	@echo "make run       - Run $(NAME) locally"
	@echo "make test      - Run tests locally"
	@echo "make clean     - Clean temp files"

install:
	@echo "Installing..."
	# Install main program
	sudo cp $(MAIN) /usr/local/bin/$(NAME)
	sudo chmod +x /usr/local/bin/$(NAME)
	# Create wrapper that changes to project directory
	@echo "#!/bin/bash" | sudo tee /usr/local/bin/$(TESTNAME) > /dev/null
	@echo "cd '$(PROJECT_DIR)' && python3 '$(TEST)'" | sudo tee -a /usr/local/bin/$(TESTNAME) > /dev/null
	sudo chmod +x /usr/local/bin/$(TESTNAME)
	@echo "Done! Commands available:"
	@echo "  $(NAME)"
	@echo "  $(TESTNAME)"

uninstall:
	@echo "Uninstalling..."
	sudo rm -f /usr/local/bin/$(NAME)
	sudo rm -f /usr/local/bin/$(TESTNAME)
	@echo "Removed!"

run:
	@echo "Running $(NAME)..."
	python3 $(MAIN)

test:
	@echo "Running tests..."
	python3 $(TEST)

clean:
	@echo "Cleaning temp files..."
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -type d -delete
	@echo "Cleaned!"
