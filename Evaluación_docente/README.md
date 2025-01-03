
# Google Apps Script: Filter and Copy Rows by Type

This Google Apps Script is designed to filter rows in a Google Sheets spreadsheet based on a specific "type" value and copy the filtered data into new spreadsheets. It includes two main functions:

1. **`filterAndCopyByType`**: Prompts the user to select a type from the available types and creates a single new spreadsheet for that type.
2. **`filterAndCopyAllByType`**: Automatically processes all unique types and creates a new spreadsheet for each type.

## Features

- Filters data based on `UniqueID` and `AREA` columns in a sheet named `RawData`.
- Allows manual selection of a specific type or processes all types automatically.
- Creates new spreadsheets with filtered data.
- Copies additional sheets from the original spreadsheet while maintaining structure.

## Prerequisites

- A Google Sheets spreadsheet with a `RawData` sheet containing `UniqueID` and `AREA` columns.
- Google Apps Script editor access to add the script.

## Usage

### Setting Up the Script

1. Open your Google Sheet.
2. Navigate to **Extensions > Apps Script**.
3. Paste the provided script into the editor.
4. Save the script and give it a name (e.g., "FilterAndCopy").
5. Run the script and grant necessary permissions when prompted.

### Functions

#### `filterAndCopyByType`

1. Executes filtering based on user input for a specific type.
2. Creates a new spreadsheet with rows corresponding to the selected type.

#### `filterAndCopyAllByType`

1. Automatically filters and processes all unique types.
2. Creates separate spreadsheets for each unique type.

### Example

#### Filter and Copy by Specific Type

```javascript
function runFilterAndCopyByType() {
    filterAndCopyByType();
}
```

#### Filter and Copy All Types

```javascript
function runFilterAndCopyAllByType() {
    filterAndCopyAllByType();
}
```

### Notes

- Ensure the `RawData` sheet exists and contains the required columns (`UniqueID` and `AREA`).
- Excluded sheets (e.g., `P1 ASIGNATURA ABIERTA`, `P5 ASIGNATURA ABIERTA`, etc.) are ignored during processing.

## Errors and Troubleshooting

- **Sheet Not Found**: Ensure the `RawData` sheet is present.
- **No Data Found**: Verify that the `RawData` sheet has data starting from row 2.
- **Column Not Found**: Confirm the header row contains `UniqueID` and `AREA`.

