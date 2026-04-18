# Inazuma Eleven 2 Player Data Tools

A collection of Python scripts for reading, editing, and writing player data from **Inazuma Eleven 2** (Nintendo DS).

These tools allow you to inspect and modify player information and stats by working with the game's internal data files:

* `unitbase.dat`
* `unitbase.str`
* `unitstat.dat`

---

## ⚠️ Important Notice

**The `.dat` and `.str` files are NOT included in this repository.**

You must provide your own copies of:

* `unitbase.dat`
* `unitbase.str`
* `unitstat.dat`

These files should be extracted from your own copy of the game.

### Required Directory Structure

Place the files inside a directory named `ie_2_og` in the root of the project:

```
project_root/
│
├── ie_2_og/
│   ├── unitbase.dat
│   ├── unitbase.str
│   └── unitstat.dat
│
├── scripts/
│   └── ...
│
└── README.md
```

The scripts will not function correctly if this structure is not followed.

---

## Features

* Read and parse player base data (`unitbase.dat`)
* Decode string/profile data (`unitbase.str`)
* Read and modify player stats (`unitstat.dat`)
* Rebuild modified data back into game-compatible files

---

## Requirements

* Python 3.8 or higher

<!-- Install dependencies (if any):

```
pip install -r requirements.txt
``` -->

---

## Usage

Run scripts from the project root directory.

Example:

```
python -m read_ie_files
```

---

## Disclaimer

This project is intended for **educational and modding purposes only**.

* Do not distribute copyrighted game files.
* You are responsible for how you use this tool.
* Always keep backups of your original files before making changes.

---

## Contributing

Contributions are welcome. Feel free to open issues or submit pull requests to improve functionality, fix bugs, or expand support.

---

## License

This project is licensed under the MIT License (or specify your preferred license).
