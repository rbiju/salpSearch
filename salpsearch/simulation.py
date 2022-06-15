from creature_chains import CreatureChain


class Simulation:
    def __init__(self, creature_chain: CreatureChain, **kwargs):
        self.creature_chain = creature_chain

        self.space = self.creature_chain.creature.physics_handler.space
        self.concentration_space = self.creature_chain.creature.concentration_handler.concentration_space

        self.fps = kwargs['fps']
        self.dt = 1 / self.fps
        self.max_time = kwargs['max_time']

    def run(self):
        frame_counter = 0
        t = 0

        while t < self.max_time:
            t = self.dt * frame_counter
            self.creature_chain.run_chain()

            frame_counter += 1
            self.concentration_space.step(self.dt)
            self.space.step(self.dt)
