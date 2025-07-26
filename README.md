# 🐦 HappyBird Watcher

A SyftBox app that monitors the SyftBox filesystem for `happybird.txt` files and displays them in an interactive Jupyter widget.

## Features

- 📁 Automatically scans SyftBox directories for happybird.txt files
- 🔄 Real-time updates with configurable refresh intervals
- 🎯 Click to view file contents
- 🚀 Works in three modes: Checkpoint (mock data), Development (local server), and Production (SyftBox)

## Installation

### For Development

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/happybird-watcher.git
cd happybird-watcher

# Install in development mode
pip install -e .
```

### For SyftBox Users

The app will be automatically installed when you add it to your SyftBox apps.

## Usage

### In Jupyter Notebooks

```python
from happybird_watcher import HappyBirdWatcher

# Create and display the widget
watcher = HappyBirdWatcher()
watcher
```

### Creating HappyBird Files

Users can create their happy bird messages in their SyftBox directories:

```bash
echo "🐦 Today was amazing!" > ~/SyftBox/myusername/happybird.txt
```

## Development

### Running the Development Server

```bash
# Using the provided run script (recommended for SyftBox compatibility)
./run.sh

# Or manually with Python
python -m syft_widget.cli --package-name happybird_watcher --auto-discover --port 8005
```

### Project Structure

```
happybird-watcher/
├── happybird_watcher/       # Package source code
│   ├── __init__.py         # Package exports
│   ├── widgets.py          # Widget implementation
│   └── endpoints.py        # API endpoints
├── run.sh                  # SyftBox app runner
├── pyproject.toml         # Package configuration
└── README.md              # This file
```

## SyftBox Integration

This app integrates with SyftBox to:
- Monitor files across all SyftBox users
- Provide real-time updates
- Respect SyftBox permissions and security

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License - see LICENSE file for details
