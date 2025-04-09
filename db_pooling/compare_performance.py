#!/usr/bin/env python3

"""
Performance Comparison: With vs Without Connection Pooling

This script compares the performance of database operations
with and without connection pooling. It runs benchmarks on both
implementations and provides a detailed comparison.
"""

import os
import sys
import subprocess
import time
import matplotlib.pyplot as plt
import numpy as np
import matplotlib

class PerformanceComparer:
    """Handles running benchmarks and capturing output"""
    
    def __init__(self, num_operations=10000):
        self.num_operations = num_operations
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.without_pool_script = os.path.join(self.script_dir, "without_pool", "db_without_pool.py")
        self.with_pool_script = os.path.join(self.script_dir, "with_pool", "db_with_pool.py")
        self.sqlalchemy_script = os.path.join(self.script_dir, "with_pool", "sqlalchemy_pool_example.py")
    
    def run_benchmark(self, script_path):
        """Run a benchmark script and return its output"""
        print(f"Running {script_path}...")
        print(f"This may take several minutes due to the increased dataset size ({self.num_operations} operations)")
        print("Please wait...")
        
        start_time = time.time()
        try:
            result = subprocess.run(
                [sys.executable, script_path, str(self.num_operations)],
                capture_output=True,
                text=True,
                check=True
            )
            elapsed = time.time() - start_time
            print(f"Completed in {elapsed:.2f} seconds")
            print("Output:")
            print(result.stdout)
            return result.stdout
        except subprocess.CalledProcessError as e:
            print(f"Error running {script_path}:")
            print(e.stderr)
            return None
    
    def extract_benchmark_results(self, output):
        """Extract benchmark results from script output"""
        if not output:
            return None
            
        results = {}
        for line in output.strip().split("\n"):
            if "Insert time:" in line:
                results["insert_time"] = float(line.split(":")[-1].strip().split()[0])
            elif "Query time:" in line:
                results["query_time"] = float(line.split(":")[-1].strip().split()[0])
            elif "Update time:" in line:
                results["update_time"] = float(line.split(":")[-1].strip().split()[0])
            elif "Total time:" in line:
                results["total_time"] = float(line.split(":")[-1].strip().split()[0])
        return results
    
    def run_all_benchmarks(self):
        """Run all benchmarks and return their results"""
        print("\nRunning benchmarks with 10,000 operations (100x increased dataset)")
        print("This will take longer but provide more accurate results")
        print("=" * 50)
        
        # Run without pool benchmark
        without_pool_output = self.run_benchmark(self.without_pool_script)
        without_pool_results = self.extract_benchmark_results(without_pool_output)
        
        # Run with pool benchmark
        with_pool_output = self.run_benchmark(self.with_pool_script)
        with_pool_results = self.extract_benchmark_results(with_pool_output)
        
        # Check if SQLAlchemy is installed
        try:
            import sqlalchemy
            sqlalchemy_installed = True
        except ImportError:
            sqlalchemy_installed = False
        
        sqlalchemy_results = None
        if sqlalchemy_installed:
            sqlalchemy_output = self.run_benchmark(self.sqlalchemy_script)
            sqlalchemy_results = self.extract_benchmark_results(sqlalchemy_output)
        else:
            print("\nNote: SQLAlchemy is not installed. Skipping SQLAlchemy pooling example.")
            print("To install SQLAlchemy, run: pip install sqlalchemy")
        
        return without_pool_results, with_pool_results, sqlalchemy_results

