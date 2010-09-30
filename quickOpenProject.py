import sublime, sublimeplugin, os

##
# Open project from a quickPanel
#
# Specify the directory holding all your project files as an argument to the command.
# Bind it via (examples):
#  <binding key="ctrl+shift+p" command="quickOpenProject 'C:/Users/seld/Web/projects'" />
#
# @author Jordi Boggiano <j.boggiano@seld.be>
##

class quickOpenProject(sublimeplugin.WindowCommand):
    allowedExtensions = ['.sublime-project']

    def wantFile(self, f):
        root, ext = os.path.splitext(f)
        return os.path.isfile(f) and ext in self.allowedExtensions

    def run(self, window, args):
        projectsPath = str(args[0])
        displayFiles = [f for f in os.listdir(projectsPath) if self.wantFile(projectsPath+'/'+f)]
        displayFiles.sort()
        projectFilesPath = [projectsPath+'/'+str(f) for f in displayFiles]
        for i in range(len(displayFiles)):
            for ext in self.allowedExtensions:
                displayFiles[i] = displayFiles[i].replace(ext, '')

        window.showQuickPanel("", "openProject", projectFilesPath, displayFiles,
            sublime.QUICK_PANEL_FILES | sublime.QUICK_PANEL_MULTI_SELECT)