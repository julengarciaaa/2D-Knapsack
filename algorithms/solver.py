from deap import base, creator, tools
import random
import copy
from algorithms.container_filler import ContainerFiller
from states.container_state import ContainerState
from model.warehouse import Warehouse
from model.container import Container

class Solver:
    def __init__(self, container, warehouse, n1, n2, s_depth, s_width):
        self.container = container
        self.warehouse = warehouse
        self.container_filler = ContainerFiller(n1, n2, s_depth, s_width)
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

    def _configure_toolbox(self):
        # Genetic operators' registration
        self.toolbox.register("evaluate", self.evaluate)
        self.toolbox.register("mate", self.crossover)
        self.toolbox.register("mutate", self.mutate)
        self.toolbox.register("select", tools.selTournament, tournsize=3)

    def evaluate(self, individual):
        return (individual.container.get_filling_rate(),)

    def generate_initial_population(self, n_pop):
    # Calculate the n_pop best containers' states
        states = self.container_filler.fill_container(
            self.container, 
            self.warehouse, 
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
        new_warehouse = Warehouse(copy.copy(self.warehouse.inventory))
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
        new_warehouse = Warehouse(copy.copy((self.warehouse.inventory)))
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

    def solve(self, npop=20, ngen=50, cxpb=0.7, mutpb=0.3):
        # Generate the initial population
        pop = self.generate_initial_population(npop)

        # Assess the initial population
        fitnesses = list(map(self.toolbox.evaluate, pop))
        for ind, fit in zip(pop, fitnesses):
            ind.fitness.values = fit 
        
        # 2. Ciclo evolutivo
        for g in range(ngen):
            print(f"-- Generación {g} --")
            
            # SELECCIÓN: Elegimos a los padres para la siguiente generación
            # Tournament selection usa el fitness que calculamos en la init
            offspring = self.toolbox.select(pop, len(pop))
            # Clonamos para no modificar los originales accidentalmente
            offspring = list(map(copy.deepcopy, offspring))

            # CRUCE (Mate): Aplicamos cruce a parejas con probabilidad cxpb
            for child1, child2 in zip(offspring[::2], offspring[1::2]):
                if random.random() < cxpb:
                    self.toolbox.mate(child1, child2)
                    # Al cruzarse, el fitness ya no es válido
                    del child1.fitness.values
                    del child2.fitness.values

            # MUTACIÓN: Aplicamos mutación con probabilidad mutpb
            for mutant in offspring:
                if random.random() < mutpb:
                    self.toolbox.mutate(mutant)
                    del mutant.fitness.values

            # RE-EVALUACIÓN: Solo evaluamos a los que han cambiado (fitness inválido)
            invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
            fitnesses = map(self.toolbox.evaluate, invalid_ind)
            for ind, fit in zip(invalid_ind, fitnesses):
                ind.fitness.values = fit

            # REEMPLAZO: La descendencia pasa a ser la nueva población
            pop[:] = offspring

            # Opcional: imprimir el mejor de la generación
            best_ind = tools.selBest(pop, 1)[0]
            print(f"Mejor Fitness: {best_ind.fitness.values[0]:.4f}")

        # Retornamos el mejor individuo de toda la historia
        return tools.selBest(pop, 1)[0]

