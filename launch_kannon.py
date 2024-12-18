import argparse
import json
import multiprocessing
import os
import os.path as osp
import shutil
import sys
import time
from datetime import datetime

from kannon.visualizer import generate_visual_story, apply_japanese_aesthetics
from kannon.data_processing import process_data, check_data_quality
from kannon.review import perform_review, apply_improvements

NUM_ITERATIONS = 3

def print_time():
    """Log the current timestamp."""
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

def parse_arguments():
    """Parse command-line arguments for the Kannon SEA pipeline."""
    parser = argparse.ArgumentParser(description="Kannon SEA: Visual Storytelling")
    parser.add_argument("--dataset", type=str, required=True, help="Path to input dataset")
    parser.add_argument("--style", type=str, default="ukiyo-e", choices=["ukiyo-e", "sumi-e", "minimalist"], help="Artistic style for visuals")
    parser.add_argument("--output", type=str, default="output", help="Directory for visual outputs")
    parser.add_argument("--iterations", type=int, default=NUM_ITERATIONS, help="Number of iterations for refinement")
    parser.add_argument("--parallel", type=int, default=0, help="Number of parallel processes (0 for sequential)")
    return parser.parse_args()

def worker(task_queue, style, output_dir, lock):
    """Process tasks for visual storytelling."""
    print(f"Worker started.")
    while True:
        task = task_queue.get()
        if task is None:
            break
        with lock:
            print(f"Processing task: {task}")
            data = process_data(task["dataset"])
            data = check_data_quality(data)
            visual_story = generate_visual_story(data, style=style)
            apply_japanese_aesthetics(visual_story, style)
            save_visual_story(visual_story, output_dir, task["name"])
        print(f"Task {task['name']} completed.")
    print("Worker finished.")

def save_visual_story(visual_story, output_dir, task_name):
    """Save the visual story to the output directory."""
    os.makedirs(output_dir, exist_ok=True)
    output_path = osp.join(output_dir, f"{task_name}_visual_story.png")
    visual_story.save(output_path)
    print(f"Saved visual story to {output_path}")

if __name__ == "__main__":
    args = parse_arguments()

    # Prepare output directory
    os.makedirs(args.output, exist_ok=True)

    # Prepare tasks
    tasks = [{"dataset": args.dataset, "name": f"story_{i}"} for i in range(args.iterations)]

    if args.parallel > 0:
        # Parallel processing
        task_queue = multiprocessing.Queue()
        lock = multiprocessing.Lock()

        # Add tasks to queue
        for task in tasks:
            task_queue.put(task)

        # Start workers
        workers = []
        for _ in range(args.parallel):
            worker_process = multiprocessing.Process(
                target=worker,
                args=(task_queue, args.style, args.output, lock)
            )
            worker_process.start()
            workers.append(worker_process)

        # Add termination signals to queue
        for _ in range(args.parallel):
            task_queue.put(None)

        # Wait for workers to finish
        for worker_process in workers:
            worker_process.join()
    else:
        # Sequential processing
        for task in tasks:
            data = process_data(task["dataset"])
            data = check_data_quality(data)
            visual_story = generate_visual_story(data, style=args.style)
            apply_japanese_aesthetics(visual_story, args.style)
            save_visual_story(visual_story, args.output, task["name"])

    print("All tasks completed.")