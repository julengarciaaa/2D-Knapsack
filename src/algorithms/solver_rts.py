from deap import base, creator, tools
import numpy as np
import random
import pandas as pd
import copy
from src.states.container_state import ContainerState
from src.model.warehouse import Warehouse
from src.model.container import Container
from src.visuals.state_visuals import plot_container_state
import time

class SolverRTS:
    def __init__(self, n_pop, n_gen, n_rep, cxpb, mutpb, container_filler, alpha=1, beta=1):
        self.container_filler = container_filler
        self.n_pop = n_pop
        self.n_gen = n_gen
        self.n_rep = n_rep
        self.cxpb = cxpb
        self.mutpb = mutpb
        self.alpha = alpha
        self.beta = beta

        # Types' configuration
        if not hasattr(creator, "FitnessMax"):
            creator.create("FitnessMax", base.Fitness, weights=(1.0,))
        if not hasattr(creator, "Individual"):
            creator.create("Individual", ContainerState, fitness=creator.FitnessMax)

        # Toolbox initialization
        self.toolbox = base.Toolbox()
        self._configure_toolbox()

        # Create statistics for the individuals
        self.stats = tools.Statistics(key=lambda ind: ind.fitness.values)

        # Define the metrics of interest
        self.stats.register("avg", np.mean)
        self.stats.register("std", np.std)
        self.stats.register("min", np.min)
        self.stats.register("max", np.max)

        self.logbook = tools.Logbook()
        self.logbook.header = ["gen", "nevals", "time_gen"] + self.stats.fields

    def _configure_toolbox(self):
        # Genetic operators' registration
        self.toolbox.register("evaluate", self.evaluate)
        self.toolbox.register("mate", self.crossover)
        self.toolbox.register("mutate", self.mutate)
        self.toolbox.register("select", tools.selBest)

    def evaluate(self, individual):
        # The filling rate is the starting point for calculating the fitness
        filling_rate = individual.container.get_filling_rate()
        
        # Total area for future normalization
        total_area = individual.container.get_length() * individual.container.get_width()
        max_penalty = 0
        penalty = 0

        for piece, (min_demand, max_demand) in individual.warehouse.original_inventory.items():
            max_penalty += min_demand * piece.get_area()
        
        # Iterate through the warehouse to see the left pieces
        for piece, (min_demand, max_demand) in individual.warehouse.inventory.items():
            penalty += min_demand * piece.get_area()

        fitness = self.alpha * filling_rate - self.beta * (penalty / max_penalty)

        return (fitness,)

    def generate_initial_population(self, n_pop, container, warehouse):
        population = []

        for i in range(n_pop):
            state = self.container_filler.fill_container(
            container, 
            warehouse)[0]

            ind = creator.Individual(
                container=state.get_container(),
                warehouse=state.get_warehouse(),
                layer_filler=self.container_filler.layer_filler
            )

            ind.fitness.values = (ind.container.get_filling_rate(),)
            population.append(ind)
            
        return population
    
    def crossover(self, ind1, ind2):
        # Sort the layers acording to their filling rate
        layers = [l for l in ind1.container.get_layers()]
        layers.extend([l for l in ind2.container.get_layers()])
        layers.sort(key=lambda x: x.get_filling_rate(), reverse=True)

        # Calculate the number of layers to copy to the new solution (at most 50% of them)
        max_layers = max(1, len(layers) // 2) 
        n_layers = random.randint(0, max_layers)

        # Initialize the new state's atributes
        new_container = Container(ind1.container.length, ind1.container.width)
        new_warehouse = Warehouse(copy.copy(ind1.warehouse.original_inventory))
        new_state = ContainerState(new_container, new_warehouse, self.container_filler.layer_filler)

        # Add the best layers of the parents
        for layer in layers:
            if new_state.can_add_layer(layer):
                new_state = new_state.add_layer(layer)
            if len(new_state.container.layers) == n_layers:
                break

        # Complete the solution
        new_state = self.container_filler.fill_container(new_state.get_container(), 
                                                         new_state.get_warehouse())[0]
        
        child = creator.Individual(
            container=new_state.get_container(),
            warehouse=new_state.get_warehouse(),
            layer_filler=self.container_filler.layer_filler
        )

        return child, child

    def mutate(self, individual):
        # Sort the layers acording to their filling rate
        layers = [l for l in individual.container.get_layers()]
        layers.sort(key=lambda x: x.get_filling_rate(), reverse=True)

        # Calculate the number of layers to copy to the new solution (at most 50% of them)
        max_layers = max(1, len(layers) // 2) 
        n_layers = random.randint(0, max_layers)

        # Initialize the new state's atributes
        new_container = Container(individual.container.length, individual.container.width)
        new_warehouse = Warehouse(copy.copy((individual.warehouse.original_inventory)))
        new_state = ContainerState(new_container, new_warehouse, self.container_filler.layer_filler)

        # Add the best n_layers layers of the parent
        placed_layers = 0
        for layer in layers:
            if new_state.can_add_layer(layer):
                new_state = new_state.add_layer(layer)
                placed_layers += 1

                if placed_layers == n_layers:
                    break

        # Complete the solution
        new_state = self.container_filler.fill_container(new_state.get_container(), 
                                                         new_state.get_warehouse())[0]
        
        child = creator.Individual(
            container=new_state.get_container(),
            warehouse=new_state.get_warehouse(),
            layer_filler=self.container_filler.layer_filler
        )

        return child,

    def get_log(self):
        # Extract the columns of the logbook logbook
        gen = self.logbook.select("gen")
        fit_max = self.logbook.select("max")
        fit_avg = self.logbook.select("avg")
        fit_std = self.logbook.select("std")

        df_results = pd.DataFrame({
            "generation": gen,
            "max_fitness": fit_max,
            "avg_fitness": fit_avg,
            "std_dev": fit_std
        })

        return df_results

    def solve(self, container, warehouse):
        # Generate the initial population
        pop = self.generate_initial_population(self.n_pop, container, warehouse)

        # Assess the initial population
        fitnesses = list(map(self.toolbox.evaluate, pop))
        for ind, fit in zip(pop, fitnesses):
            ind.fitness.values = fit 
        
        # Evolutive cycle
        for g in range(self.n_gen):
            start_gen = time.time()
            # Select the offspring
            offspring = self.toolbox.select(pop, self.n_rep)
            offspring = list(map(copy.deepcopy, offspring))

            while len(offspring) != self.n_pop:
                if len(offspring) >= 2:
                    idxs = random.sample(range(len(offspring)), 2)
                    idx1, idx2 = idxs[0], idxs[1]
                    if random.random() < self.cxpb:
                        child, _ = self.toolbox.mate(offspring[idx1], offspring[idx2])

                    else:
                        idx = idxs[random.randint(0, 1)]
                        child = self.toolbox.mutate(offspring[idx])[0]
                else:
                    child = self.toolbox.mutate(offspring[0])[0]

                child.fitness.values = self.toolbox.evaluate(child)
                offspring.append(child)

            # Replacement
            pop[:] = offspring

            end_gen = time.time()
            duration_gen = end_gen - start_gen

            # Update the statistics
            record = self.stats.compile(pop)
            self.logbook.record(gen=g, nevals=len(pop), time_gen=duration_gen, **record)

            df_log = pd.DataFrame(self.logbook)
            
        return tools.selBest(pop, 1)[0], df_log

