#!/usr/bin/env python3
"""
Minimaler Isaac-Sim Starter fuer den eingebauten Unitree A1.

Nutzen:
- Laedt den mitgelieferten Unitree-A1-Asset aus Isaac Sim
- Erstellt eine Ground Plane
- Spawned den Roboter unter /World/A1
- Optional headless

Die Isaac-Sim-Asset-Doku nennt fuer den A1 den Pfad:
Robots/Unitree/A1/a1.usd
und beschreibt den A1 als Teil der Quadruped-Beispiele.
"""

import argparse


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument('--headless', action='store_true', help='Ohne GUI starten')
    p.add_argument('--prim-path', type=str, default='/World/A1', help='Prim-Pfad des Roboters')
    p.add_argument('--steps', type=int, default=1000, help='Anzahl der Simulationsschritte')
    p.add_argument('--physics-dt', type=float, default=1/200)
    p.add_argument('--render-dt', type=float, default=1/60)
    return p.parse_args()


def main():
    args = parse_args()

    from isaacsim import SimulationApp
    simulation_app = SimulationApp({'headless': args.headless})

    from isaacsim.storage.native import get_assets_root_path
    from omni.isaac.core import World
    from omni.isaac.core.utils.stage import add_reference_to_stage
    from omni.isaac.core.utils.prims import get_prim_at_path
    from omni.isaac.core.articulations import Articulation

    assets_root = get_assets_root_path()
    if assets_root is None:
        raise RuntimeError('Isaac-Sim-Assets konnten nicht gefunden werden.')

    a1_usd = assets_root + '/Isaac/Robots/Unitree/A1/a1.usd'

    world = World(stage_units_in_meters=1.0, physics_dt=args.physics_dt, rendering_dt=args.render_dt)
    world.scene.add_default_ground_plane()

    add_reference_to_stage(usd_path=a1_usd, prim_path=args.prim_path)
    prim = get_prim_at_path(args.prim_path)
    if not prim.IsValid():
        raise RuntimeError(f'A1-Prim konnte nicht geladen werden: {args.prim_path}')

    robot = Articulation(prim_path=args.prim_path, name='unitree_a1')
    world.scene.add(robot)
    world.reset()

    print('Loaded Unitree A1 from:', a1_usd)
    print('Robot prim path:', args.prim_path)
    print('DOFs:', robot.num_dof)

    for _ in range(args.steps):
        world.step(render=not args.headless)

    simulation_app.close()


if __name__ == '__main__':
    main()
