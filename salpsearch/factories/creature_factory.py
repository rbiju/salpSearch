from abc import ABC
import hydra

from salpsearch.creatures import Creature


class CreatureFactory(ABC):
    def __init__(self):
        pass

    def make_creature(self) -> Creature:
        pass


class SalpFactory(CreatureFactory):
    def __init__(self):
        super().__init__()

    @hydra.main(config_path='conf/salp', config_name='default')
    def make_creature(self):
        pass
