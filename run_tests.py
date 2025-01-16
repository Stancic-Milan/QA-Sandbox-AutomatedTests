import pytest
import argparse
import os
from datetime import datetime
from config import Config

def main():
    parser = argparse.ArgumentParser(description='Run UI Automation Tests')
    
    # Test selection options
    parser.add_argument('--tests', default='tests', help='Path to test files or directories')
    parser.add_argument('--markers', help='Run tests with specific pytest markers (e.g., smoke, regression)')
    
    # Browser options
    parser.add_argument('--browser', default=Config.BROWSER, 
                       choices=['chrome', 'firefox', 'edge'],
                       help='Browser to run tests')
    
    # Environment options
    parser.add_argument('--env', default=Config.ENV,
                       choices=['qa', 'dev', 'staging'],
                       help='Environment to run tests against')
    
    # Execution options
    parser.add_argument('--parallel', type=int, default=Config.PARALLEL_WORKERS,
                       help='Number of parallel processes')
    parser.add_argument('--reruns', type=int, default=Config.RETRY_COUNT,
                       help='Number of times to retry failed tests')
    parser.add_argument('--headless', action='store_true', default=Config.HEADLESS,
                       help='Run tests in headless mode')
    
    # Reporting options
    parser.add_argument('--html-report', action='store_true',
                       help='Generate HTML report')
    parser.add_argument('--video', action='store_true', default=Config.VIDEO_RECORDING,
                       help='Record video of test execution')
    
    args = parser.parse_args()

    # Create timestamp for report directory
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    report_dir = os.path.join('reports', timestamp)
    os.makedirs(report_dir, exist_ok=True)

    # Build pytest arguments
    pytest_args = [
        args.tests,
        '-v',
        f'--browser={args.browser}',
        f'--env={args.env}',
        f'--reruns={args.reruns}',
    ]

    # Add parallel execution if specified
    if args.parallel > 1:
        pytest_args.extend(['-n', str(args.parallel)])

    # Add markers if specified
    if args.markers:
        pytest_args.extend(['-m', args.markers])

    # Add HTML reporting if specified
    if args.html_report:
        report_path = os.path.join(report_dir, 'report.html')
        pytest_args.extend(['--html=' + report_path, '--self-contained-html'])

    # Add video recording if specified
    if args.video:
        video_path = os.path.join(report_dir, 'videos')
        os.makedirs(video_path, exist_ok=True)
        os.environ['VIDEO_OUTPUT_DIR'] = video_path

    # Set headless mode
    os.environ['HEADLESS'] = str(args.headless)

    # Run pytest with constructed arguments
    exit_code = pytest.main(pytest_args)

    # Print summary
    print("\nTest Execution Summary:")
    print(f"Environment: {args.env}")
    print(f"Browser: {args.browser}")
    print(f"Parallel Processes: {args.parallel}")
    print(f"Reruns: {args.reruns}")
    if args.html_report:
        print(f"HTML Report: {report_path}")
    if args.video:
        print(f"Video Recordings: {video_path}")
    print(f"Exit Code: {exit_code}")

if __name__ == '__main__':
    main()
