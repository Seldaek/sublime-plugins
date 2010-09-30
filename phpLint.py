import sublime, sublimeplugin, functools, re
from subprocess import STARTUPINFO, PIPE, Popen, STARTF_USESHOWWINDOW
from sublime import Region

##
# PHP Linter
# Lints automatically on file save, requires 'php' in the PATH env var
#
# @author Jordi Boggiano <j.boggiano@seld.be>
##

class phpLint(sublimeplugin.Plugin):
    def onPostSave(self, view):
        if view.fileName()[-4:] != '.php': return
        view.eraseRegions('phpLint')
        startupinfo = STARTUPINFO()
        startupinfo.dwFlags |= STARTF_USESHOWWINDOW
        file = Popen('php -l "'+view.fileName()+'"', stdout=PIPE, startupinfo=startupinfo).stdout

        if file.readline()[0:2] != 'No':
            sublime.setTimeout(functools.partial(self.updateStatus, view, file.readline().strip()), 100)

    def updateStatus(self, view, text):
        match = re.search('line (\d+)', text)
        if match is None or len(match.groups()) < 1: return
        sel = view.sel()
        point = view.textPoint(int(match.group(1))-1, 0)
        highlight = [view.line(point-1), view.line(point)]
        region = Region(point, point)

        view.show(point)
        sel.clear()
        sel.add(region)

        view.addRegions('phpLint', highlight, "identifier", sublime.DRAW_OUTLINED)

        sublime.statusMessage('<!> '+text);
