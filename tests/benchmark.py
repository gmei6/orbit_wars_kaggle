import cProfile
import pstats
import sys
import os

# Ensure the root project directory is on the path so we can import src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.sim import run
from src.agent import act

def main():
    print("Running mirror match benchmark...")
    # Run 5 games of 500 turns each
    for i in range(5):
        res = run(act, act, turns=500, seed=i)
        print(f"Game {i} finished: {res}")

if __name__ == "__main__":
    profiler = cProfile.Profile()
    profiler.enable()
    main()
    profiler.disable()
    stats = pstats.Stats(profiler).strip_dirs().sort_stats('cumtime')
    stats.print_stats(20)
