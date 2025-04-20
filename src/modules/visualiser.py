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
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas  # for embedding the plots in the wx gui
import subprocess  # for running the compiled binary

# Sicher Module Dependencies (the 4 modules bar this current visualiser module)
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
        
        #Bind the event menu to quit the gui when pressed
        self.Bind(wx.EVT_MENU, self.OnExit)

        # macro for command q to be set as the exit key for macOS
        accel_tbl = wx.AcceleratorTable([
            (wx.ACCEL_CMD, ord('Q'), wx.ID_EXIT) # bind command q to the exit key
        ])
        
        # use the command q macro
        self.SetAcceleratorTable(accel_tbl)

    # function to exit the Sicher Visualiser GUI
    def OnExit(self, event):
        """
        Handles the Cmd+Q shortcut to exit the application.
        """
        self.Destroy()  # destroy the GUI window

    # Generate Visualisations button logic, getting the performance metrics of Sicher and plotting them
    def OnGenerateVisualisations(self, event):
        """
        Handles the Generate Visualisations button click.
        Compiles the current file 10 times and generates plots for time to compile,
        memory usage, and CPU usage.
        """
        # gets the filepath from the file picker
        filepath = self.file_picker.GetPath()

        # check if no file was selected
        if not filepath:
            # tell the user the to select a file as the filepicker is empty
            wx.MessageBox('Please select a file to compile', 'Error', wx.OK | wx.ICON_ERROR)
            return

        # check if the file exists
        if not os.path.isfile(filepath):
            # tell the user the file does not exist
            wx.MessageBox('File does not exist', 'Error', wx.OK | wx.ICON_ERROR)
            return
        
        # Redraw the visualisations on click of the generate visualisations button
        self.output_panel.DestroyChildren()  # Clear the output panel
        self.output_panel.Layout()  # Layout the output panel

        # try and compile the user given file
        try:
            # read the filepath
            with open(filepath, 'r') as file:
                # set the code as the file contents
                code = file.read()

            # Initialize lists to store metrics
            compile_times = [] # store the time to compile sicher
            memory_usages = [] # store the memory usage of sicher
            cpu_usages = [] # store the cpu usage of sicher

            # Compile the file 10 times and record metrics
            for i in range(10):
                start_time = time.time() # start the compile timer
                process = psutil.Process() # get the current process (sicher)
                initial_memory = process.memory_info().rss  # Memory usage in bytes
                initial_cpu_times = process.cpu_times()  # Start measuring CPU times

                # Tokenisation Module
                tokens, _ = tokenise(code, debug=False) # creates the tokens

                # Parser Module
                parse_tokens(tokens, debug=False) # parses the tokens

                # Analyser Module
                ast = create_ast_from_tokens(tokens, debug=False) # creates an AST from the syntax correct tokens

                # Code Generator Module
                codegen = CodeGenerator(ast) # generates assembly and creates a binary from the AST, creates the codegenerator object
                codegen.generate_code() # generate the code from the avove object

                # end the compile timer and record the memory and cpu usage
                end_time = time.time() # stop the compile timer
                final_memory = process.memory_info().rss  # Memory usage in bytes
                final_cpu_times = process.cpu_times()  # End measuring CPU times

                # Calculate metrics
                time_complexity = (end_time - start_time) * 1000  # get the time to compile
                memory_usage = ((final_memory - initial_memory) / (1024 * 1024)) *100  # Convert to MB
                
                # Calculate CPU usage
                cpu_time_used = (
                    (final_cpu_times.user - initial_cpu_times.user) +
                    (final_cpu_times.system - initial_cpu_times.system)
                ) 
                
                # get the cpu time used
                cpu_usage_percentage = (cpu_time_used / time_complexity) * 10000 if time_complexity > 0 else 0 # compute the cpu usage percentage

                # Store metrics
                compile_times.append(time_complexity) # store the time to compile for sicher in the cirrent iteration
                memory_usages.append(memory_usage) # store the memory usage for sicher in the current iteration
                cpu_usages.append(cpu_usage_percentage) # store the cpu usage for sicher in the current iteration

            # Generate plots
            self.generate_plots(compile_times, memory_usages, cpu_usages) # pass the plots the compile times, memory usage and cpu usage

        # Handle exceptions for generating and visualising sicher performance plots
        except Exception as e:
            wx.MessageBox(f"Error during compilation: {e}", 'Error', wx.OK | wx.ICON_ERROR)
            
    # From the above measuements, generate the plots for the time to compile, memory usage and cpu usage of sicher
    def generate_plots(self, compile_times, memory_usages, cpu_usages):
        """
        Generates and embeds scaled-down plots for time to compile, memory usage, and CPU usage
        into a collapsible section in the GUI.
        """
        # create a figure with 3 subplots
        fig, axs = plt.subplots(3, 1, figsize=(6, 8)) 

        # Plot time to compile for sicher
        axs[0].plot(range(1, 11), compile_times, marker='o', color='blue') # plot the compile times
        axs[0].set_title('Time to Compile (seconds)', fontsize=10) # title
        axs[0].set_xlabel('Iteration', fontsize=8) # x axis label
        axs[0].set_ylabel('Time (s)', fontsize=8) # y axis label
        axs[0].tick_params(axis='both', labelsize=8) 

        # Plot memory usage for sicher
        axs[1].plot(range(1, 11), memory_usages, marker='o', color='green') # plot the memory usage
        axs[1].set_title('Memory Usage (MB)', fontsize=10) # title
        axs[1].set_xlabel('Iteration', fontsize=8) # x axis label
        axs[1].set_ylabel('Memory (MB)', fontsize=8) # y axis label
        axs[1].tick_params(axis='both', labelsize=8)

        # Plot CPU usage for sicher
        axs[2].plot(range(1, 11), cpu_usages, marker='o', color='red') # plot the cpu usage
        axs[2].set_title('CPU Usage (%)', fontsize=10) # title
        axs[2].set_xlabel('Iteration', fontsize=8) # x axis label
        axs[2].set_ylabel('CPU Usage (%)', fontsize=8) # y axis label
        axs[2].tick_params(axis='both', labelsize=8)

        # Adjust layout to reduce spacing
        fig.subplots_adjust(hspace=0.8, top=0.9)  # give some spacing to between the tops of each plots
        fig.suptitle('Sicher Compiler Performance Metrics', fontsize=12, fontweight='bold') # title for the figure

        # Embed the figure into a collapsible section
        self.add_visualisation_section(fig)
            
    # method to add the plots to a collapsable section in the visualiser GUI
    def add_visualisation_section(self, figure):
        """
        Adds a collapsible section to display the scaled-down visualisation plots.
        """
        # Create a collapsible pane for the visualisations
        collapsible_pane = wx.CollapsiblePane(
            self.output_panel,
            label="Visualisation Plots",
            style=wx.CP_DEFAULT_STYLE | wx.CP_NO_TLW_RESIZE
        )
        
        # Bind the event to handle collapsible pane changes
        collapsible_pane.Bind(wx.EVT_COLLAPSIBLEPANE_CHANGED, self.on_collapsible_pane_changed)

        # Set the arrow color to yellow (same as buttons)
        collapsible_pane.SetForegroundColour("#FAD000")
        collapsible_pane.SetBackgroundColour("#1E1E3F")

        # Make the collapsible pane visible by default
        collapsible_pane.Collapse(False)

        # Add a panel to hold the matplotlib figure
        pane = collapsible_pane.GetPane()
        plot_panel = wx.Panel(pane)
        plot_panel.SetBackgroundColour("#1E1E3F")

        # Embed the matplotlib figure into the panel
        canvas = FigureCanvas(plot_panel, -1, figure)

        # Set a fixed size for the plot panel to scale down the plots
        plot_panel.SetMinSize((600, 1000))  # Width: 600px, Height: 400px

        # Layout for the plot panel
        plot_sizer = wx.BoxSizer(wx.VERTICAL)
        plot_sizer.Add(canvas, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)
        plot_panel.SetSizer(plot_sizer)

        # Layout for the collapsible pane
        pane_sizer = wx.BoxSizer(wx.VERTICAL)
        pane_sizer.Add(plot_panel, proportion=1, flag=wx.EXPAND)
        pane.SetSizer(pane_sizer)

        # Add the collapsible pane to the output panel
        self.output_sizer.Add(collapsible_pane, flag=wx.EXPAND | wx.ALL, border=5)
        self.output_panel.Layout()
        
    # Show Diagnostics button logic
    def OnShowDiagnostics(self, event):
        """
        Handles the Show Diagnostics button click.
        Displays system and compilation diagnostics.
        """
        # Clear the output panel
        self.output_panel.DestroyChildren()

        # Gather system information
        os_info = os.uname() if hasattr(os, "uname") else "Unknown OS" # get the os information
        cpu_info = os.cpu_count() # get the cpu info 
        process = psutil.Process() # get the current process (sicher)

        # Gather diagnostic data in the below dictionary
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
        # create the main panel
        panel = wx.Panel(self)
        
        # Set the background colour of the panel to be the dark purple colour
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

        # File Upload Button
        file_label = wx.StaticText(panel, label='Select a C Source File:')
        file_label.SetForegroundColour("#FAD000")
        font = file_label.GetFont()
        font.PointSize += 5
        font = font.Bold()
        file_label.SetFont(font)
        vbox.Add(file_label, flag=wx.ALIGN_LEFT | wx.TOP | wx.LEFT, border=10)
        file_label.SetBackgroundColour("#2D2B55")

        # some horizontal spacing for the below file picker
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)

        # Set default path for the file picker using a relative path
        base_dir = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the current file
        default_path = os.path.join(base_dir, "../../examples/hello_world.c")  # Construct the relative path to the hello world.c file
        self.file_picker = wx.FilePickerCtrl(panel, path=default_path) # start the file picker with the default path, in the examples directory
        hbox1.Add(self.file_picker, proportion=1, flag=wx.EXPAND)
        vbox.Add(hbox1, flag=wx.EXPAND | wx.ALL, border=10)
        
        # Label fo the below Sicher Controls (Buttons)
        magic_buttons_label = wx.StaticText(panel, label='Sicher Controls:')
        magic_buttons_label.SetForegroundColour("#FAD000")
        font = magic_buttons_label.GetFont()
        font.PointSize += 3  # Slightly smaller than the title
        font = font.Bold()
        magic_buttons_label.SetFont(font)
        vbox.Add(magic_buttons_label, flag=wx.ALIGN_CENTER | wx.TOP, border=10)

        # Buttons (Compile, Generate Visualisations, Show Diagnostics)
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

        # Add a spacer between Compile and Generate Visualisations buttons
        hbox_buttons.AddSpacer(10)

        # Generate Visualisations button
        self.visualise_button = wx.Button(panel, label='Generate Visualisations')
        self.visualise_button.SetBackgroundColour("#FAD000")
        self.visualise_button.SetForegroundColour("#2D2B55")
        font = self.visualise_button.GetFont()
        font = font.Bold()
        self.visualise_button.SetFont(font)
        self.visualise_button.Bind(wx.EVT_BUTTON, self.OnGenerateVisualisations)
        hbox_buttons.Add(self.visualise_button, flag=wx.RIGHT, border=10)

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
        
        hbox_buttons.AddSpacer(10)  # Add 10 pixels of horizontal space between the eiqgnowtics and clear buttons

        # Clear button
        self.clear_button = wx.Button(panel, label='Clear')
        self.clear_button.SetBackgroundColour("#FAD000")
        self.clear_button.SetForegroundColour("#2D2B55")
        font = self.clear_button.GetFont()
        font = font.Bold()
        self.clear_button.SetFont(font)
        self.clear_button.Bind(wx.EVT_BUTTON, self.OnClearButtonClick)
        hbox_buttons.Add(self.clear_button, flag=wx.LEFT, border=10)
        
        # Add a spacer between Show Diagnostics and Run buttons
        hbox_buttons.AddSpacer(10)  # Add 10 pixels of horizontal space

        # Run button
        self.run_button = wx.Button(panel, label='Run')
        self.run_button.SetBackgroundColour("#FAD000")
        self.run_button.SetForegroundColour("#2D2B55")
        font = self.run_button.GetFont()
        font = font.Bold()
        self.run_button.SetFont(font)
        self.run_button.Bind(wx.EVT_BUTTON, self.OnRunButtonClick)
        hbox_buttons.Add(self.run_button, flag=wx.LEFT, border=10)
        
        # Add a spacer between Run and Show Source buttons
        hbox_buttons.AddSpacer(10)  # Add 10 pixels of horizontal space

        # Show Source button
        self.show_source_button = wx.Button(panel, label='Show Source')
        self.show_source_button.SetBackgroundColour("#FAD000")
        self.show_source_button.SetForegroundColour("#2D2B55")
        font = self.show_source_button.GetFont()
        font = font.Bold()
        self.show_source_button.SetFont(font)
        self.show_source_button.Bind(wx.EVT_BUTTON, self.OnShowSourceButtonClick)
        hbox_buttons.Add(self.show_source_button, flag=wx.LEFT, border=10)
        
        # Add a spacer between Show Source and Show Full Log buttons
        hbox_buttons.AddSpacer(10)  # Add 10 pixels of horizontal space

        # Show Full Log button
        self.show_full_log_button = wx.Button(panel, label='Show Full Log')
        self.show_full_log_button.SetBackgroundColour("#FAD000")
        self.show_full_log_button.SetForegroundColour("#2D2B55")
        font = self.show_full_log_button.GetFont()
        font = font.Bold()
        self.show_full_log_button.SetFont(font)
        self.show_full_log_button.Bind(wx.EVT_BUTTON, self.OnShowFullLogButtonClick)
        hbox_buttons.Add(self.show_full_log_button, flag=wx.LEFT, border=10)
        
        # Add a spacer between Show Full Log and Help buttons
        hbox_buttons.AddSpacer(10)  # Add 10 pixels of horizontal space

        # Help button
        self.help_button = wx.Button(panel, label='Help')
        self.help_button.SetBackgroundColour("#FAD000")
        self.help_button.SetForegroundColour("#2D2B55")
        font = self.help_button.GetFont()
        font = font.Bold()
        self.help_button.SetFont(font)
        self.help_button.Bind(wx.EVT_BUTTON, self.OnHelpButtonClick)
        hbox_buttons.Add(self.help_button, flag=wx.LEFT, border=10)
        
        # Add a spacer between Show Full Log and Customise buttons
        hbox_buttons.AddSpacer(10)  # Add 10 pixels of horizontal space

        # Customise button
        self.customise_button = wx.Button(panel, label='Customise')
        self.customise_button.SetBackgroundColour("#FAD000")
        self.customise_button.SetForegroundColour("#2D2B55")
        font = self.customise_button.GetFont()
        font = font.Bold()
        self.customise_button.SetFont(font)
        self.customise_button.Bind(wx.EVT_BUTTON, self.OnCustomiseButtonClick)
        hbox_buttons.Add(self.customise_button, flag=wx.LEFT, border=10)

        # Time/Space Complexity Labels
        hbox_complexity = wx.BoxSizer(wx.HORIZONTAL)  # Horizontal box sizer for centering
        self.complexity_label = wx.StaticText(panel, label="")
        self.complexity_label.SetForegroundColour("#FAD000")
        font = self.complexity_label.GetFont()
        font.PointSize += 2
        self.complexity_label.SetFont(font)

        # Add the label to the horizontal sizer and center it
        hbox_complexity.Add(self.complexity_label, flag=wx.ALIGN_CENTER)
        vbox.Add(hbox_complexity, flag=wx.ALIGN_CENTER | wx.TOP, border=5)
        
        # Add a spacer between the buttons and the output panel
        vbox.AddSpacer(10)

        # Output Header
        output_label = wx.StaticText(panel, label='Sicher Output:')
        output_label.SetForegroundColour("#FAD000")
        font = output_label.GetFont()
        font.PointSize += 5
        font = font.Bold()
        output_label.SetFont(font)
        vbox.Add(output_label, flag=wx.ALIGN_LEFT | wx.TOP | wx.LEFT, border=10)
        output_label.SetBackgroundColour("#2D2B55")
        vbox.AddSpacer(10)

        # Output panel for collapsible sections
        self.output_panel = wx.Panel(panel)
        self.output_panel.SetBackgroundColour("#1E1E3F")
        self.output_sizer = wx.BoxSizer(wx.VERTICAL)
        self.output_panel.SetSizer(self.output_sizer)
        vbox.Add(self.output_panel, proportion=1, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)

        # adjust the vbox sizer to fit the panel
        panel.SetSizer(vbox)

        # Gives the GUI window the Sicher C Compiler title
        self.SetTitle('Sicher C Compiler')

        # Centers the GUI window on the screen
        self.Centre()

    # Compile button logic
    def OnCompile(self, event):
        # get the filepath from the file picker
        filepath = self.file_picker.GetPath()

        # check if no file was selected
        if not filepath:
            # tell the user the to select a file as the filepicker is empty
            wx.MessageBox('Please select a file to compile', 'Error', wx.OK | wx.ICON_ERROR)
            return

        # Check if the file exists
        if not os.path.isfile(filepath):
            # tell the user the file does not exist
            wx.MessageBox('File does not exist', 'Error', wx.OK | wx.ICON_ERROR)
            return

        # Check if the file is a C source file
        if not filepath.endswith('.c'):
            # tell the user the file is not a C source file
            wx.MessageBox('File is not a C source file', 'Error', wx.OK | wx.ICON_ERROR)
            return

        # Check if the file is empty
        if os.path.getsize(filepath) == 0:
            # tell the user the file is empty
            wx.MessageBox('File is empty', 'Error', wx.OK | wx.ICON_ERROR)
            return

        # Check if the file is readable
        try:
            # try and open the filepath
            with open(filepath, 'r') as file:
                # as it can be opened no error was raised
                pass
            
        # handle any IO errors that may occur while attempting to read the file
        except IOError:
            # tell the user there was an error reading the file
            wx.MessageBox('Error reading file', 'Error', wx.OK | wx.ICON_ERROR)
            return

        # Clear the output panel
        self.output_panel.DestroyChildren()

        try:
            # Read the source file
            with open(filepath, 'r') as file:
                # save the source file as code
                code = file.read()

            # Measure start time and CPU usage
            start_time = time.time() # start the compile timer
            process = psutil.Process() # get the current process (sicher)
            initial_memory = process.memory_info().rss  # Memory usage in bytes
            initial_cpu_times = process.cpu_times()  # Start measuring CPU times

            # Tokenization
            tokens, tokeniser_log = tokenise(code, debug=True) # tokenise the code (infer the tokeniser module)
            self.add_collapsible_section("Tokenisation Module", tokeniser_log)  # Display the debug output

            # Parsing
            parsing_debug_output = parse_tokens(tokens, debug=True) # parse the tokens (infer the parser module)
            self.add_collapsible_section("Parser Module", parsing_debug_output) # Display the debug output

            # Analyzing
            ast = create_ast_from_tokens(tokens, debug=True) # create the AST (infer the analyser module)
            self.add_collapsible_section("Analyser Module (Abstract Syntax Tree)", ast.pretty_print()) # Display the AST

            # Code Generation
            codegen = CodeGenerator(ast) # create the code generator object (infer the code generator module)
            generated_code = codegen.generate_code() # generate the code using the code generator object
            self.add_collapsible_section("Code Generator Module", generated_code) # Display the generated code

            # Save the generated code to a file
            codegen.save_code_to_file('output.ll')

            # Compile the generated code to an ARM64 binary
            output_binary_name = getattr(self, "custom_binary_name", "output_binary")  # Use custom name if set
            codegen.compile_to_arm64('output.ll', output_binary_name) # save as the custom binary name

            # Display success message
            wx.MessageBox(f"Compilation successful! Binary saved as: {output_binary_name}", "Success", wx.OK | wx.ICON_INFORMATION)

            # End time and CPU usage
            end_time = time.time() # stop the compile timer
            final_memory = process.memory_info().rss  # Memory usage in bytes
            final_cpu_times = process.cpu_times()  # End measuring CPU times

            # Calculate time complexity
            time_complexity = end_time - start_time # get the time to compile

            # Calculate memory usage (RAM usage)
            memory_usage = (final_memory - initial_memory) / (1024 * 1024)  # Convert to MB

            # Calculate CPU usage
            cpu_time_used = (
                (final_cpu_times.user - initial_cpu_times.user) +
                (final_cpu_times.system - initial_cpu_times.system)
            ) # get the cpu time used 
            
            cpu_usage_percentage = (cpu_time_used / time_complexity) * 100 if time_complexity > 0 else 0 # compute the cpu usage percentage by using the cpu time divided by the time to compile

            # Update the performance labels with the time to compile, memory usage and cpu usage
            self.complexity_label.SetLabel(
                f"Time to Compile: {time_complexity:.2f} seconds | " # to 2 decimal places for the secounds
                f"Memory Usage: {memory_usage:.2f} MB | " # to 2 decimal places for the memory usage
                f"CPU Usage: {cpu_usage_percentage:.2f}%" # to 2 decimal places for the cpu percentage
            )

            # Top Level Viz
            self.add_top_level_viz(ast) # show the top level visualisation of the AST

        # handle any exceptions
        except Exception as e:
            # tell the user an error has occured as a wx message box/alert
            wx.MessageBox(f"Error: {e}", 'Error', wx.OK | wx.ICON_ERROR)

    # Defines a method to add collapsable sections housing each of the Sicher Modules work plus the additional top level viz
    def add_collapsible_section(self, title, content):
        # Create a collapsible pane for a given content (.e. module container/top level viz)
        collapsible_pane = wx.CollapsiblePane(
            self.output_panel,
            label=title,
            style=wx.CP_DEFAULT_STYLE | wx.CP_NO_TLW_RESIZE
        )
        
        # bind the created collapsible pane to the event handler
        collapsible_pane.Bind(wx.EVT_COLLAPSIBLEPANE_CHANGED, self.on_collapsible_pane_changed)

        # Set the arrow color to yellow (same as buttons)
        collapsible_pane.SetForegroundColour("#FAD000")
        collapsible_pane.SetBackgroundColour("#1E1E3F")

        # Make the collapsible pane visible by default
        collapsible_pane.Collapse(False)

        # Add content to the collapsible pane
        pane = collapsible_pane.GetPane()
        
        # set the text controls of the panel
        text_ctrl = wx.TextCtrl(
            pane,
            value=content,
            style=wx.TE_MULTILINE | wx.TE_READONLY | wx.BORDER_NONE
        )
        
        # set the styling of the text control
        text_ctrl.SetBackgroundColour("#1E1E3F") # the dark purple colour
        text_ctrl.SetForegroundColour("#FAD000") # the yellow colour

        # Adjust the height of the collapsible boxes
        text_ctrl.SetMinSize((-1, 150))  # Set a minimum height of 150 pixels

        # Layout for the collapsible pane
        pane_sizer = wx.BoxSizer(wx.VERTICAL) # define the pane sizer
        pane_sizer.Add(text_ctrl, proportion=1, flag=wx.EXPAND) # add the text control to the pane sizer
        pane.SetSizer(pane_sizer) # set the sizer of the pane to be the pane sizer

        # Add the collapsible pane to the output panel
        self.output_sizer.Add(collapsible_pane, flag=wx.EXPAND | wx.ALL, border=5)
        
        # output panel layout
        self.output_panel.Layout()

    # handle the collapsable pane changes
    def on_collapsible_pane_changed(self, event):
        # redraw the layout of the output panel
        self.output_panel.Layout()
        
    # Event handler for the clear button
    def OnClearButtonClick(self, event):
        """
        Handles the "Clear" button click.
        Clears all collapsible sections and destroys their content.
        """
        # Destroy all children of the output panel
        self.output_panel.DestroyChildren()

        # Refresh the layout to reflect the changes
        self.output_panel.Layout()

    # Function to add the top level viz diagram/graphic of the AST
    def add_top_level_viz(self, ast):
        """
        Adds a top-level visualization of the AST to the output panel.

        Args:
            ast: The root of the AST.
        """
        
        # add a collapsible pane for the top level visualisation
        collapsible_pane = wx.CollapsiblePane(
            self.output_panel,
            label="Top Level Visualisation",
            style=wx.CP_DEFAULT_STYLE | wx.CP_NO_TLW_RESIZE
        )
        
        # bind the top level viz collapsable pane to the gui    
        collapsible_pane.Bind(wx.EVT_COLLAPSIBLEPANE_CHANGED, self.on_collapsible_pane_changed)

        # Make the collapsible pane visible by default
        collapsible_pane.Collapse(False) # is not collapsed by default

        # Create the visualization panel
        viz_panel = ASTVisualizerPanel(collapsible_pane.GetPane(), ast)
        viz_panel.SetMinSize((800, 600))  # set the top level viz pane to (800, 600) pixels
        
        # Add the visualization panel to the collapsible pane
        pane_sizer = wx.BoxSizer(wx.VERTICAL)
        pane_sizer.Add(viz_panel, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)
        collapsible_pane.GetPane().SetSizer(pane_sizer)

        # Add the collapsible pane to the output panel
        self.output_sizer.Add(collapsible_pane, flag=wx.EXPAND | wx.ALL, border=5)
        
        # add the collapsable pane for the top level visualisation to the output panel
        self.output_panel.Layout()
        
    # Event handler for the run button
    def OnRunButtonClick(self, event):
        """
        Handles the "Run" button click.
        Executes the custom binary if set, otherwise executes the default binary.
        """
        # Use the custom binary name if set, otherwise default to "output_binary"
        binary_name = getattr(self, "custom_binary_name", "output_binary")

        # try and run the compiled binary
        try:
            # get the executable binary from the current directory
            result = subprocess.run([f"./{binary_name}"], capture_output=True, text=True, check=True) # will default to ./output_binary if no custom binary name is set by the user using the customise button

            # Display the output in a collapsible section
            output = result.stdout.strip() if result.stdout else "No output." # get the output from the binary
            
            # add the output to the output panel with the run output title
            self.add_collapsible_section("Run Output", output)

        # handle any run binary errors
        except subprocess.CalledProcessError as e:
            # Handle errors during execution
            error_message = f"Error running ./{binary_name}:\n{e.stderr.strip() if e.stderr else str(e)}" # get the error message from the binary
            
            # tell the user there was an error running the binary along with the above error message
            self.add_collapsible_section("Run Output (Error)", error_message)
            
        # handle file not found errors
        except FileNotFoundError:
            # Handle the case where the binary does not exist
            self.add_collapsible_section("Run Output (Error)", f"Error: ./{binary_name} not found.") # tell the user the binary was not found
            
    # Event handler for the show source button
    def OnShowSourceButtonClick(self, event):
        """
        Handles the "Show Source" button click.
        Displays the content of the input C source file in a collapsible section.
        """
        
        # get the filepath from the file picker
        filepath = self.file_picker.GetPath()

        # check if no file was selected
        if not filepath:
            # tell the user the to select a file as the filepicker is empty
            wx.MessageBox('Please select a file to display', 'Error', wx.OK | wx.ICON_ERROR)
            # return back to the gui
            return

        # Check if the file does not exist
        if not os.path.isfile(filepath):
            # tell the user the file does not exist
            wx.MessageBox('File does not exist', 'Error', wx.OK | wx.ICON_ERROR)
            # return back to the gui
            return

        # Check if the file can be read
        try:
            # try and open the source file
            with open(filepath, 'r') as file:
                # set the source code to the file being currently read
                source_code = file.read()

            # Display the source code in a collapsible section
            self.add_collapsible_section("Source Code", source_code)

        # handle io errors
        except IOError:
            # tell the user there was an error reading the file
            wx.MessageBox('Error reading file', 'Error', wx.OK | wx.ICON_ERROR)
            
    # Event handler for the show full log button
    def OnShowFullLogButtonClick(self, event):
        """
        Handles the "Show Full Log" button click.
        Runs sicher.py with the --debug flag and displays the full log in a collapsible section.
        """
        # get the filepath from the file picker
        filepath = self.file_picker.GetPath()

        # check if no file was selected
        if not filepath:
            # tell the user the to select a file as the filepicker is empty
            wx.MessageBox('Please select a file to compile', 'Error', wx.OK | wx.ICON_ERROR)
            return

        # Check if the source file does not exists
        if not os.path.isfile(filepath):
            # tell the user the file does not exist
            wx.MessageBox('File does not exist', 'Error', wx.OK | wx.ICON_ERROR)
            
            # return back to the gui
            return

        # capture the full log output from sicher.py (the entry point)
        try:
            # Run sicher.py as a subprocess with the --debug flag so I can capture the ouput
            result = subprocess.run(
                ["python3", "src/sicher.py", filepath, "--debug"],
                capture_output=True,
                text=True,
                check=True
            )

            # Capture the debug output
            debug_log = result.stdout.strip()

            # Display the debug log in a collapsible section
            self.add_collapsible_section("Full Debug Log", debug_log)

        # handle execution errors
        except subprocess.CalledProcessError as e:
            # Handle errors during execution
            error_message = f"Error running sicher.py:\n{e.stderr.strip() if e.stderr else str(e)}" # get the error message from the binary
            # tell the user there was an error running sicher.py along with the above error message in the collapsable section
            self.add_collapsible_section("Full Debug Log (Error)", error_message)
            
        # handle file not found errors
        except FileNotFoundError:
            # Handle the case where sicher.py is not found and the user is using the GUI
            self.add_collapsible_section("Full Debug Log (Error)", "Error: sicher.py not found.")
            
    # Event handler for the help button
    def OnHelpButtonClick(self, event):
        """
        Handles the "Help" button click.
        Displays an alert box explaining the Visualiser features and Sicher functionality.
        """
        
        # create the help text of which an alert will be shown if the on help button is clicked
        help_text = (
            "Welcome to the Sicher C Compiler Visualiser!\n\n"
            "Features:\n"
            "- Compile: Compiles the selected C source file and displays the output of each module.\n"
            "- Generate Visualisations: Compiles the file multiple times and generates performance metrics (time, memory, CPU usage).\n"
            "- Show Diagnostics: Displays system and Sicher-specific diagnostics.\n"
            "- Run: Executes the compiled binary and displays its output.\n"
            "- Show Source: Displays the content of the selected C source file.\n"
            "- Show Full Log: Runs Sicher with the --debug flag and displays the full debug log.\n"
            "- Help: Displays this help dialog.\n"
            "- Customise: Allows you to specify a custom output binary name.\n\n"
            
            "How to Use Sicher:\n"
            "1. Use the file picker to select a C source file.\n"
            "2. Click 'Compile' to compile the file and view the output.\n"
            "3. Use other buttons to explore additional features.\n\n"
            
            "Time/Space Complexity Labels:\n"
            "- Time to Compile: The time taken to compile the file.\n"
            "- Memory Usage: The memory used during compilation.\n"
            "- CPU Usage: The percentage of CPU used during compilation.\n\n"
            
            "About Sicher:\n"
            "Sicher is a C compiler that tokenizes, parses, analyzes, and generates assembly code for C programs and then proceeds to create a executable Binary for it. "
            "It also provides performance metrics and visualizations for educational purposes."
        )

        # add the help text to a message box using wx
        wx.MessageBox(help_text, "Help - Sicher C Compiler", wx.OK | wx.ICON_INFORMATION)
        
    # Event handler for the customise button
    def OnCustomiseButtonClick(self, event):
        """
        Handles the "Customise" button click.
        Opens a popup dialog for the user to specify a custom output binary name.
        """
        # Create a dialog for the user to enter a custom binary name
        dialog = wx.TextEntryDialog(
            self,
            "Enter a custom output binary name:",
            "Customise Output Binary",
            value="output_binary"
        )

        # check if the user clicked ok
        if dialog.ShowModal() == wx.ID_OK:
            # Get the custom binary name from the dialog
            self.custom_binary_name = dialog.GetValue().strip()

            # check if the custom binary name is empty
            if not self.custom_binary_name:
                # tell the user the custom binary name cannot be empty
                wx.MessageBox("Binary name cannot be empty.", "Error", wx.OK | wx.ICON_ERROR)
                
            # if the user entered a custom binary name
            else:
                # tell the user the custom binary name has been set
                wx.MessageBox(f"Custom binary name set to: {self.custom_binary_name}", "Success", wx.OK | wx.ICON_INFORMATION)

        # remove the customise dialog/alert box as I no longer need it
        dialog.Destroy()

