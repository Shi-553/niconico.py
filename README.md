![niconico](https://img.shields.io/badge/niconico-(%E5%B8%B0%E3%81%A3%E3%81%A6%E3%81%8D%E3%81%9F)-auto?logo=niconico&logoColor=%23e6e6e6&color=%23252525)

[![PyPI](https://img.shields.io/pypi/v/niconico.py-ma?logo=pypi)](https://pypi.org/project/niconico.py-ma/)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/niconico.py-ma?logo=pypi)
![PyPI - Downloads](https://img.shields.io/pypi/dm/niconico.py-ma?logo=pypi)
![PyPI - License](https://img.shields.io/pypi/l/niconico.py-ma?logo=pypi)

[![Test](https://github.com/Shi-553/niconico.py/actions/workflows/release.yml/badge.svg)](https://github.com/Shi-553/niconico.py/actions/workflows/release.yml)
[![Test](https://github.com/Shi-553/niconico.py/actions/workflows/pypi.yml/badge.svg)](https://github.com/Shi-553/niconico.py/actions/workflows/pypi.yml)

# <img src="https://avatars.githubusercontent.com/u/113749892" height="30" /> niconico.py-ma

niconico.py-ma is a Python library for retrieving Niconico video content and information, and is compatible with the latest version of Niconico.
This is a Music Assistant fork with additional features and improvements.
It allows you to download videos, retrieve information, get comments, and more.

## Requirement

To use the video download function, you need to install [FFmpeg](https://www.ffmpeg.org/) and set the path.

## Installation

You can install it using pip:
```bash
pip install niconico.py-ma
```

## Usage

```python
from niconico import NicoNico
client = NicoNico()
```

### Examples

All examples can be found [here](https://github.com/Shi-553/niconico.py/tree/main/examples).

## Original Project

This is a fork of [niconico.py](https://github.com/niconicolibs/niconico.py) by Negima1072, enhanced for Music Assistant integration.

## Command

Console commands are available, see the following commands for usage:
```bash
niconico -h
```

## Contributing

All contributions are welcome, but please:
- Use the `develop` branch.
- Follow PEP8.
- Be clear about the meaning and purpose of your issue or PR.

## License

[MIT License](LICENSE)
