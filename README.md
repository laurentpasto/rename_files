# Smart Image Renaming Tool

A Python script that helps you automatically rename image files based on their containing folders.

## Features

- Recursively processes multiple folders
- Automatically detects artist/creator names from folder paths
- Renames files according to pattern: `Artist_ProjectName_01.jpg`
- Handles various image formats (jpg, png, gif, etc.)
- Preserves original file extensions
- Sequential numbering within each folder
- Skip files that have already been renamed
- Handles filename conflicts with unique identifiers

## Requirements

- Python 3.x
- No additional packages required (uses only standard library)

## Installation

1. Download the `smart_rename_images02.py` file to your computer
2. Make it executable (optional, for macOS/Linux users):
   ```
   chmod +x smart_rename_images02.py
   ```

## Usage Instructions

### Running the Script

1. Open Terminal or Command Prompt
2. Navigate to the folder containing the script:
   ```
   cd /path/to/script/folder
   ```
3. Run the script:
   ```
   python3 smart_rename_images02.py
   ```

### Setup Process

When you run the script, it will guide you through the following steps:

1. **Enter artist folder names**
   - Enter each artist/creator name (one per line)
   - These should match the folder names in your directory structure
   - Press Enter twice when done
   - Example input:
     ```
     Artist1
     Artist2
     Artist3
     [Enter]
     ```

2. **Enter the root folder path**
   - The base directory to start processing from
   - All subdirectories of this path will be scanned
   - Example: `/Users/username/Desktop/Photos`

3. **Enter default artist name**
   - Used only if no artist name can be detected from the folder path
   - This is optional - you can leave it blank

4. **Enter maximum folder depth**
   - Controls how deep into the folder structure the script will go
   - Leave blank for unlimited depth
   - Enter 1 to process only immediate subfolders, 2 for subfolders of subfolders, etc.

5. **Confirm the operation**
   - Review the settings
   - Type 'y' to proceed or 'n' to cancel

### File Naming Process

The script will:
1. Find image files in each folder
2. Detect the artist name from the folder path (or use default)
3. Use the current folder name as the project name
4. Rename files to: `ArtistName_ProjectName_01.ext`
5. Increment numbers for multiple files: `ArtistName_ProjectName_02.ext`, etc.

## Example

If your folder structure looks like this:
```
Photos/
├── Artist1/
│   ├── Project1/
│   │   ├── image1.jpg
│   │   └── image2.jpg
│   └── Project2/
│       └── image3.png
└── Artist2/
    └── Project3/
        ├── img001.jpg
        └── img002.jpg
```

After running the script, it will become:
```
Photos/
├── Artist1/
│   ├── Project1/
│   │   ├── Artist1_Project1_01.jpg
│   │   └── Artist1_Project1_02.jpg
│   └── Project2/
│       └── Artist1_Project2_01.png
└── Artist2/
    └── Project3/
        ├── Artist2_Project3_01.jpg
        └── Artist2_Project3_02.jpg
```

## Troubleshooting

- **No files renamed**: Check if the path is correct and contains image files
- **Python command not found**: Try using `python3` instead of `python`
- **Permission error**: Make sure you have write permissions for the folders
- **Artist name not detected**: Ensure the artist names you entered match the folder names exactly

## Customization

You can edit the script to:
- Change the separator character (currently `_`)
- Add additional image file extensions
- Modify the naming pattern

## Safety Features

- The script shows you what it will do before proceeding
- It only processes image files, leaving other files untouched
- It handles errors gracefully without crashing