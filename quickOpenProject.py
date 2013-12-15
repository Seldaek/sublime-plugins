import sublime_plugin
import os

##
# Open project from a quickPanel
#
# Specify the directory holding all your project files as an argument to the command.
# Bind it via (examples):
#    { "keys": ["ctrl+shift+alt+p"], "command": "quick_open_project", "args": {"dir": "/foo/bar/sublime-projects"} },
#
# @author Jordi Boggiano <j.boggiano@seld.be>
##


class QuickOpenProjectCommand(sublime_plugin.WindowCommand):
    projects = []

    def want_file(self, f):
        root, ext = os.path.splitext(f)
        return os.path.isfile(f) and ext == '.sublime-project'

    def open_project(self, index):
        if index == -1:
            return
        # TODO fix this call, ST2/3 do not support it
        self.window.run_command('open_project', [self.projects[index]])

    def run(self, dir):
        projectsPath = str(dir)
        displayFiles = [f for f in os.listdir(projectsPath) if self.want_file(projectsPath + '/' + f)]
        displayFiles.sort()
        self.projects = [projectsPath + '/' + str(f) for f in displayFiles]
        for i in range(len(displayFiles)):
            displayFiles[i] = displayFiles[i].replace('.sublime-project', '')

        self.window.show_quick_panel(displayFiles, self.open_project)
