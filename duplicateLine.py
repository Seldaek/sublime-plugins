import sublime, sublimeplugin

##
# Duplicates current line if there's nothing selected. Else duplicates content
# Bind it via (examples):
#  <binding key="ctrl+shift+d" command="duplicateLine"/>
#  <binding key="ctrl+shift+alt+down" command="duplicateLine"/>
##

class DuplicateLineCommand(sublimeplugin.TextCommand):
  def run(self, view, args):
    for region in view.sel():
      if region.empty():
        line = view.line(region)
        lineContents = view.substr(line) + '\n'
        view.insert(line.begin(), lineContents)
      else:
        s = view.substr(region)
        view.insert(region.end(), s)
