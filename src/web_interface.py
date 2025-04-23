from flask import Flask, request, render_template, redirect, url_for, flash
import os
from modules.tokeniser import tokenise
from modules.parser import parse_tokens
from modules.analyser import create_ast_from_tokens
from modules.codegenerator import CodeGenerator
import time
import psutil

app = Flask(__name__, template_folder='templates/')
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'your_secret_key'

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
        flash('No file part in the request.', 'error')
        return redirect(url_for('index'))
    
    file = request.files['file']
    if file.filename == '':
        flash('No file selected. Please choose a file to upload.', 'error')
        return redirect(url_for('index'))
    
    if not file.filename.endswith('.c'):
        flash('Invalid file type. Please upload a C source file.', 'error')
        return redirect(url_for('index'))
    
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    try:
        file.save(filepath)
        if os.stat(filepath).st_size == 0:
            flash('The uploaded file is empty. Please upload a valid C source file.', 'error')
            os.remove(filepath)
            return redirect(url_for('index'))
    except Exception as e:
        flash(f'Error saving the file: {str(e)}', 'error')
        return redirect(url_for('index'))
    
    return redirect(url_for('compile_file', filename=file.filename))

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
    debug = True 
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

        for _ in range(10):
            start_time = time.perf_counter() 
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
            end_time = time.perf_counter() 
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

            from modules.performance_plotter import generate_performance_plots
            fig = generate_performance_plots(compile_times, memory_usages, cpu_usages)

            plot_path = os.path.join('src', 'static', 'performance_plots.png')
            fig.savefig(plot_path)
            results['performance_plot'] = plot_path

    except Exception as e:
        results['error'] = str(e)

    compilation_history[filename] = results

    return render_template('results.html', filename=filename, results=results)

if __name__ == '__main__':
    app.run(debug=True)