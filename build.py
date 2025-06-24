import os
import sys
import zipfile
import shutil
from datetime import datetime

def build_addon():
    """Build the NVDA addon package"""
    
    # Import build variables
    try:
        import buildVars
        addon_info = buildVars.addon_info
    except ImportError:
        print("Error: buildVars.py not found!")
        return False
    
    # Get addon info
    name = addon_info["addon_name"]
    version = addon_info["addon_version"]
    
    # Output filename
    output_file = f"{name}-{version}.nvda-addon"
    
    print(f"Building {addon_info['addon_summary']} v{version}")
    print("-" * 50)
    
    # Check required directories
    if not os.path.exists("addon"):
        print("Error: 'addon' directory not found!")
        return False
    
    # Check for required files
    required_files = [
        "addon/manifest.ini",
        "addon/globalPlugins/__init__.py",
        "addon/globalPlugins/keyboardShortcutAutocomplete.py"
    ]
    
    for file_path in required_files:
        if not os.path.exists(file_path):
            print(f"Error: Required file '{file_path}' not found!")
            return False
    
    # Create the addon package
    print(f"\nCreating {output_file}...")
    
    try:
        with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as zf:
            # Walk through addon directory
            for root, dirs, files in os.walk("addon"):
                # Skip excluded directories
                dirs[:] = [d for d in dirs if not any(
                    d.startswith(ex.replace("*", "")) for ex in buildVars.excludedFiles
                )]
                
                for file in files:
                    # Skip excluded files
                    if any(file.endswith(ex.replace("*", "")) for ex in buildVars.excludedFiles):
                        continue
                    
                    file_path = os.path.join(root, file)
                    # Create the archive name relative to addon directory
                    arcname = os.path.relpath(file_path, "addon")
                    arcname = arcname.replace("\\", "/")  # Use forward slashes
                    
                    print(f"  Adding: {arcname}")
                    zf.write(file_path, arcname)
        
        # Get file size
        size = os.path.getsize(output_file) / 1024
        
        print(f"\n{'='*50}")
        print(f"Build completed successfully!")
        print(f"{'='*50}")
        print(f"\nAddon file: {output_file}")
        print(f"File size: {size:.2f} KB")
        print(f"\nInstallation instructions:")
        print(f"1. Open NVDA")
        print(f"2. Go to Tools → Manage add-ons (NVDA+N, T, A)")
        print(f"3. Click 'Install from external source' or press Alt+I")
        print(f"4. Browse to and select: {output_file}")
        print(f"5. Follow the installation prompts")
        print(f"6. Restart NVDA when prompted")
        print(f"\nUsage:")
        print(f"- Type a shortcut and press NVDA+E to expand it")
        print(f"- Press NVDA+Shift+K to manage shortcuts")
        print(f"- Press NVDA+Alt+Shift+K to enable/disable")
        
        return True
        
    except Exception as e:
        print(f"\nError creating addon package: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main function"""
    # Change to script directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Build the addon
    success = build_addon()
    
    # Exit code
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
    input("\nPress Enter to close...")