from setuptools import setup

setup(
    name = "Flappy UFO",
    options = {
        "build_apps" : {
            # Files that we want to include. Specifically:
            #  * All of our image-files (.png)
            #  * All of our sound- and music-files (.ogg)
            #  * All of our text-files (.txt)
            #  * All of our 3D models (.egg)
            #    - These will be automatically converted
            #      to .bam files
            #  * And all of our font-files (in the "Font" folder)
            "include_patterns" : [
                "**/*.egg",
		"**/*.png"
            ],
            # We want a gui-app, and our "main" Python file
            # is "Game.py"
            "gui_apps" : {
                "Flappy UFO" : "FlappyUFO.py"
            },
            # Plugins that we're using. Specifically,
            # we're using OpenGL, and OpenAL audio
            "plugins" : [
                "pandagl"
            ],
            # Platforms that we're building for.
            # Remove those that you don't want.
            "platforms" : [
                "win_amd64",
                'macosx_10_6_x86_64',
            ],
            # The name of our log-file. We're keeping
            # the directory-name short--our title is kinda long--
            # and we're placing the file within the user's
            # "app-data" directory.
            "log_filename" : "$USER_APPDATA/FlappyUFO/output.log",
            # Instead of allowing log-data to accumulate,
            # we're here choosing to start the log fresh
            # on each run.
            "log_append" : False
        }
    }
)
