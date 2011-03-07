import sublime, sublimeplugin

##
# Strips the trailing whitespace of every line and then saves the file
# 
# Use this as a replacement for the save command
#
# Bind it via (example):
#  <binding key="ctrl+shift+s" command="stripAndSave"/>
##

class StripAndSaveCommand(sublimeplugin.WindowCommand):
   def run(self, window, args):
      window.activeView().runCommand('sequence', ['removeWhitespace trailing', 'removeWhitespace extra'])
      window.runCommand('save')
