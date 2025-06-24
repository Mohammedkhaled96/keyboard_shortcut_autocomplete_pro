import os.path

# Build customizations
# Change this file instead of sconstruct or manifest files, whenever possible.

# For translation support - define _ as a no-op function if not in NVDA environment
try:
    _
except NameError:
    def _(text):
        return text

# Full name of the add-on
addon_info = {
    # for previously unpublished addons, please follow the community guidelines at:
    # https://bitbucket.org/nvdaaddonteam/todo/raw/master/guidelines.txt
    # add-on Name, internal for NVDA
    "addon_name": "keyboardShortcutsPro",
    # Add-on summary, usually the user visible name of the addon.
    # Translators: Summary for this add-on
    # to be shown on installation and add-on information found in Add-ons Manager.
    "addon_summary": _("Keyboard Shortcut Autocomplete Professional"),
    # Add-on description
    # Translators: Long description to be shown for this add-on on add-on information from add-ons manager
    "addon_description": _("""Professional text expansion addon for NVDA that allows you to define abbreviations and expand them into full text.

Features:
• Define custom text shortcuts and their expansions
• Expand shortcuts instantly with NVDA+E
• Professional shortcuts manager with search, import/export capabilities
• Support for multiple languages including Arabic and English
• Undo last expansion with NVDA+Shift+E
• Live hints while typing to show available expansions
• Quick shortcuts list with NVDA+Shift+L
• Import/Export shortcuts for backup and sharing
• Thread-safe and reliable operation

Keyboard shortcuts:
• NVDA+E: Expand shortcut at cursor
• NVDA+Shift+K: Open shortcuts manager
• NVDA+Alt+Shift+K: Toggle addon enabled/disabled
• NVDA+Shift+E: Undo last expansion
• NVDA+Shift+S: Show if word at cursor is a shortcut
• NVDA+Shift+L: List all shortcuts

Perfect for:
• Email addresses and signatures
• Common phrases and greetings
• Technical terms and jargon
• Multi-language text expansion
• Productivity enhancement
• Reducing typing effort and errors"""),
    # version
    "addon_version": "1.1.1",
    # Author(s)
    "addon_author": "Mohammed Khaled Mahmoud <mohammed.khaled.mahmoud1996@gmail.com>",
    # URL for the add-on documentation support
    "addon_url": "https://github.com/Mohammedkhaled96/keyboard_shortcut_autocomplete_pro",
    # URL for the add-on repository where the source code can be found
    "addon_sourceURL": "https://github.com/Mohammedkhaled96/keyboard_shortcut_autocomplete_pro",
    # Documentation file name
    "addon_docFileName": "readme.html",
    # Minimum NVDA version supported (e.g. "2018.3.0", minor version is optional)
    "addon_minimumNVDAVersion": "2019.3.0",
    # Last NVDA version supported/tested (e.g. "2018.4.0", ideally more recent than minimum version)
    "addon_lastTestedNVDAVersion": "2024.1.0",
    # Add-on update channel (default is None, denoting stable releases,
    # and for development releases, use "dev".)
    # Do not change unless you know what you are doing!
    "addon_updateChannel": "stable",
    # Add-on license such as GPL 2
    "addon_license": "GPL v2",
    # URL for the license document the ad-on is licensed under
    "addon_licenseURL": "https://www.gnu.org/licenses/gpl-2.0.html",
}

# Define the python files that are the sources of your add-on.
# You can either list every file (using ""/") as a path separator,
# or use glob expressions.
# For example to include all files with a ".py" extension from the "globalPlugins" dir of your add-on
# pythonSources = ["addon/globalPlugins/*.py"]
# For more information on SCons Glob expressions please take a look at:
# https://scons.org/doc/production/HTML/scons-user/apd.html
pythonSources = [
    os.path.join("addon", "globalPlugins", "keyboardShortcutAutocomplete.py"),
    os.path.join("addon", "globalPlugins", "__init__.py"),
]

# Files that contain strings for translation. Usually your python sources
i18nSources = pythonSources + ["buildVars.py"]

# Files that will be ignored when building the nvda-addon file
# Paths are relative to the addon directory, not to the root directory of your addon sources.
excludedFiles = [
    "*.pyc",
    "*.pyo",
    "__pycache__",
    ".git",
    ".gitignore",
    ".github",
    "*.md",
    ".vscode",
    ".idea",
    "*.sublime-*",
    "tests",
    "docs",
    "*.log",
    "*.tmp",
    "*.bak",
    "*~",
    "desktop.ini",
    "Thumbs.db",
    ".DS_Store"
]

# Base language for the NVDA add-on
# If your add-on is written in a language different than english,
# modify this variable.
baseLanguage = "en"

# Markdown extensions for add-on documentation
# Most add-ons do not require additional Markdown extensions.
# If you need to add support for markup such as tables, fill out the below list.
# Extensions string must be of the form "markdown.extensions.extensionName"
# e.g. "markdown.extensions.tables" to add tables.
markdownExtensions = []