class ResultAnalyzer:
    """Analyzes and prints benchmark results in table format"""
    
    def print_comparison_table(self, without_pool, with_pool, sqlalchemy_pool=None):
        """Print a formatted comparison table of the results"""
        print("\n")
        print("=" * 90)
        print("PERFORMANCE COMPARISON TABLE (10,000 OPERATIONS)".center(90))
        print("=" * 90)
        
        headers = ["Operation", "Without Pool", "With Custom Pool", "Improvement"]
        if sqlalchemy_pool:
            headers.append("SQLAlchemy Pool")
            headers.append("SQLAlchemy Improvement")
        
        # Print headers
        header_format = "{:<15} {:<15} {:<15} {:<15}"
        if sqlalchemy_pool:
            header_format += " {:<15} {:<15}"
        
        print(header_format.format(*headers))
        print("-" * 90)
        
        # Prepare data
        operations = ["Insert", "Query", "Update", "Total"]
        without_pool_data = [
            without_pool["insert_time"],
            without_pool["query_time"],
            without_pool["update_time"],
            without_pool["total_time"]
        ]
        with_pool_data = [
            with_pool["insert_time"],
            with_pool["query_time"],
            with_pool["update_time"],
            with_pool["total_time"]
        ]
        
        if sqlalchemy_pool:
            sqlalchemy_data = [
                sqlalchemy_pool["insert_time"],
                sqlalchemy_pool["query_time"],
                sqlalchemy_pool["update_time"],
                sqlalchemy_pool["total_time"]
            ]
        
        # Print data rows
        row_format = "{:<15} {:<15.4f}s {:<15.4f}s {:<15.1f}%"
        if sqlalchemy_pool:
            row_format += " {:<15.4f}s {:<15.1f}%"
        
        for i, operation in enumerate(operations):
            improvement = (without_pool_data[i] - with_pool_data[i]) / without_pool_data[i] * 100
            
            if sqlalchemy_pool:
                sqlalchemy_improvement = (without_pool_data[i] - sqlalchemy_data[i]) / without_pool_data[i] * 100
                print(row_format.format(
                    operation, 
                    without_pool_data[i], 
                    with_pool_data[i], 
                    improvement,
                    sqlalchemy_data[i],
                    sqlalchemy_improvement
                ))
            else:
                print(row_format.format(
                    operation, 
                    without_pool_data[i], 
                    with_pool_data[i], 
                    improvement
                ))
        
        print("=" * 90)
        print("\nNote: Positive improvement percentages indicate better performance with connection pooling.")
        print("\nKey Takeaways:")
        print("1. Connection pooling significantly reduces database operation time.")
        print("2. The performance improvement is especially noticeable for operations")
        print("   that require establishing new connections frequently.")
        print("3. SQLAlchemy's connection pooling provides additional features like")
        print("   connection recycling, overflow handling, and connection validation.")

