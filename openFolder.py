import sublime, sublime_plugin, os, subprocess

class OpenFolderCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        if not self.view.file_name():
            return
        folder_name, file_name = os.path.split(self.view.file_name())

        # handle network mounts
        if folder_name[2:4] == '\\\\':
            folder_name = folder_name[0:3] + folder_name[4:]

        command = "explorer " + folder_name
        subprocess.Popen(command)