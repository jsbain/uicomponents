import ui
from uicontainer import FlowContainer
from PopupButton import PopupButton

class KeyboardExtension(ui.View):
    def __init__(self):
        pass
root=ui.View()
root.flex='WH'
root.present('fullscreen')
class key(object):
    def __init__(self, k='',subkeys=[]):
        self.key=k
        self.subkeys=[key(s) for s in subkeys]
        

keymap=[key('\t'),key('_'),key('#',['@']),key('<',['<=']),key('>',['>=']),
        key('{'),key('}'),key('['),key(']'),key("'",['"']),key('('),key(')'),
        key(':',[';'])]+[key(str(n)) for n in range(1,9)]+[key('0'),key('+',['%']),key('-'),key('/',['\n','\t','\\','/']),key('*'),key('=',['!='])]
                                


def makeButton(k):
    def buttaction(sender):
        print k.key
    childButtons=[makeButton(subkey)  for subkey in k.subkeys]
    return PopupButton(title=k.key,childButtons=childButtons,action=buttaction)

keyboard=FlowContainer(frame=(0,root.height-100,root.width,250),flex='THW')
root.add_subview(keyboard)
keyboard.hidden=True

for key in keymap:
    keyboard.add_subview(makeButton(key))
keyboard.hidden=False
#keyboard.layout()

