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
from modules.codegenerator import CodeGenerator
import time
import psutil


class CompilerFrame(wx.Frame):
    def __init__(self, *args, **kw):
        super(CompilerFrame, self).__init__(*args, **kw, size=(800, 600 * 2))
        self.InitUI()

    def OnGenerateVisualisations(self, event):
        """
        Handles the Generate Visualisations button click.
        Currently, it clears the collapsible sections below the button.
        """
        self.output_panel.DestroyChildren()
        self.output_panel.Layout()

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

        # Buttons (Compile and Generate Visualisations)
        hbox_buttons = wx.BoxSizer(wx.HORIZONTAL)

        # Compile button
        self.compile_button = wx.Button(panel, label='Compile')
        self.compile_button.SetBackgroundColour("#FAD000")
        self.compile_button.SetForegroundColour("#2D2B55")
        font = self.compile_button.GetFont()
        font = font.Bold()
        self.compile_button.SetFont(font)
        self.compile_button.Bind(wx.EVT_BUTTON, self.OnCompile)
        hbox_buttons.Add(self.compile_button, flag=wx.RIGHT, border=10)

        # Generate Visualisations button
        self.visualise_button = wx.Button(panel, label='Generate Visualisations')
        self.visualise_button.SetBackgroundColour("#FAD000")
        self.visualise_button.SetForegroundColour("#2D2B55")
        font = self.visualise_button.GetFont()
        font = font.Bold()
        self.visualise_button.SetFont(font)
        self.visualise_button.Bind(wx.EVT_BUTTON, self.OnGenerateVisualisations)
        hbox_buttons.Add(self.visualise_button, flag=wx.LEFT, border=10)

        vbox.Add(hbox_buttons, flag=wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, border=20)

        # Time/Space Complexity Labels
        hbox_complexity = wx.BoxSizer(wx.HORIZONTAL)  # Horizontal box sizer for centering
        self.complexity_label = wx.StaticText(panel, label="")
        self.complexity_label.SetForegroundColour("#FAD000")
        font = self.complexity_label.GetFont()
        font.PointSize += 2
        self.complexity_label.SetFont(font)

        # Add the label to the horizontal sizer and center it
        hbox_complexity.Add(self.complexity_label, flag=wx.ALIGN_CENTER)

        # Add the horizontal sizer to the main vertical sizer
        vbox.Add(hbox_complexity, flag=wx.ALIGN_CENTER | wx.TOP, border=5)

        # Output Header
        output_label = wx.StaticText(panel, label='Sicher Output:')
        output_label.SetForegroundColour("#FAD000")
        font = output_label.GetFont()
        font.PointSize += 5
        font = font.Bold()
        output_label.SetFont(font)
        vbox.Add(output_label, flag=wx.ALIGN_LEFT | wx.TOP | wx.LEFT, border=10)
        output_label.SetBackgroundColour("#2D2B55")
        vbox.AddSpacer(10)  # Add some space between the label and the output panel

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

            # Measure start time
            start_time = time.time()
            process = psutil.Process()
            initial_memory = process.memory_info().rss  # Memory usage in bytes

            # Tokenization
            tokens, tokeniser_log = tokenise(code, debug=True)
            self.add_collapsible_section("Tokenisation", tokeniser_log)  # Display the debug output

            # Parsing
            parsing_debug_output = parse_tokens(tokens, debug=True)
            self.add_collapsible_section("Parsing", parsing_debug_output)

            # Analyzing
            ast = create_ast_from_tokens(tokens, debug=True)
            self.add_collapsible_section("Analyzing", ast.pretty_print())

            # Code Generation
            codegen = CodeGenerator(ast)
            generated_code = codegen.generate_code()
            self.add_collapsible_section("Code Generation", generated_code)

            # End time
            end_time = time.time()
            final_memory = process.memory_info().rss  # Memory usage in bytes

            # Calculate time complexity
            time_complexity = end_time - start_time

            # Calculate memory usage (RAM usage)
            memory_usage = (final_memory - initial_memory) / (1024 * 1024)  # Convert to MB

            # Update the combined complexity label
            self.complexity_label.SetLabel(
                f"Time to Compile: {time_complexity:.4f} seconds | Memory Usage: {memory_usage:.2f} MB"
            )

            # Top Level Viz
            self.add_top_level_viz(ast)

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

    def add_top_level_viz(self, ast):
        """
        Adds a top-level visualization of the AST to the output panel.

        Args:
            ast: The root of the AST.
        """
        collapsible_pane = wx.CollapsiblePane(
            self.output_panel,
            label="Top Level Viz",
            style=wx.CP_DEFAULT_STYLE | wx.CP_NO_TLW_RESIZE
        )
        collapsible_pane.Bind(wx.EVT_COLLAPSIBLEPANE_CHANGED, self.on_collapsible_pane_changed)

        # Make the collapsible pane visible by default
        collapsible_pane.Collapse(False)

        # Create the visualization panel
        viz_panel = ASTVisualizerPanel(collapsible_pane.GetPane(), ast)
        viz_panel.SetMinSize((800, 600))  # Set a minimum size for the visualization

        # Add the visualization panel to the collapsible pane
        pane_sizer = wx.BoxSizer(wx.VERTICAL)
        pane_sizer.Add(viz_panel, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)
        collapsible_pane.GetPane().SetSizer(pane_sizer)

        # Add the collapsible pane to the output panel
        self.output_sizer.Add(collapsible_pane, flag=wx.EXPAND | wx.ALL, border=5)
        self.output_panel.Layout()


