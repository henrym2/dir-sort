# Python sorting script

A simple python3 sorting script, made to clean up normally disorganized folders like Downloads or Documents, without applying any opinionated structure

## Usage

Just drop the script in the folder you want to sort and run with:

`>python3 sort.py /`

The script will then sort that directory using the relative path. Be careful with the path to avoid causing issues in your system

### Config

The script is configured by modifying the config class at the end of the file. Additional file types/folders can be added with entries into the folders dictionary.

```python
class config:
    folders = {
        "images": ("png", "jpg", "gif", "ps", "svg", "ico", "bmp", "jpeg"),
        "videos": ("mp4", "avi", "wmv", "m4v"),
        "spreadsheets": ("xlsx", "xls", "xlsm"),
        "docs": ("pdf", "docx", "txt", "pptx", "ppt", "doc", "tex"),
        "executable": ("exe", "py", "bin", "bat", "apk", "com", "msi", "jar"),
        "archives": ("rar", "zip", "iso", "7z", "pkg", "gz", "tar", "z", "bin"),
        "ebooks": ("epub", "mobi"),
        "misc": (),
        "backup": (),
    }
    dangerousPaths = (
        "/",
        ":\\",
        "/home",
        "/etc",
        "/bin",
        "*:\\*\\*",
        "C:",
        "D:",
    )

    safePaths = (
        "/Downloads",
        "/Documents",
    )
```


### Arguments
```bash
>python3 sort.py PATH
```
Path is a required argument. The path argument is relative to the current working directory, so if you're currently in C:/Users/Username/Downloads then a path of `/` would act on that directory and any sub directories.

```bash
>python3 -force sort.py / # -f
```
Force the script to run in unsafe mode, ignoring the configured "dangerous" paths. It's not recommended to ever pass this flag unless you know exactly what you're doing. 

```bash
>python3 -depth DEPTH sort.py / #-d
```
Direct the script to run through a deeper level in the directory tree. For safeties sake default is 0. Can be thought of as how deep in subdirectories a user may want to have sorted. This is purposely set low to minimize damage incase a user runs the script in an unsafe directory unintentionally

```bash
>python3 -safe sort.py / #-s
```
Direct the script to run in safe mode, preventing it from running outside of the "safePaths" as configured in the config class at the bottom of the script

```bash
>python3 -backup sort.py / #-b
```
>Currently disabled due to recursive archives

Direct the script to zip and backup the current state of the folder **before** sorting is attempted
