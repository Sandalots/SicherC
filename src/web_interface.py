from flask import Flask, request, render_template, redirect, url_for
import os
from modules.tokeniser import tokenise
from modules.parser import parse_tokens
from modules.analyser import create_ast_from_tokens
from modules.codegenerator import CodeGenerator
from modules.visualiser import main as visualiser
import time
import psutil

app = Flask(__name__, template_folder='templates/')
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

compilation_history = {} 

@app.context_processor
def inject_compilation_history():
    return {'compilation_history': compilation_history}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(url_for('index'))
    
    file = request.files['file']
    if file.filename == '':
        return redirect(url_for('index'))
    
    if file and file.filename.endswith('.c'):
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        return redirect(url_for('compile_file', filename=file.filename))
    else:
        return "Invalid file type. Please upload a C source file."

@app.route('/history')
def history():
    return render_template('history.html', history=compilation_history)

@app.route('/history/<filename>')
def view_history(filename):
    results = compilation_history.get(filename)
    if not results:
        return f"No history found for {filename}", 404
    return render_template('results.html', filename=filename, results=results)

@app.route('/compile/<filename>')
def compile_file(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    results = {}
    debug = True  # Assume debug is always enabled by default

    try:
        # Tokeniser
        with open(filepath, 'r') as file:
            code = file.read()
        tokens, tokeniser_log = tokenise(code, debug=debug)
        results['tokens'] = tokens
        results['tokeniser_log'] = tokeniser_log

        # Parser
        parser_debug_output = parse_tokens(tokens, debug=debug)
        results['parser_log'] = parser_debug_output

        # Analyser
        ast = create_ast_from_tokens(tokens, debug=debug)
        results['ast'] = ast.pretty_print()
        results['analyser_log'] = ast.debug_log if hasattr(ast, 'debug_log') else "No analyser debug log available."

        # Code Generator
        code_generator = CodeGenerator(ast)
        generated_code = code_generator.generate_code()
        results['generated_code'] = generated_code

        # Save and compile
        code_generator.save_code_to_file('output.ll')
        code_generator.compile_to_arm64('output.ll', 'output_binary')

        results['binary'] = "Compilation successful. Binary saved as 'output_binary'."

        # Performance Metrics
        compile_times = []
        memory_usages = []
        cpu_usages = []

        # Compile the file multiple times to gather performance metrics
        for _ in range(10):
            start_time = time.time()
            process = psutil.Process()
            initial_memory = process.memory_info().rss
            initial_cpu_times = process.cpu_times()

            # Tokenisation
            tokens, _ = tokenise(code, debug=True)

            # Parsing
            parse_tokens(tokens, debug=True)

            # Analyser
            ast = create_ast_from_tokens(tokens, debug=True)

            # Code Generation
            codegen = CodeGenerator(ast)
            codegen.generate_code()

            # Measure end time and resource usage
            end_time = time.time()
            final_memory = process.memory_info().rss
            final_cpu_times = process.cpu_times()

            # Calculate metrics
            compile_times.append(end_time - start_time)
            memory_usages.append((final_memory - initial_memory) / (1024 * 1024))
            cpu_time_used = (
                (final_cpu_times.user - initial_cpu_times.user) +
                (final_cpu_times.system - initial_cpu_times.system)
            )
            cpu_usages.append((cpu_time_used / (end_time - start_time)))

        # Generate performance plots
        from modules.performance_plotter import generate_performance_plots
        fig = generate_performance_plots(compile_times, memory_usages, cpu_usages)

        # Save the plots as an image
        # Save the plots as an image
        plot_path = os.path.join('src', 'static', 'performance_plots.png')
        fig.savefig(plot_path)
        results['performance_plot'] = plot_path

    except Exception as e:
        results['error'] = str(e)

    # Save results to history
    compilation_history[filename] = results

    return render_template('results.html', filename=filename, results=results)

if __name__ == '__main__':
    app.run(debug=True)