"""Test v1_1.physics, including the same-owner co-arrival stacking rule."""
import os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from v1_1 import physics as ph


def test_resolve_combat_stacking():
    # Test that multiple fleets from the same owner sum together BEFORE combat.
    
    # 1. Stacking attackers overcome defender
    # Planet owned by player 1, garrison 15
    # Player 2 sends two fleets: 10 and 10. They stack to 20.
    # 20 vs 15 -> Player 2 captures, 5 left.
    new_owner, new_garrison = ph.resolve_combat(1, 15, [(2, 10), (2, 10)])
    assert new_owner == 2, f"Expected 2, got {new_owner}"
    assert new_garrison == 5, f"Expected 5, got {new_garrison}"

    # 2. Multi-party combat with same-owner stacking
    # Planet owned by 1, garrison 10
    # Player 2 sends 10 + 5 (stacks to 15)
    # Player 3 sends 10
    # Top two: Player 2 (15) vs Player 3 (10). Survivor: Player 2 with 5.
    # Survivor vs garrison: Player 2 (5) vs Garrison (10).
    # Result: Player 1 keeps it, garrison reduced to 5.
    new_owner, new_garrison = ph.resolve_combat(1, 10, [(2, 10), (2, 5), (3, 10)])
    assert new_owner == 1
    assert new_garrison == 5

    # 3. Stacked attackers tie with another attacker
    # Planet owned by 1, garrison 0
    # Player 2 sends 10
    # Player 3 sends 5 + 5
    # Result: 2 and 3 tie at 10, mutual destruction. Survivor force is 0.
    # Planet remains owner 1, garrison 0.
    new_owner, new_garrison = ph.resolve_combat(1, 0, [(2, 10), (3, 5), (3, 5)])
    assert new_owner == 1
    assert new_garrison == 0

    print("test_v1_1_physics passed (same-owner co-arrival verified)")


if __name__ == "__main__":
    test_resolve_combat_stacking()
