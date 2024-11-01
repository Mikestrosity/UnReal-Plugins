from unreal import ToolMenuContext, ToolMenus, ToolMenuEntryScript, uclass, ufunction
import sys
import os
import importlib
import tkinter

# Get the source directory of the current script
srcDir = os.path.dirname(os.path.abspath(__file__))
if srcDir not in sys.path:
    sys.path.append(srcDir)  # Add the source directory to Python's path

# Import the UnrealUtilities module and reload it to get the latest version
import UnrealUtilities
importlib.reload(UnrealUtilities)

@uclass()
class LoadFromDirEntryScript(ToolMenuEntryScript):
    @ufunction(override=True)
    def execute(self, context):
        # Create a Tkinter window to select a directory
        window = tkinter.Tk()
        window.withdraw()  # Hide the main window
        fileDir = tkinter.filedialog.askdirectory()  # Open a dialog to select a directory
        window.destroy()  # Destroy the window after selection
        # Call the LoadFromDir method from UnrealUtilities with the selected directory
        UnrealUtilities.UnrealUtility().LoadFromDir(fileDir)

@uclass()
class BuildBaseMaterialEntryScript(ToolMenuEntryScript):
    @ufunction(override=True)
    def execute(self, context: ToolMenuContext) -> None:
        # Call the FindOrCreateBaseMaterial method from UnrealUtilities
        UnrealUtilities.UnrealUtility().FindOrCreateBaseMaterial()

class UnrealSubstancePlugin:
    def __init__(self):
        # Initialize the plugin with a submenu name and label
        self.subMenuName = "SubstancePlugin"
        self.subMenuLabel = "SubstancePlugin"
        self.InitUI()  # Call the UI initialization method

    def InitUI(self):
        # Find the main menu and add a new submenu for the plugin
        mainMenu = ToolMenus.get().find_menu("LevelEditor.MainMenu")
        self.subMenu = mainMenu.add_sub_menu(mainMenu.menu_name, "", "SubstancePlugin", "Substance Plugin")
        # Add menu entries for the functionalities
        self.AddEntryScript("BuildBaseMaterial", "Build Base Material", BuildBaseMaterialEntryScript())
        self.AddEntryScript("LoadFromDir", "Load From Directory", LoadFromDirEntryScript())
        ToolMenus.get().refresh_all_widgets()  # Refresh the UI to reflect the new menu

    def AddEntryScript(self, name, label, script: ToolMenuEntryScript):
        # Initialize and register a new menu entry script
        script.init_entry(self.subMenu.menu_name, self.subMenu.menu_name, "", name, label)
        script.register_menu_entry()

# Instantiate the UnrealSubstancePlugin to set it up
UnrealSubstancePlugin()