# Class to modal the top level visualisation of the AST
class ASTVisualizerPanel(wx.ScrolledWindow):
    # constructor for the AST visualiser panel
    def __init__(self, parent, ast):
        # use the parent class constructor to initialise the panel
        super(ASTVisualizerPanel, self).__init__(parent)
        
        # get the ast
        self.ast = ast
        
        # set the background colour of the panel to be the dark purple colour
        self.SetBackgroundColour("#1E1E3F")

        # Enable scrolling of the panel
        self.SetScrollbars(20, 20, 50, 50)  # create the scrollbars
        self.virtual_size = (2000, 2000)  # a virtual size to allow for an expanded and scrollable area
        self.SetVirtualSize(self.virtual_size)

        # Variables for panning
        self.is_panning = False # check if the user is panning
        self.last_mouse_position = None # get the last mouse position

        # Bind events
        self.Bind(wx.EVT_PAINT, self.OnPaint) # when user is panning
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown) # get the left mouse button down
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp) # get the left mouse button up
        self.Bind(wx.EVT_MOTION, self.OnMouseMove) # get the mouse moving

    # function to create the visualisation of the AST
    def OnPaint(self, event):
        # get the drawing context for the top level visualisation
        dc = wx.PaintDC(self)
        
        # allow for scrolling of the top level viz
        self.PrepareDC(dc)  # Adjust for scrolling
        
        # creat the graphic context visualiser for the drwing content of the top level viz
        gc = wx.GraphicsContext.Create(dc)

        # if we have a graphic context
        if gc:
            # set the yellow theme for the node 'box'/rectangle
            gc.SetBrush(wx.Brush("#FAD000"))  # Yellow theme color
            gc.SetPen(wx.Pen("#FAD000", 2))  # Yellow border

            # Start drawing the AST nodes
            self.draw_node(gc, self.ast.root, 1000, 50, 200, 100)  # Centered in the virtual space

    # function to draw a node
    def draw_node(self, gc, node, x, y, x_offset, y_offset, depth=0):
        # check if we have a node
        if not node:
            # if no node is stop the drawing
            return

        # Alternate colors based on depth (even: bright yellow, odd: darker yellow)
        color = "#FAD000" if depth % 2 == 0 else "#C9A000"  # Bright yellow for even layers, darker yellow for odd layers

        # Set the brush and pen color for the rectangle
        gc.SetBrush(wx.Brush(color)) # use the alternating color for the node
        gc.SetPen(wx.Pen(color, 2)) # use the alternating color for the node border

        # Draw the current node as a rectangle
        rect_width, rect_height = 120, 50 # set the dimensions of the node rectangle
        gc.DrawRectangle(x - rect_width // 2, y, rect_width, rect_height) # draw the node rectangle

        # Draw the node label
        label_lines = [node.node_type, node.value] if node.value else [node.node_type]

        # Draw the node type (bold)
        gc.SetFont(wx.Font(10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD), "#2D2B55") # set font styling for the node
        gc.DrawText(label_lines[0], x - rect_width // 2 + 10, y + 10) # draw the label of the box

        # Draw the node value (normal)
        if len(label_lines) > 1:
            gc.SetFont(wx.Font(10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL), "#2D2B55") # set font styling for the node value
            gc.DrawText(label_lines[1], x - rect_width // 2 + 10, y + 25) # draw the value of the box

        # Calculate positions for child nodes
        # get number of children for a node
        num_children = len(node.children)
        # check if we have children
        if num_children > 0:
            child_y = y + y_offset + 20  # add some y padding
            child_x_start = x - (x_offset * (num_children - 1)) // 2 # create the x position start for the child

            # for the children draw child nodes rectangle boxes in the top lvel viz
            for i, child in enumerate(node.children):
                # create the x position for the child node
                child_x = child_x_start + i * x_offset

                # Draw an arrow to the child node
                gc.SetPen(wx.Pen("#FAD000", 2))  # Keep arrows bright yellow
                gc.StrokeLine(x, y + rect_height, child_x, child_y) # create the arrow to both childs

                # Recursively draw the child node, increasing the depth for every child
                self.draw_node(gc, child, child_x, child_y, x_offset, y_offset, depth + 1) # for all children draw a top level viz complete with arrows and alternating colours for each line depth

    # get left click down
    def OnLeftDown(self, event):
        # Start panning
        self.is_panning = True
        # capture the last mouse position
        self.last_mouse_position = event.GetPosition()
        
        # capture mouse data
        self.CaptureMouse()

    # get left click up /stop panning
    def OnLeftUp(self, event):
        # Stop panning
        if self.is_panning:
            # stop panning
            self.is_panning = False
            
            # release mouse data
            self.ReleaseMouse()

    # function to calculate mouse movmeent
    def OnMouseMove(self, event):
        # check if panning or dragging or left mouse button is down
        if self.is_panning and event.Dragging() and event.LeftIsDown():
            # get the current mouse position
            current_position = event.GetPosition()
            # modify the scroll position based on the mouse movement
            dx = self.last_mouse_position.x - current_position.x # the difference in x position for the scroll
            dy = self.last_mouse_position.y - current_position.y # the difference in y position for the scroll

            # Scroll the window
            self.Scroll(self.GetScrollPos(wx.HORIZONTAL) + dx // 20, self.GetScrollPos(wx.VERTICAL) + dy // 20) # scroll using the above deltas plus some 20px padding

            # update the last mouse position
            self.last_mouse_position = current_position

# Main loop to run the Visualiser GUI Module
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