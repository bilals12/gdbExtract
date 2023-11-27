# gdbExtract

## overview
this is a python script designed to automate process of extracting function information from binary files using the GNU debugger (GDB). in case u don't want to use IDA or any other GUI that feels cumbersome, this tool will come in handy. it's particularly useful for reverse engineering, vulnerability assessment, and other analysis. there's a full write up on my blog, here.

## features
- automated extraction: quickly extracts function data from binaries using GDB
- JSON output: structures extracted data into a readable and easily manipulable JSON format
- data filtering + aggregation: filter out "safe" functions and aggregate data for functions that appear multiple times
- CLI: simple CLI for interacting with the script

## installation
you will need python and GDB installed on your system. 

- clone the repo
```bash
git clone https://github.com/bilals12/gdbExtract.git
cd gdbExtract
```

## usage
*note*: the paths to the binary file and output file are hardcoded inside the script. you will have to modify them. if you want to just enter the paths as args inside the CLI, the script will have to be modified accordingly.

1. `search`
- runs GDB to extract function information from binary file specified in `BINARY_PATH`
- parses GDB output to get details of each function
- saves data in JSON file specified in `DATA_FILE`

```bash
python gdbExtract.py search
```

the extracted function data will look something like this
```json
[
    {
        "address": "0x00401350",
        "name": "main",
        "signature": "int main()"
    },
    {
        "address": "0x00401390",
        "name": "helper_function",
        "signature": "void helper_function(int)"
    },
    // etc...
]
```

2. `remove-safe`
- filters out functions deemed "safe" from analysis
- reads JSON from previous step, removes functions labeled "safe" and saves filtered data in a new JSON file

```bash
python gdbExtract.py remove-safe
```

3. `combine`
- aggregates data for functions appearing multiple times
- reads filtered data and combines entries for same function, keeping track of occurrences

```bash
python gdbExtract.py combine
```

```json
{
    "helper_function": {
        "addresses": ["0x00401390", "0x00401500"],
        "signature": "void helper_function(int)",
        "count": 2
    },
    // etc...
}
```

4. `list` and `find`
- `list` will list all functions
```
0x00401350: main
0x00401390: helper_function
// etc...
```

- `find` will search for a specific function by name or address
```
enter a function address or name: main
found 0x00401350: main
```

if it can't find the function, it will spit back an error

```
enter a function address or name: unknown_function
could not find function with address or name 'unknown_function'.
```

## testing
i've also included a unit testing script. it's good practice to make sure each part functions as expected. it will also validate the logic and data handling. 
- mocking: uses `unittest.mock.patch` to mock external dependencies like file operations (`open`) and subprocess calls
- file testing: in `test_read_write_json_file`, an actual file is written and read. it's a simple way to test file I/O but you might want to mock this operation as well
- output testing: for `list_functions` and `search_function`, `sys.stdout` is captured to test console output
