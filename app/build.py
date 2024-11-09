from cx_Freeze import setup, Executable
import datetime
from core.utils.settings import BUILD_VERSION

build_options = {
    "silent_level": 1,
    "silent": True,
    "build_exe": "dist",
    "include_msvcr": True,
    "includes": [],
    "optimize": 1,
    "include_files": [
        ("assets/komorebi.png", "app/assets/komorebi.png"),
        ("assets/komorebi.ico", "app/assets/komorebi.ico"),
        ("assets/checkmark.png", "app/assets/checkmark.png"),
        ("assets/chevron.png", "app/assets/chevron.png"),
    ]
}
directory_table = [
    ("ProgramMenuFolder", "TARGETDIR", "."),
    ("MyProgramMenu", "ProgramMenuFolder", "."),
]
msi_data = {
    "Directory": directory_table,
    "ProgId": [
        ("Prog.Id", None, None, "Komorebi Configurator", "IconId", None),
    ],
    "Icon": [
        ("IconId", "assets/komorebi.ico"),
    ],
}
bdist_msi_options = {
    "data": msi_data,
    "install_icon": "assets/komorebi.ico",
    "upgrade_code": "{0d14224f-3434-49ea-b526-682795f7c7f0}",
    "add_to_path": False,
    "dist_dir": "dist/out",
    "initial_target_dir": r'[LocalAppDataFolder]\KomoGUI',
    "all_users": False,
    "summary_data": {
        "author": "AmN",
        "comments": "Komorebi Configurator",
        "keywords": "windows; statusbar; ricing; customization; tiling; taskbar; komorebi",
    }
}
executables = [
    Executable(
        "main.py",
        base="gui",
        icon="assets/komorebi.ico",
        shortcut_name="KomoGUI",
        shortcut_dir="MyProgramMenu",
        copyright=f"Copyright (C) {datetime.datetime.now().year} AmN",
        target_name="komogui.exe",
    )
]
setup(
    name="KomoGUI",
    version=BUILD_VERSION,
    author="AmN",
    description="Komorebi Configurator",
    executables=executables,
    options={
        "build_exe": build_options,
        "bdist_msi": bdist_msi_options,
    },
)