class ASTVisualizerPanel(wx.ScrolledWindow):
    def __init__(self, parent, ast):
        super(ASTVisualizerPanel, self).__init__(parent)
        self.ast = ast
        self.SetBackgroundColour("#1E1E3F")

        # Enable scrolling
        self.SetScrollbars(20, 20, 50, 50)  # Scroll step size and virtual size
        self.virtual_size = (2000, 2000)  # Set a large virtual size for the canvas
        self.SetVirtualSize(self.virtual_size)

        # Variables for panning
        self.is_panning = False
        self.last_mouse_position = None

        # Bind events
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self.Bind(wx.EVT_MOTION, self.OnMouseMove)

    def OnPaint(self, event):
        dc = wx.PaintDC(self)
        self.PrepareDC(dc)  # Adjust for scrolling
        gc = wx.GraphicsContext.Create(dc)

        if gc:
            gc.SetBrush(wx.Brush("#FAD000"))  # Yellow theme color
            gc.SetPen(wx.Pen("#FAD000", 2))  # Yellow border

            # Start drawing the AST
            self.draw_node(gc, self.ast.root, 1000, 50, 200, 100)  # Centered in the virtual space

    def draw_node(self, gc, node, x, y, x_offset, y_offset):
        if not node:
            return

        # Draw the current node as a rectangle
        rect_width, rect_height = 120, 50
        gc.DrawRectangle(x - rect_width // 2, y, rect_width, rect_height)

        # Draw the node label
        gc.SetFont(wx.Font(10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD), "#2D2B55")
        label = f"{node.node_type}\n{node.value}" if node.value else node.node_type
        gc.DrawText(label, x - rect_width // 2 + 10, y + 10)

        # Calculate positions for child nodes
        num_children = len(node.children)
        if num_children > 0:
            child_y = y + y_offset + 20  # Add extra vertical padding
            child_x_start = x - (x_offset * (num_children - 1)) // 2

            for i, child in enumerate(node.children):
                child_x = child_x_start + i * x_offset

                # Draw an arrow to the child node
                gc.SetPen(wx.Pen("#FAD000", 2))
                gc.StrokeLine(x, y + rect_height, child_x, child_y)

                # Recursively draw the child node
                self.draw_node(gc, child, child_x, child_y, x_offset, y_offset)

    def OnLeftDown(self, event):
        # Start panning
        self.is_panning = True
        self.last_mouse_position = event.GetPosition()
        self.CaptureMouse()

    def OnLeftUp(self, event):
        # Stop panning
        if self.is_panning:
            self.is_panning = False
            self.ReleaseMouse()

    def OnMouseMove(self, event):
        if self.is_panning and event.Dragging() and event.LeftIsDown():
            current_position = event.GetPosition()
            dx = self.last_mouse_position.x - current_position.x
            dy = self.last_mouse_position.y - current_position.y

            # Scroll the window
            self.Scroll(self.GetScrollPos(wx.HORIZONTAL) + dx // 20,
                        self.GetScrollPos(wx.VERTICAL) + dy // 20)

            self.last_mouse_position = current_position


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