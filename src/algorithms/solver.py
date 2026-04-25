from deap import base, creator, tools
import numpy as np
import random
import pandas as pd
import copy
from src.algorithms.container_filler import ContainerFiller
from src.states.container_state import ContainerState
from src.states.layer_state import LayerState
from src.model.warehouse import Warehouse
from src.model.container import Container
from src.visuals.state_visuals import plot_container_state, plot_layer_state

class Solver:
    def __init__(self, n_pop=20, n_gen=50, n_rep=10, cxpb=0.7, mutpb=0.3, n1=1, n2=1, s_depth=1, s_width=1):
        self.container_filler = ContainerFiller(n1, n2, s_depth, s_width)
        self.n_pop = n_pop
        self.n_gen = n_gen
        self.n_rep = n_rep
        self.cxpb = cxpb
        self.mutpb = mutpb
        self.n1 = n1
        self.n2 = n2
        self.s_depth = s_depth
        self.s_width = s_width

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
        self.logbook.header = ["gen", "nevals"] + self.stats.fields

    def _configure_toolbox(self):
        # Genetic operators' registration
        self.toolbox.register("evaluate", self.evaluate)
        self.toolbox.register("mate", self.crossover)
        self.toolbox.register("mutate", self.mutate)
        self.toolbox.register("select", tools.selBest)

    def evaluate(self, individual):
        # El filling_rate es nuestra base (0.0 a 1.0)
        filling_rate = individual.container.get_filling_rate()
        
        # Área total del contenedor para normalizar
        total_area = individual.container.get_length() * individual.container.get_width()
        penalty = 0
        
        # Recorremos el inventario para ver qué falta
        for piece, (min_demand, current_qty) in individual.warehouse.inventory.items():
            # Calculamos cuántas se han usado comparando con el stock inicial
            # Nota: Asegúrate de que original_inventory esté disponible
            initial_min, initial_max = individual.warehouse.original_inventory.get(piece, (0, 0))
            used = initial_max - current_qty
            
            if used < min_demand:
                missing = min_demand - used
                # Penalización normalizada: (Área de la pieza / Área total)
                # Multiplicamos por 1.5 para que sea una "Hard Constraint"
                piece_area_ratio = (piece.get_area() / total_area)
                penalty += missing * piece_area_ratio * 1.5

        # Ahora el fitness estará en un rango comprensible (ej: 0.8 de llenado - 0.3 de penalización = 0.5)
        return (filling_rate - penalty,)

    def generate_initial_population(self, n_pop, container, warehouse):
        # Calculate the n_pop best containers' states
        states = self.container_filler.fill_container(
            container, 
            warehouse, 
            n_solutions=n_pop
        )
        
        # Convert containers' states to DEAP's individuals
        population = []
        for s in states:
            ind = creator.Individual(
                container=s.get_container(),
                warehouse=s.get_warehouse(),
                s_depth=s.layer_filler.s_depth,
                s_width=s.layer_filler.s_width
            )

            ind.fitness.values = (ind.container.get_filling_rate(),)
            population.append(ind)
            
        return population
    
    def crossover(self, ind1, ind2):
        # Sort the layers acording to their filling rate
        layers = [l for l in ind1.container.get_layers()]
        layers.extend([l for l in ind2.container.get_layers()])
        layers.sort(key=lambda x: x.get_filling_rate(), reverse=True)

        # Initialize the new state's atributes
        new_container = Container(ind1.container.length, ind1.container.width)
        new_warehouse = Warehouse(copy.copy(ind1.warehouse.original_inventory))
        new_state = ContainerState(new_container, new_warehouse, self.s_depth, self.s_width)

        # Add the best layers of the parents
        for layer in layers:
            if new_state.can_add_layer(layer):
                new_state = new_state.add_layer(layer)

        # Complete the solution
        new_state = self.container_filler.fill_container(new_state.get_container(), 
                                                         new_state.get_warehouse())[0]
        
        child = creator.Individual(
            container=new_state.get_container(),
            warehouse=new_state.get_warehouse(),
            s_depth=new_state.layer_filler.s_depth,
            s_width=new_state.layer_filler.s_width
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
        new_state = ContainerState(new_container, new_warehouse, self.s_depth, self.s_width)

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
            s_depth=new_state.layer_filler.s_depth,
            s_width=new_state.layer_filler.s_width
        )

        return child,

    def get_log(self):
        # Extract the columns of the logbook logbook
        gen = self.logbook.select("gen")
        fit_max = self.logbook.select("max")
        fit_avg = self.logbook.select("avg")
        fit_std = self.logbook.select("std")

        df_results = pd.DataFrame({
            "generacion": gen,
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
            # Select the offspring
            offspring = self.toolbox.select(pop, self.n_rep)
            offspring = list(map(copy.deepcopy, offspring))

            while len(offspring) != self.n_pop:
                idxs = random.sample(range(len(offspring)), 2)
                idx1, idx2 = idxs[0], idxs[1]
                if random.random() < self.cxpb:
                    child, _ = self.toolbox.mate(offspring[idx1], offspring[idx2])

                else:
                    idx = idxs[random.randint(0, 1)]
                    child = self.toolbox.mutate(offspring[idx])[0]

                child.fitness.values = self.toolbox.evaluate(child)
                offspring.append(child)

            # Replacement
            pop[:] = offspring

            # Update the statistics
            record = self.stats.compile(pop)
            self.logbook.record(gen=g, nevals=len(pop), **record)
            if g == 0:
                print(self.logbook.header)
            print(self.logbook.stream)

        return tools.selBest(pop, 1)[0]

