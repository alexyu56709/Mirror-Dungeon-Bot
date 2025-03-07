from cx_Freeze import setup, Executable
import sys

# Include additional files
include_files = [
    ('ObjectDetection/UI/', 'ObjectDetection/UI/'),
]

# Specify build options
build_exe_options = {
    "include_files": include_files,
    "optimize": 0
}

# Create the executable
executables = [
    Executable(
        "Bot.py",
        base=None,  # Set to "Win32GUI" for a GUI app (no console)
        target_name="CGrinder.exe",
        icon="app_icon.ico"
    )
]

setup(
    name="CGrinder",
    version="1.0",
    description="Your bot application",
    options={"build_exe": build_exe_options},
    executables=executables
)