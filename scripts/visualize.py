import argparse
import os

from kaggle_environments import make

def main():
    ap = argparse.ArgumentParser(description="Generate an HTML replay for Orbit Wars.")
    ap.add_argument("--a", default="v2_macro/agent.py", help="Agent A path")
    ap.add_argument("--b", default="starter", help="Agent B path ('starter', 'random', or path)")
    ap.add_argument("--seed", type=int, default=12345, help="Random seed")
    ap.add_argument("--out", default="replay.html", help="Output HTML file")
    args = ap.parse_args()

    print(f"Running match: {args.a} vs {args.b} (seed {args.seed})...")
    env = make("orbit_wars", configuration={"seed": args.seed}, debug=True)
    
    # Load agents (same loading logic Kaggle uses)
    agents = [args.a, args.b]
    
    env.run(agents)
    print("Match complete. Generating HTML...")
    
    html = env.render(mode="html")
    with open(args.out, "w") as f:
        f.write(html)
        
    print(f"Replay saved to: {os.path.abspath(args.out)}")
    print(f"Open this file in your web browser to view the match.")

if __name__ == "__main__":
    main()
