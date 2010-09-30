import sublime, sublimeplugin, functools, re
from subprocess import STARTUPINFO, PIPE, Popen, STARTF_USESHOWWINDOW
from sublime import Region

##
# JS Linter
# Lints automatically on file save
# Additionally an on demand file lint is available via the command:
#   <binding key="ctrl+shift+l" command="jsLint"/>
#
# @author Jordi Boggiano <j.boggiano@seld.be>
##

class jsLint(sublimeplugin.TextCommand):
    def __init__(self):
        self.metadata = dict()

    def run(self, view, args):
        self.lintFile(view, True)

    def isEnabled(self, view, args):
        return view.fileName()[-3:] == '.js'

    def onPostSave(self, view):
        view.eraseRegions('jsLint')
        if view.fileName()[-3:] == '.js':
            self.lintFile(view, False)

    def onSelectionModified(self, view):
        regions = view.getRegions('jsLint')
        if not regions or not view.fileName() in self.metadata: return
        sel = view.sel()
        if len(sel) > 1: return
        for i in range(len(regions)):
            if regions[i].intersects(sel[0]):
                self.updateStatus('<!> '+self.metadata[view.fileName()][i])

    def onClose(self, view):
        self.clearMetadata(view)

    def clearMetadata(self, view):
        file = view.fileName()
        if file in self.metadata:
            del self.metadata[file]

    def lintFile(self, view, openFull):
        basePath = sublime.packagesPath()+"\\Seld\\"
        startupinfo = STARTUPINFO()
        startupinfo.dwFlags |= STARTF_USESHOWWINDOW
        content = view.substr(Region(0, view.size()))
        process = Popen('cscript "'+basePath+'jslint.js"', stdin=PIPE, stdout=PIPE, stderr=PIPE, startupinfo=startupinfo)
        (stdout, stderr) = process.communicate(content)

        output = b''
        for line in stderr.splitlines():
            print line
            if line[0:7] == 'Lint at':
                if output.strip():
                    output += b"\n"
                try:
                    output += line.decode('utf-8').strip() + " >>"
                except UnicodeDecodeError:
                    print "File encoding error detected"
            elif output.strip() and line.strip():
                output += " "+line.decode('utf-8').strip()

        if not output.strip():
            if openFull:
                view.eraseRegions('jsLint')
                self.updateStatus('No syntax error detected')
            return

        if openFull:
            lines = output.splitlines()
            jsLint.highlightTexts(self, view, lines)
            view.window().showQuickPanel("", "jsLintGoto", lines, sublime.QUICK_PANEL_MONOSPACE_FONT)
        else:
            sublime.setTimeout(functools.partial(self.updateStatus, '<!> '+output.splitlines()[0]), 100)

    def updateStatus(self, text):
        sublime.statusMessage(text);

    def highlightTexts(self, view, texts):
        highlightedAreas = []
        self.clearMetadata(view)
        self.metadata[view.fileName()] = texts

        for text in texts:
            match = re.search('(\d+).+?(\d+)', text)
            if match is None or len(match.groups()) < 2: continue
            point = view.textPoint(int(match.group(1))-1, int(match.group(2))-1)
            highlightedAreas.append(Region(point-1, point+1))

        view.addRegions('jsLint', highlightedAreas, "identifier", sublime.DRAW_OUTLINED)

class jsLintGoto(sublimeplugin.TextCommand):
    def run(self, view, args):
        match = re.search('(\d+).+?(\d+)', args[0])
        if match is None or len(match.groups()) < 2: return
        sel = view.sel()
        point = view.textPoint(int(match.group(1))-1, int(match.group(2))-1)
        region = Region(point, point)

        view.show(point)
        sel.clear()
        sel.add(region)

        jsLint().updateStatus('<!> '+args[0])