class PerformanceVisualizer:
    """Creates visualizations of benchmark results"""
    
    def create_comparison_chart(self, without_pool, with_pool, sqlalchemy_pool=None):
        """Create a bar chart comparing pooled and non-pooled performance"""
        labels = ["Insert", "Query", "Update", "Total"]
        no_pool_data = [
            without_pool["insert_time"],
            without_pool["query_time"],
            without_pool["update_time"],
            without_pool["total_time"]
        ]
        
        custom_pool_data = [
            with_pool["insert_time"],
            with_pool["query_time"],
            with_pool["update_time"],
            with_pool["total_time"]
        ]
        
        # Set width of bars
        barWidth = 0.25
        
        # Set positions of the bars on X axis
        r1 = np.arange(len(labels))
        r2 = [x + barWidth for x in r1]
        
        # Create figure
        plt.figure(figsize=(14, 10))
        
        # Create bars
        plt.bar(r1, no_pool_data, width=barWidth, edgecolor='grey', label='Without Pool')
        plt.bar(r2, custom_pool_data, width=barWidth, edgecolor='grey', label='With Custom Pool')
        
        # Add SQLAlchemy data if provided
        if sqlalchemy_pool:
            sqlalchemy_data = [
                sqlalchemy_pool["insert_time"],
                sqlalchemy_pool["query_time"],
                sqlalchemy_pool["update_time"],
                sqlalchemy_pool["total_time"]
            ]
            r3 = [x + barWidth for x in r2]
            plt.bar(r3, sqlalchemy_data, width=barWidth, edgecolor='grey', label='SQLAlchemy Pool')
            
            # Adjust labels position
            plt.xticks([r + barWidth for r in range(len(labels))], labels)
        else:
            # Adjust labels position
            plt.xticks([r + barWidth/2 for r in range(len(labels))], labels)
        
        # Calculate improvement percentages
        improvements = []
        for i in range(len(no_pool_data)):
            improvement = (no_pool_data[i] - custom_pool_data[i]) / no_pool_data[i] * 100
            improvements.append(improvement)
        
        # Find the maximum value to adjust label position
        all_values = no_pool_data.copy()
        all_values.extend(custom_pool_data)
        if sqlalchemy_pool:
            all_values.extend(sqlalchemy_data)
        max_value = max(all_values)
        label_offset = max_value * 0.03  # 3% of max value
        
        # Add labels above the bars
        for i in range(len(r1)):
            plt.text(r1[i], no_pool_data[i] + label_offset, f"{no_pool_data[i]:.2f}s", ha='center', va='bottom')
            plt.text(r2[i], custom_pool_data[i] + label_offset, f"{custom_pool_data[i]:.2f}s\n({improvements[i]:.1f}% faster)", 
                    ha='center', va='bottom', color='green' if improvements[i] > 0 else 'red')
        
        # Add SQLAlchemy labels if provided
        if sqlalchemy_pool:
            sqlalchemy_improvements = []
            for i in range(len(no_pool_data)):
                improvement = (no_pool_data[i] - sqlalchemy_data[i]) / no_pool_data[i] * 100
                sqlalchemy_improvements.append(improvement)
            
            for i in range(len(r3)):
                plt.text(r3[i], sqlalchemy_data[i] + label_offset, f"{sqlalchemy_data[i]:.2f}s\n({sqlalchemy_improvements[i]:.1f}% faster)", 
                        ha='center', va='bottom', color='green' if sqlalchemy_improvements[i] > 0 else 'red')
        
        # Add labels and title
        plt.xlabel('Operation Type', fontweight='bold', fontsize=14)
        plt.ylabel('Time (seconds)', fontweight='bold', fontsize=14)
        plt.title('Database Operation Performance Comparison\n(10,000 operations)', fontweight='bold', fontsize=18)
        plt.legend(fontsize=12)
        
        # Adjust y-axis to add some padding at the top for labels
        plt.ylim(0, max_value * 1.2)
        
        # Add grid for better readability
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        
        # Save figure
        plt.savefig('performance_comparison.png', dpi=300, bbox_inches='tight')
        print("Chart saved as 'performance_comparison.png'")
        
        # Try to display the chart (if running in an environment with display capabilities)
        try:
            plt.show()
        except:
            pass

def main():
    """Main function to run the performance comparison"""
    print("Database Connection Pooling Performance Comparison")
    print("=" * 50)
    
    # Create instances of our classes
    comparer = PerformanceComparer(num_operations=10000)
    analyzer = ResultAnalyzer()
    visualizer = PerformanceVisualizer()
    
    # Run benchmarks and get results
    without_pool_results, with_pool_results, sqlalchemy_results = comparer.run_all_benchmarks()
    
    # Print comparison table
    analyzer.print_comparison_table(without_pool_results, with_pool_results, sqlalchemy_results)
    
    # Try to create visualization
    try:
        visualizer.create_comparison_chart(without_pool_results, with_pool_results, sqlalchemy_results)
    except ImportError:
        print("\nNote: matplotlib is not installed. Skipping chart creation.")
        print("To install matplotlib, run: pip install matplotlib")
    
    print("\nComparison complete! You've seen the benefits of connection pooling firsthand.")
    print("Check out the README for more details about database connection pooling.")

if __name__ == "__main__":
    main() 