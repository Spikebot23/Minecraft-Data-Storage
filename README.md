# Minecraft Data Storage

A Python project that encodes a file into a Minecraft world and decodes the stored data back into a file.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [How It Works](#how-it-works)
- [Configuration](#configuration)
- [Limitations](#limitations)
- [License](#license)
- [Contact](#contact)

## Features

- Encodes file data as colored stained glass blocks in a Minecraft world.
- Reads and copies a template Minecraft world before storing the data.
- Supports the data file being provided through an interactive filename prompt.
- Stores the original filename and file size in a binary header.
- Decodes stored values and recreates a file in the project directory.
- Can encode text and binary source files.

## Prerequisites

- Python 3.9 or newer
- The `anvil` Python package

## Installation

1. Clone or download this project.
2. Open a terminal in the project directory.
3. Install the required Python package:

   ```bash
   pip install anvil-parser
   ```

## Usage

### Encode a File

Place the file you want to encode in the project directory, or provide its path when prompted.

Run:

```bash
python Encode.py
```

At the prompt, enter the source filename:

```text
Enter file to encode>> cat.jpg
```

Press Enter without typing a filename to encode `DataStorage.txt` by default.

The encoded world is created or updated at:

```text
DataStorage_Save/
```

### Decode a World

Run:

```bash
python Decode.py
```

Enter the name of the world directory to decode:

```text
Enter file to Decode>> DataStorage_Save
```

Currently, enter `DataStorage_Save` at the prompt to decode the default encoded world.

Decoded files are saved in the project directory with a `new-` prefix. For example, decoding `DataStorage.txt` creates:

```text
new-DataStorage.txt
```

## How It Works

Each encoded byte is split into hundreds, tens, and ones values. These values are mapped to one of ten block types:

| Digit | Block |
| --- | --- |
| 0 | Air |
| 1 | Red stained glass |
| 2 | Orange stained glass |
| 3 | Yellow stained glass |
| 4 | Lime stained glass |
| 5 | Green stained glass |
| 6 | Cyan stained glass |
| 7 | Light blue stained glass |
| 8 | Purple stained glass |
| 9 | Pink stained glass |

The encoder adds an `EMRS` marker, filename length, file size, original filename, and file bytes to the payload. Each byte is stored across three vertical block positions.

The decoder reads these blocks, reconstructs the byte values, validates the `EMRS` marker, and writes the recovered file.

## Configuration

- `DataStorage.txt` - Default file encoded when no filename is entered.
- `DataStorageTemplate` - Minecraft Java Edition world used as the source template.
- `DataStorage_Save` - Output world created by the encoder.
- `Encode.py` - Encodes a file into the world.
- `Decode.py` - Decodes a stored world back into a file.

## Limitations

- The decoder currently reconstructs and writes decoded data as UTF-8 text. Files containing arbitrary binary bytes may not decode correctly.
- The decoder and encoder are intended to be run with the project directory as the working context.

## License

MIT License

Copyright (c) 2026 Spikebot23

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## Contact

Name: Emeris Stripling

Email: the.real.spike.23+HackClub@gmail.com

GitHub:# Minecraft Data Storage

