#!/usr/bin/env python3
import os
import re

def detect_artist_from_path(folder_path, artist_folders):
    """
    Detects artist name from the folder path by checking if any of the folders
    in the path match the known artist folders.
    
    Args:
        folder_path (str): The folder path to check
        artist_folders (list): List of known artist folder names
    
    Returns:
        str: Detected artist name or None if not found
    """
    path_parts = folder_path.split(os.path.sep)
    for part in path_parts:
        if part in artist_folders:
            return part
    return None

def rename_images_in_folder(folder_path, artist_folders, default_artist=None, project_name=None):
    """
    Renames image files in the specified folder.
    
    Args:
        folder_path (str): Path to the folder containing images
        artist_folders (list): List of known artist folder names
        default_artist (str, optional): Default artist name if none is detected
        project_name (str, optional): Custom project name. If None, use folder name
    
    Returns:
        int: Number of files renamed
    """
    # Define image file extensions to look for
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.psd']
    
    # If no project name is specified, use the folder name
    if project_name is None:
        project_name = os.path.basename(folder_path)
    
    # Detect artist name from the path or use default
    artist_name = detect_artist_from_path(folder_path, artist_folders) or default_artist
    if not artist_name:
        print(f"Warning: Could not detect artist for {folder_path}, skipping...")
        return 0
    
    # Get all files in the directory
    try:
        files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    except FileNotFoundError:
        print(f"Error: Folder not found - {folder_path}")
        return 0
    except PermissionError:
        print(f"Error: Permission denied for folder - {folder_path}")
        return 0
    
    # Filter out only image files
    image_files = [f for f in files if any(f.lower().endswith(ext) for ext in image_extensions)]
    
    # Sort the files to ensure consistent numbering
    image_files.sort()
    
    print(f"\nProcessing folder: {folder_path}")
    print(f"Artist detected: {artist_name}")
    print(f"Project name: {project_name}")
    print(f"Found {len(image_files)} image files")
    
    # Track renamed files
    renamed_count = 0
    
    # Rename each image file
    for i, old_filename in enumerate(image_files, 1):
        # Skip files that already match our naming pattern
        if re.match(f"{re.escape(artist_name)}_{re.escape(project_name)}_\\d+", old_filename):
            print(f"Skipping already renamed file: {old_filename}")
            continue
            
        # Get file extension
        _, extension = os.path.splitext(old_filename)
        
        # Create new filename
        new_filename = f"{artist_name}_{project_name}_{i:02d}{extension}"
        
        # Full paths
        old_path = os.path.join(folder_path, old_filename)
        new_path = os.path.join(folder_path, new_filename)
        
        # If the new filename already exists, add a unique identifier
        if os.path.exists(new_path):
            import uuid
            unique_id = str(uuid.uuid4())[:8]
            new_filename = f"{artist_name}_{project_name}_{i:02d}_{unique_id}{extension}"
            new_path = os.path.join(folder_path, new_filename)
        
        # Rename the file
        try:
            print(f"Renaming: {old_filename} -> {new_filename}")
            os.rename(old_path, new_path)
            renamed_count += 1
        except (OSError, PermissionError) as e:
            print(f"Error renaming {old_filename}: {e}")
    
    return renamed_count

def process_directory_structure(root_path, artist_folders, default_artist=None, max_depth=None, current_depth=0):
    """
    Recursively process a directory structure to find folders to rename images in.
    
    Args:
        root_path (str): Root path to start from
        artist_folders (list): List of known artist folder names
        default_artist (str, optional): Default artist name if none is detected
        max_depth (int, optional): Maximum folder depth to process
        current_depth (int): Current depth in the folder hierarchy
    
    Returns:
        int: Total number of files renamed
    """
    # Check if we've exceeded the maximum depth
    if max_depth is not None and current_depth > max_depth:
        return 0
    
    total_renamed = 0
    
    try:
        # Get all entries in the current directory
        entries = os.listdir(root_path)
        
        # Process directories
        for entry in entries:
            entry_path = os.path.join(root_path, entry)
            
            # Skip hidden folders and files
            if entry.startswith('.'):
                continue
                
            if os.path.isdir(entry_path):
                # Process images in this folder
                renamed = rename_images_in_folder(entry_path, artist_folders, default_artist)
                total_renamed += renamed
                
                # Recursively process subfolders
                sub_renamed = process_directory_structure(
                    entry_path, artist_folders, default_artist, max_depth, current_depth + 1
                )
                total_renamed += sub_renamed
    
    except (PermissionError, FileNotFoundError) as e:
        print(f"Error accessing {root_path}: {e}")
    
    return total_renamed

def load_artist_list():
    """Load list of common artist folder names."""
    # You can customize this list with your own folder names
    folder_names = []
    return folder_names

if __name__ == "__main__":
    print("Smart Image Renaming Tool")
    print("========================\n")
    
    # Get artist folders from user
    print("Enter artist folder names (one per line, press Enter twice when done):")
    artist_folders = []
    while True:
        artist = input().strip()
        if not artist:
            break
        artist_folders.append(artist)
    
    if not artist_folders:
        artist_folders = load_artist_list()
        if not artist_folders:
            print("Warning: No artist folders specified.")
    
    print(f"Using {len(artist_folders)} artist folder names")
    
    # Get the root path to start from
    root_path = input("Enter the root folder path to start processing: ").strip()
    if not root_path:
        root_path = os.getcwd()
    
    # Default artist name (used only if no artist can be detected from path)
    default_artist = input("Enter default artist name (used only if no artist detected): ").strip()
    
    # Ask for maximum depth
    max_depth_input = input("Enter maximum folder depth to process (leave blank for unlimited): ").strip()
    max_depth = int(max_depth_input) if max_depth_input else None
    
    # Confirm before proceeding
    print(f"\nWill process image files in: {root_path}")
    print(f"Default artist (if none detected): {default_artist or 'None'}")
    if artist_folders:
        print(f"Artist folders to look for: {', '.join(artist_folders)}")
    if max_depth is not None:
        print(f"Maximum folder depth: {max_depth}")
    else:
        print("Maximum folder depth: Unlimited")
        
    print("\nWARNING: This will rename multiple files across multiple folders!")
    confirm = input("Proceed? (y/n): ").lower()
    
    if confirm == 'y':
        print("\nProcessing folders...")
        total_renamed = process_directory_structure(root_path, artist_folders, default_artist, max_depth)
        print(f"\nTotal files renamed: {total_renamed}")
    else:
        print("Operation cancelled.")