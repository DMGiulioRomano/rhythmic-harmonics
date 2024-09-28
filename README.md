# Rhythmic-harmonics

## Description
This project involves generating rhythmic harmonic structures using LaTeX and Csound. It includes audio processing, document generation, and scripting to automate these tasks.

## Dependencies
- **Python**: Required to run the scripts (`latex.py`, `csound.py`).
- **LaTeX**: Required for document generation.
- **Csound**: Required for sound processing.

## Installation
1. Install [Python](https://www.python.org/downloads/).
2. Install LaTeX (e.g., TeX Live, MiKTeX).
3. Install [Csound](https://csound.com/download.html).


## File Structure
- **latex/**: LaTeX files for generating documents.
- **rec/**: Audio recordings.
- **csound/**: Csound files for audio processing.

## Usage
- **Build the project**:
  ```bash
  make
  ```

- **Clean the project**:
  ```bash
  make clean
  ```

## Configuration
The project is configured via the `config.ini` file, which defines the sound files, project parameters, and LaTeX layout settings.

### Editing Sound Files
To change the sound files used in the project, modify the `[SoundFiles]` section in config.ini:

  ```ini
[SoundFiles]
0 = ../rec/1.wav, 0.4
1 = ../rec/2.wav, 1.0
  ```

Each entry consists of a key, followed by the path to the sound file and an optional parameter (e.g., volume or duration).

### Adjusting Project Parameters
You can modify various parameters in the `[Parameters]` section of config.ini. For example:

  ```ini
[Parameters]
poly = False
duration0thHarmonics = 4.0
  ```
 - `poly`: Controls polyphonic behavior.
 - `duration0thHarmonics`: Defines the duration of the fundamental harmonic. Adjust this value to speed up or slow down the tempo.

### Configuring LaTeX Layout

The LaTeX color scheme and input markdown file can be set in the `[Latex]` section of `config.ini`:

  ```ini
[Latex]
layoutTempColor = 0:black, 1:red, 2:green, 3:violet
input_markdown = ../input.md
  ```
  - `layoutTempColor`: Defines the colors used in LaTeX outputs.
  - `input_markdown`: Specifies the path to the markdown file used for input.


## `input.md` Structure and Usage

The `input.md` file is organized in a way that maps rhythmic harmonic points to specific sound files. The format is as follows:

- **First Number**: Indicates the repetition of the entire block of harmonics.

- **Second Number**: Refers to the line in the harmonic structure.

- **Third Number**: Identifies the specific point on that line.

- **Number After Space**: Represents the dictionary key, which corresponds to the sound file to be used.

**Example Entry**

```
1-2-1 0
```

- 1: Repetition of the block.

- 2: Line number in the harmonic structure.

- 1: Point number on the line.

- 0: Key in the `COLOR_TO_SOUND_FILE` dictionary, indicating the sound file to use.

## Updating `input.md`

Ensure that the keys in input.md correspond to valid entries in `config.ini`. If you add a new sound file in the `[SoundFiles] `section, update input.md to reference this new key. For example, if you add:

```ini
4 = ../rec/4.wav, 1.2
```

Then update input.md like so:

```
1-2-1 0
1-3-2 1
3-5-1 4
```

This keeps your project consistent and ensures proper sound file usage.





