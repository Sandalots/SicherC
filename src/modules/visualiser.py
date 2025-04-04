# Visualiser Module for Sicher
# Sandy MacDonald
# 2003619
# 2025

# Visualiser Module Dependencies
import os
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
        
        # Sicher Title
        title = wx.StaticText(panel, label='Sicher C Compiler')
        title.SetForegroundColour("#FAD000")
        font = title.GetFont()
        font.PointSize += 10
        font = font.Bold()
        title.SetFont(font)
        vbox.Add(title, flag=wx.ALIGN_CENTER | wx.TOP, border=10)

        # File upload 
        file_label = wx.StaticText(panel, label='Select a C Source File:')
        file_label.SetForegroundColour("#FAD000")
        font = file_label.GetFont()
        font.PointSize += 5
        font = font.Bold()
        file_label.SetFont(font)
        vbox.Add(file_label, flag=wx.ALIGN_LEFT | wx.TOP | wx.LEFT, border=10)
        file_label.SetBackgroundColour("#2D2B55")
        
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        
        # Set default path for the file picker using a relative path
        base_dir = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the current script
        default_path = os.path.join(base_dir, "../../examples/hello_world.c")  # Construct the relative path
        self.file_picker = wx.FilePickerCtrl(panel, path=default_path)
        hbox1.Add(self.file_picker, proportion=1, flag=wx.EXPAND)
        vbox.Add(hbox1, flag=wx.EXPAND | wx.ALL, border=10)

        # Compile button
        self.compile_button = wx.Button(panel, label='Compile')
        self.compile_button.SetBackgroundColour("#FAD000")
        self.compile_button.SetForegroundColour("#2D2B55")
        font = self.compile_button.GetFont()
        font = font.Bold()
        self.compile_button.SetFont(font)
        self.compile_button.Bind(wx.EVT_BUTTON, self.OnCompile)
        vbox.Add(self.compile_button, flag=wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, border=20)

        # Output panel for collapsible sections
        self.output_panel = wx.Panel(panel)
        self.output_panel.SetBackgroundColour("#1E1E3F")
        self.output_sizer = wx.BoxSizer(wx.VERTICAL)
        self.output_panel.SetSizer(self.output_sizer)
        vbox.Add(self.output_panel, proportion=1, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)

        panel.SetSizer(vbox)

        self.SetTitle('Sicher C Compiler')
        self.Centre()

    def OnCompile(self, event):
        filepath = self.file_picker.GetPath()
        if not filepath:
            wx.MessageBox('Please select a file to compile', 'Error', wx.OK | wx.ICON_ERROR)
            return

        # Clear the output panel
        self.output_panel.DestroyChildren()

        try:
            with open(filepath, 'r') as file:
                code = file.read()

            # Tokenization
            tokens = tokenise(code, debug=True)
            self.add_collapsible_section("Tokenization", str(tokens))
            
            # Parsing
            parsing_debug_output = parse_tokens(tokens, debug=True)
            self.add_collapsible_section("Parsing", parsing_debug_output)
            # Analyzing
            ast = create_ast_from_tokens(tokens, debug=True)
            self.add_collapsible_section("Analyzing", ast.pretty_print())
            
            # Code Generation
            
            # Top Level Viz

        except Exception as e:
            wx.MessageBox(f"Error: {e}", 'Error', wx.OK | wx.ICON_ERROR)

    def add_collapsible_section(self, title, content):
         # Create a collapsible pane
        collapsible_pane = wx.CollapsiblePane(
            self.output_panel,
            label=title,
            style=wx.CP_DEFAULT_STYLE | wx.CP_NO_TLW_RESIZE
        )
        collapsible_pane.Bind(wx.EVT_COLLAPSIBLEPANE_CHANGED, self.on_collapsible_pane_changed)

        # Set the arrow color to yellow (same as buttons)
        collapsible_pane.SetForegroundColour("#FAD000")
        collapsible_pane.SetBackgroundColour("#1E1E3F")

        # Make the collapsible pane visible by default
        collapsible_pane.Collapse(False)

        # Add content to the collapsible pane
        pane = collapsible_pane.GetPane()
        text_ctrl = wx.TextCtrl(
            pane,
            value=content,
            style=wx.TE_MULTILINE | wx.TE_READONLY | wx.BORDER_NONE
        )
        text_ctrl.SetBackgroundColour("#1E1E3F")
        text_ctrl.SetForegroundColour("#FAD000")

        # Adjust the height of the collapsible boxes
        text_ctrl.SetMinSize((-1, 150))  # Set a minimum height of 150 pixels

        # Layout for the collapsible pane
        pane_sizer = wx.BoxSizer(wx.VERTICAL)
        pane_sizer.Add(text_ctrl, proportion=1, flag=wx.EXPAND)
        pane.SetSizer(pane_sizer)

        # Add the collapsible pane to the output panel
        self.output_sizer.Add(collapsible_pane, flag=wx.EXPAND | wx.ALL, border=5)
        self.output_panel.Layout()

    def on_collapsible_pane_changed(self, event):
        self.output_panel.Layout()

def main():
    app = wx.App()
    app.SetAppName("Sicher")

    # Create the frame
    frame = CompilerFrame(None)
    # Show the frame
    frame.Show()

    # Bring the Sicher window to the front
    wx.CallAfter(frame.Raise)

    app.MainLoop()

# Run the main function
if __name__ == '__main__':
    main()