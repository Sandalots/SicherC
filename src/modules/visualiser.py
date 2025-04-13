# Visualiser Module for Sicher
# Sandy MacDonald
# 2003619
# 2025

# Visualiser Module Dependencies
import os  # for handling the path of given C source files
import wx  # the actual GUI library, I am using wxPython for the GUI
import time  # for measuring the time to compile
import psutil  # for measuring memory and CPU usage of Sicher
import sys  # for getting the Python version
import matplotlib.pyplot as plt  # For sicher visualisations

# Sicher Module Dependencies
from modules.tokeniser import tokenise  # for tokenising the given C source code
from modules.parser import parse_tokens  # for parsing the tokenised C source code
from modules.analyser import create_ast_from_tokens  # for modelling the given C source code as an Sicher AST
from modules.codegenerator import CodeGenerator  # for generating actual assembly code from the AST


# Models the Compiler Frame to the GUI
class CompilerFrame(wx.Frame):
    ## Constructs the Compiler Frame
    def __init__(self, *args, **kw):
        super(CompilerFrame, self).__init__(*args, **kw, size=(800, 600 * 2))  # Declares the size of the window
        self.InitUI()  # Populates the GUI with the initial elements

    # Generate Visualisations button logic
    def OnGenerateVisualisations(self, event):
        """
        Handles the Generate Visualisations button click.
        Compiles the current file 10 times and generates plots for time to compile,
        memory usage, and CPU usage.
        """
        filepath = self.file_picker.GetPath()

        if not filepath:
            wx.MessageBox('Please select a file to compile', 'Error', wx.OK | wx.ICON_ERROR)
            return

        if not os.path.isfile(filepath):
            wx.MessageBox('File does not exist', 'Error', wx.OK | wx.ICON_ERROR)
            return

        try:
            with open(filepath, 'r') as file:
                code = file.read()

            # Initialize lists to store metrics
            compile_times = []
            memory_usages = []
            cpu_usages = []

            # Compile the file 10 times and record metrics
            for i in range(10):
                start_time = time.time()
                process = psutil.Process()
                initial_memory = process.memory_info().rss  # Memory usage in bytes
                initial_cpu_times = process.cpu_times()  # Start measuring CPU times

                # Tokenization
                tokens, _ = tokenise(code, debug=False)

                # Parsing
                parse_tokens(tokens, debug=False)

                # Analyzing
                ast = create_ast_from_tokens(tokens, debug=False)

                # Code Generation
                codegen = CodeGenerator(ast)
                codegen.generate_code()

                # End time and CPU usage
                end_time = time.time()
                final_memory = process.memory_info().rss  # Memory usage in bytes
                final_cpu_times = process.cpu_times()  # End measuring CPU times

                # Calculate metrics
                time_complexity = end_time - start_time
                memory_usage = (final_memory - initial_memory) / (1024 * 1024)  # Convert to MB
                cpu_time_used = (
                    (final_cpu_times.user - initial_cpu_times.user) +
                    (final_cpu_times.system - initial_cpu_times.system)
                )
                cpu_usage_percentage = (cpu_time_used / time_complexity) * 100 if time_complexity > 0 else 0

                # Store metrics
                compile_times.append(time_complexity)
                memory_usages.append(memory_usage)
                cpu_usages.append(cpu_usage_percentage)

            # Generate plots
            self.generate_plots(compile_times, memory_usages, cpu_usages)

        except Exception as e:
            wx.MessageBox(f"Error during compilation: {e}", 'Error', wx.OK | wx.ICON_ERROR)
            
    def generate_plots(self, compile_times, memory_usages, cpu_usages):
        """
        Generates and displays plots for time to compile, memory usage, and CPU usage.
        """
        # Create a figure with 3 subplots
        fig, axs = plt.subplots(3, 1, figsize=(8, 12))

        # Plot time to compile
        axs[0].plot(range(1, 11), compile_times, marker='o', color='blue')
        axs[0].set_title('Time to Compile (seconds)')
        axs[0].set_xlabel('Iteration')
        axs[0].set_ylabel('Time (s)')

        # Plot memory usage
        axs[1].plot(range(1, 11), memory_usages, marker='o', color='green')
        axs[1].set_title('Memory Usage (MB)')
        axs[1].set_xlabel('Iteration')
        axs[1].set_ylabel('Memory (MB)')

        # Plot CPU usage
        axs[2].plot(range(1, 11), cpu_usages, marker='o', color='red')
        axs[2].set_title('CPU Usage (%)')
        axs[2].set_xlabel('Iteration')
        axs[2].set_ylabel('CPU Usage (%)')

        # Adjust layout and show the plots
        plt.tight_layout()
        plt.show()

    # Show Diagnostics button logic
    def OnShowDiagnostics(self, event):
        """
        Handles the Show Diagnostics button click.
        Displays system and compilation diagnostics.
        """
        # Clear the output panel
        self.output_panel.DestroyChildren()

        # Gather system information
        os_info = os.uname() if hasattr(os, "uname") else "Unknown OS"
        cpu_info = os.cpu_count()
        process = psutil.Process()

        # Gather diagnostic data
        diagnostics = {
            "Operating System": os_info.sysname if hasattr(os_info, "sysname") else os_info,
            "OS Version": os_info.release if hasattr(os_info, "release") else "Unknown",
            "CPU Cores": cpu_info,
            "CPU Frequency": f"{psutil.cpu_freq().current} MHz" if psutil.cpu_freq() else "Unknown",
            "Memory Usage": f"{process.memory_info().rss / (1024 * 1024):.2f} MB",
            "CPU Usage": f"{process.cpu_percent(interval=1)}%",
            "Python Version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
            "Sicher Version": "1.0.0", 
            "Sicher Path": os.path.abspath(__file__),
            "Number of Threads": process.num_threads(),
            "Process Name": process.name(),
            "Process Status": process.status(),
            "Process Creation Time": time.ctime(process.create_time()),
            "Process Memory Usage": f"{process.memory_info().rss / (1024 * 1024):.2f} MB",
            "Process CPU Time": f"{process.cpu_times().user + process.cpu_times().system:.2f} seconds",
            "Process Command Line": " ".join(process.cmdline()),
            "Process Working Directory": process.cwd(),
            "Process Environment Variables": dict(process.environ()),
            "Process ID": process.pid,
            "Executable Path": process.exe(),
        }

        # Format diagnostics as a string
        diagnostics_text = "\n".join(f"{key}: {value}" for key, value in diagnostics.items())

        # Add diagnostics to the output panel
        self.add_collapsible_section("Diagnostics", diagnostics_text)

    # Initialise the GUI elements
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

        # Buttons (Compile, Generate Visualisations, Show Diagnostics)
        hbox_buttons = wx.BoxSizer(wx.HORIZONTAL)

        hbox_buttons.AddStretchSpacer(1)  # Add a stretchable space before the buttons

        # Compile button
        self.compile_button = wx.Button(panel, label='Compile')
        self.compile_button.SetBackgroundColour("#FAD000")
        self.compile_button.SetForegroundColour("#2D2B55")
        font = self.compile_button.GetFont()
        font = font.Bold()
        self.compile_button.SetFont(font)
        self.compile_button.Bind(wx.EVT_BUTTON, self.OnCompile)
        hbox_buttons.Add(self.compile_button, flag=wx.RIGHT, border=10)

        # Add a spacer between Compile and Generate Visualisations buttons
        hbox_buttons.AddSpacer(20)  # Add 20 pixels of horizontal space

        # Generate Visualisations button
        self.visualise_button = wx.Button(panel, label='Generate Visualisations')
        self.visualise_button.SetBackgroundColour("#FAD000")
        self.visualise_button.SetForegroundColour("#2D2B55")
        font = self.visualise_button.GetFont()
        font = font.Bold()
        self.visualise_button.SetFont(font)
        self.visualise_button.Bind(wx.EVT_BUTTON, self.OnGenerateVisualisations)
        hbox_buttons.Add(self.visualise_button, flag=wx.RIGHT, border=10)

        # Add a spacer between Generate Visualisations and Show Diagnostics buttons
        hbox_buttons.AddSpacer(10)  # Add 10 pixels of horizontal space

        # Show Diagnostics button
        self.diagnostics_button = wx.Button(panel, label='Show Diagnostics')
        self.diagnostics_button.SetBackgroundColour("#FAD000")
        self.diagnostics_button.SetForegroundColour("#2D2B55")
        font = self.diagnostics_button.GetFont()
        font = font.Bold()
        self.diagnostics_button.SetFont(font)
        self.diagnostics_button.Bind(wx.EVT_BUTTON, self.OnShowDiagnostics)
        hbox_buttons.Add(self.diagnostics_button, flag=wx.LEFT, border=10)

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

        # Gives the GUI window the Sicher C Compiler title
        self.SetTitle('Sicher C Compiler')

        # Centers the GUI window on the screen
        self.Centre()

    # Compile button logic
    def OnCompile(self, event):
        filepath = self.file_picker.GetPath()

        if not filepath:
            wx.MessageBox('Please select a file to compile', 'Error', wx.OK | wx.ICON_ERROR)
            return

        # Check if the file exists
        if not os.path.isfile(filepath):
            wx.MessageBox('File does not exist', 'Error', wx.OK | wx.ICON_ERROR)
            return
        # Check if the file is a C source file
        if not filepath.endswith('.c'):
            wx.MessageBox('File is not a C source file', 'Error', wx.OK | wx.ICON_ERROR)
            return
        # Check if the file is empty
        if os.path.getsize(filepath) == 0:
            wx.MessageBox('File is empty', 'Error', wx.OK | wx.ICON_ERROR)
            return
        # Check if the file is readable
        try:
            with open(filepath, 'r') as file:
                pass
        except IOError:
            wx.MessageBox('Error reading file', 'Error', wx.OK | wx.ICON_ERROR)
            return

        # Clear the output panel
        self.output_panel.DestroyChildren()

        try:
            with open(filepath, 'r') as file:
                code = file.read()

            # Measure start time and CPU usage
            start_time = time.time()
            process = psutil.Process()
            initial_memory = process.memory_info().rss  # Memory usage in bytes
            initial_cpu_times = process.cpu_times()  # Start measuring CPU times

            # Tokenization
            tokens, tokeniser_log = tokenise(code, debug=True)
            self.add_collapsible_section("Tokenisation Module", tokeniser_log)  # Display the debug output

            # Parsing
            parsing_debug_output = parse_tokens(tokens, debug=True)
            self.add_collapsible_section("Parser Module", parsing_debug_output)

            # Analyzing
            ast = create_ast_from_tokens(tokens, debug=True)
            self.add_collapsible_section("Analyser Module (Abstract Syntax Tree)", ast.pretty_print())

            # Code Generation
            codegen = CodeGenerator(ast)
            generated_code = codegen.generate_code()
            self.add_collapsible_section("Code Generator Module", generated_code)

            # End time and CPU usage
            end_time = time.time()
            final_memory = process.memory_info().rss  # Memory usage in bytes
            final_cpu_times = process.cpu_times()  # End measuring CPU times

            # Calculate time complexity
            time_complexity = end_time - start_time

            # Calculate memory usage (RAM usage)
            memory_usage = (final_memory - initial_memory) / (1024 * 1024)  # Convert to MB

            # Calculate CPU usage
            cpu_time_used = (
                (final_cpu_times.user - initial_cpu_times.user) +
                (final_cpu_times.system - initial_cpu_times.system)
            )
            cpu_usage_percentage = (cpu_time_used / time_complexity) * 100 if time_complexity > 0 else 0

            # Update the combined complexity label
            self.complexity_label.SetLabel(
                f"Time to Compile: {time_complexity:.4f} seconds | "
                f"Memory Usage: {memory_usage:.2f} MB | "
                f"CPU Usage: {cpu_usage_percentage:.2f}%"
            )

            # Top Level Viz
            self.add_top_level_viz(ast)

        except Exception as e:
            wx.MessageBox(f"Error: {e}", 'Error', wx.OK | wx.ICON_ERROR)

    # Defines a method to add collapsable sections housing each of the Sicher Modules work plus the additional top level viz
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
            label="Top Level Visualisation",
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


# Main loop to run the GUI
def main():
    # create the wx GUI application
    app = wx.App()

    # set the name of the application to the Sicher C Compiler
    app.SetAppName("Sicher C Compiler")

    # Create the frame
    frame = CompilerFrame(None)

    # Show the frame
    frame.Show()

    # Bring the Sicher window to the front
    wx.CallAfter(frame.Raise)

    # Keep the GUI running
    app.MainLoop()


# Run the main function
if __name__ == '__main__':
    main()