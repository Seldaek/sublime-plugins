import sublime, sublimeplugin

##
# Duplicates current line if there's nothing selected. Else duplicates content
# Bind it via (example):
#  <binding key="ctrl+shift+s" command="stripAndSave"/>
##

class StripAndSaveCommand(sublimeplugin.WindowCommand):
   def run(self, window, args):
      window.activeView().runCommand('sequence', ['removeWhitespace trailing', 'removeWhitespace extra'])
      window.runCommand('save')