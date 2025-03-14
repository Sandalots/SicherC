import wx

from modules.tokeniser import tokenise
from modules.parser import parse_tokens
from modules.analyser import create_ast_from_tokens

class CompilerFrame(wx.Frame):
    def __init__(self, *args, **kw):
        super(CompilerFrame, self).__init__(*args, **kw, size=(800, 600 * 2))
        self.InitUI()

    def InitUI(self):
        panel = wx.Panel(self)
        panel.SetBackgroundColour("#2D2B55")

        vbox = wx.BoxSizer(wx.VERTICAL)

        # File upload
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        self.file_picker = wx.FilePickerCtrl(panel)
        hbox1.Add(self.file_picker, proportion=1, flag=wx.EXPAND)
        vbox.Add(hbox1, flag=wx.EXPAND | wx.ALL, border=10)

        # Compile button
        self.compile_button = wx.Button(panel, label='Compile')
        self.compile_button.SetBackgroundColour("#FAD000")
        self.compile_button.SetForegroundColour("#2D2B55")
        self.compile_button.Bind(wx.EVT_BUTTON, self.OnCompile)
        vbox.Add(self.compile_button, flag=wx.ALIGN_CENTER | wx.BOTTOM, border=20)

        # Output tab
        self.notebook = wx.Notebook(panel)
        self.output_tab = wx.TextCtrl(self.notebook, style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.output_tab.SetBackgroundColour("#1E1E3F")
        self.output_tab.SetForegroundColour("#FAD000")
        self.countermeasures_tab = wx.TextCtrl(self.notebook, style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.countermeasures_tab.SetBackgroundColour("#1E1E3F")
        self.countermeasures_tab.SetForegroundColour("#FAD000")
        self.notebook.AddPage(self.output_tab, 'Output')
        self.notebook.AddPage(self.countermeasures_tab, 'Countermeasures')
        vbox.Add(self.notebook, proportion=1, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)

        # Make binary button
        self.make_binary_button = wx.Button(panel, label='Make Binary')
        self.make_binary_button.SetBackgroundColour("#FAD000")
        self.make_binary_button.SetForegroundColour("#2D2B55")
        self.make_binary_button.Bind(wx.EVT_BUTTON, self.OnMakeBinary)
        vbox.Add(self.make_binary_button, flag=wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, border=10)

        panel.SetSizer(vbox)

        self.SetTitle('Sicher C Compiler')
        self.Centre()

    def OnCompile(self, event):
        filepath = self.file_picker.GetPath()
        if not filepath:
            wx.MessageBox('Please select a file to compile', 'Error', wx.OK | wx.ICON_ERROR)
            return

        # Clear the output box
        self.output_tab.Clear()

        try:
            with open(filepath, 'r') as file:
                code = file.read()

            # Tokenization
            tokens = tokenise(code, debug=True)
            self.output_tab.AppendText("Tokenization:\n")
            self.output_tab.AppendText(str(tokens) + "\n\n")

            # Parsing
            parse_tokens(tokens, debug=True)
            self.output_tab.AppendText("Parsing:\n")
            self.output_tab.AppendText("Source code is syntactically correct\n\n")

            # Analyzing
            ast = create_ast_from_tokens(tokens, debug=True)
            self.output_tab.AppendText("Analyzing:\n")
            self.output_tab.AppendText(ast.pretty_print() + "\n")

        except Exception as e:
            wx.MessageBox(f"Error: {e}", 'Error', wx.OK | wx.ICON_ERROR)

    def OnMakeBinary(self, event):
        wx.MessageBox('Make Binary functionality is not implemented yet', 'Info', wx.OK | wx.ICON_INFORMATION)

def main():
    app = wx.App()
    app.SetAppName("Sicher")

    frame = CompilerFrame(None)
    frame.Show()

    # Bring the window to the front
    wx.CallAfter(frame.Raise)

    app.MainLoop()

if __name__ == '__main__':
    main()