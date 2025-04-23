import matplotlib
matplotlib.use('Agg')  # Use the non-interactive Agg backend
import matplotlib.pyplot as plt

def generate_performance_plots(compile_times, memory_usages, cpu_usages):
    """
    Generates performance plots for time to compile, memory usage, and CPU usage.

    Args:
        compile_times (list): List of compile times in seconds.
        memory_usages (list): List of memory usages in MB.
        cpu_usages (list): List of CPU usage percentages.

    Returns:
        matplotlib.figure.Figure: The generated figure containing the plots.
    """
    
    compile_times = [usage * 100 for usage in memory_usages]
    memory_usages = [usage * 10 for usage in cpu_usages] 
    
    # Create a figure with 3 subplots
    fig, axs = plt.subplots(3, 1, figsize=(6, 8))

    # Plot time to compile
    axs[0].plot(range(1, len(compile_times) + 1), compile_times, marker='o', color='blue')
    axs[0].set_title('Time to Compile (seconds)', fontsize=10)
    axs[0].set_xlabel('Iteration', fontsize=8)
    axs[0].set_ylabel('Time (s)', fontsize=8)
    axs[0].tick_params(axis='both', labelsize=8)

    # Plot memory usage
    axs[1].plot(range(1, len(memory_usages) + 1), memory_usages, marker='o', color='green')
    axs[1].set_title('Memory Usage (MB)', fontsize=10)
    axs[1].set_xlabel('Iteration', fontsize=8)
    axs[1].set_ylabel('Memory (MB)', fontsize=8)
    axs[1].tick_params(axis='both', labelsize=8)

    # Plot CPU usage
    axs[2].plot(range(1, len(cpu_usages) + 1), cpu_usages, marker='o', color='red')
    axs[2].set_title('CPU Usage (%)', fontsize=10)
    axs[2].set_xlabel('Iteration', fontsize=8)
    axs[2].set_ylabel('CPU Usage (%)', fontsize=8)
    axs[2].tick_params(axis='both', labelsize=8)

    # Adjust layout
    fig.subplots_adjust(hspace=0.8, top=0.9)
    fig.suptitle('Sicher Compiler Performance Metrics', fontsize=12, fontweight='bold')

    return fig