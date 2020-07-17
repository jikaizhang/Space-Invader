from cx_Freeze import Executable, setup

# executables = [cx_Freeze.Executable("Space_Invaders.py")]

target = Executable(
	script = "Space_Invaders.py",
	# shortcutName = "Space Invaders",
	# shortcutDir = "DesktopFolder",
	base = "Win32GUI",
    icon = "C:/Users/jzhan/Desktop/SpaceInvader/resources/icon.ico"
	)

setup(
	name = "Space Invaders",
	options = {
		"build_exe": 
		{
			"packages": ["pygame"], 
			"include_files": ["resources"],
			"excludes": ["numpy", "test", "tkinter"]
		}
		# "bdist_msi": {"initial_target_dir": "Desktop"}
	},
	executables = [target]
	)