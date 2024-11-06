find . -type f -name "*.py" -exec wc -l {} +
python3 -m black --line-length 120 *