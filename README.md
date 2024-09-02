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

## Usage
- **Build the project**:
  ```bash
  make
  ```

- **Clean the project**:
  ```bash
  make clean
  ```

## File Structure
- **latex/**: LaTeX files for generating documents.
- **rec/**: Audio recordings.
- **csound/**: Csound files for audio processing.

## Csound processing

The `csound.py` script you provided seems to be responsible for orchestrating and generating sound events using Csound. Here’s a breakdown of how you can modify the script to change the overall tempo and how the script handles the dictionary of sound files and their maximum durations:

### Changing the Overall Tempo

The overall tempo, or the length of time for the fundamental harmonic (referred to as `duration0thHarmonics`), can be modified by adjusting the `duration0thHarmonics` parameter in the script.

```python
# Define the length of the line in seconds
duration0thHarmonics = 7.0
```

- To speed up the tempo (make the harmonic shorter), reduce the value of `duration0thHarmonics`.

- To slow down the tempo (make the harmonic longer), increase the value of `duration0thHarmonics`.

For example, setting `duration0thHarmonics = 5.0` will shorten the duration, making the tempo faster, while setting it to 10.0 will lengthen it, making the tempo slower.

### Modifying the Sound File Dictionary

The script defines a dictionary `COLOR_TO_SOUND_FILE` that maps identifiers (like '0', '1', etc.) to lists containing the corresponding sound file and its maximum duration.

```python
COLOR_TO_SOUND_FILE = {
    '0': ['../rec/1.wav', 0.4],  # File and maximum duration
    '1': ['../rec/2.wav', 1.0],  # File and maximum duration
    # Add more mappings if needed
}
```

- **Adding a New Entry**: To add a new sound file with a maximum duration, simply add another key-value pair to the dictionary. For example:

    ```python
    '2': ['../rec/3.wav', 0.8],
    ```

    This will associate the identifier `'2'` with the file `3.wav` and a maximum duration of 0.8 seconds.

- **Updating input.md**: When you add new keys to the `COLOR_TO_SOUND_FILE` dictionary, you must also update the `input.md` file to reflect these changes. The `input.md` file contains references or descriptions of the sound files used.

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

### Updating `input.md`

When you add a new key to the `COLOR_TO_SOUND_FILE` dictionary, you must update input.md to ensure that the new key is used correctly. Here’s a step-by-step guide:

- **Add a New Key to the Dictionary**

    If you add a new key-value pair to `COLOR_TO_SOUND_FILE`, for example:

    ```python
    '4': ['../rec/4.wav', 1.2],
    ```

    This means you now have a new sound file associated with the key '4'.

- **Update `input.md`**

    Add entries to `input.md` that use the new key. For example:
    
    ```
    1-5-3 4
    2-8-2 4
    ```

    These entries specify that the points 1-5-3 and 2-8-2 should now use the new sound file associated with key '4'.

- **Verify Consistency**

    Ensure that every key in `input.md` matches a valid key in the `COLOR_TO_SOUND_FILE` dictionary. Missing or incorrect keys can lead to errors in sound processing.

### Example of Updated input.md

Let’s say you previously had this in input.md:

```
1-2-1 0
1-3-2 1
2-4-0 2
```

And you added a new entry `'4': ['../rec/4.wav', 1.2]` to `COLOR_TO_SOUND_FILE`, you might update `input.md` to include:

```
1-2-1 0
1-3-2 1
2-4-0 2
3-5-1 4
```

Summary
- Modify `COLOR_TO_SOUND_FILE`: Add or update keys as needed.
- Update `input.md`: Add new entries or modify existing ones to include any new keys.
- Ensure Consistency: Verify that all keys in input.md are defined in `COLOR_TO_SOUND_FILE`.

By following these steps, you’ll maintain synchronization between your sound processing script and the `input.md` file, ensuring accurate and consistent audio processing.







