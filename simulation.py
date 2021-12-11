from virus import Virus
from logger import Logger
from person import Person
import random
import sys
random.seed(42)


class Simulation(object):
    ''' Main class that will run the herd immunity simulation program.
    Expects initialization parameters passed as command line arguments when file is run.

    Simulates the spread of a virus through a given population.  The percentage of the
    population that are vaccinated, the size of the population, and the amount of initially
    infected people in a population are all variables that can be set when the program is run.
    '''

    def __init__(self, virus, pop_size, vaccinated_amount, initial_infected=1):
        ''' Logger object logger records all events during the simulation.
        Population represents all Persons in the population.
        The next_person_id is the next available id for all created Persons,
        and should have a unique _id value.
        The vaccination percentage represents the total percentage of population
        vaccinated at the start of the simulation.
        You will need to keep track of the number of people currently infected with the disease.
        The total infected people is the running total that have been infected since the
        simulation began, including the currently infected people who died.
        You will also need to keep track of the number of people that have die as a result
        of the infection.

        All arguments will be passed as command-line arguments when the file is run.
        HINT: Look in the if __name__ == "__main__" function at the bottom.
        '''
        self.pop_size = pop_size
        self.next_person_id = 0
        self.virus = virus  # Virus object
        self.initial_infected = initial_infected  # Int
        self.total_infected = self.initial_infected  # Int
        self.vaccinated_amount = vaccinated_amount  # float between 0 and 1
        self.total_dead = self.initial_infected  # Int
        self.logger = Logger(
            f"{virus.name}_simulation_pop_{pop_size}_vp_{vaccinated_amount}_infected_{initial_infected}.txt")
        self.newly_infected = []
        self.population = []  # List of Person objects
        self.time_step_counter = 0
        self.should_continue = True
        self._create_population()

    def _create_population(self):
        '''This method will create the initial population.
            Args:
                initial_infected (int): The number of infected people that the simulation
                will begin with.
            Returns:
                list: A list of Person objects.
        '''
        # infected people
        for _ in range(self.initial_infected):
            self.next_person_id += 1
            person = Person(self.next_person_id, False, virus)
            self.population.append(person)
        # # of vaccinated people
        for _ in range(self.vaccinated_amount):
            self.next_person_id += 1
            person = Person(self.next_person_id, True, None)
            self.population.append(person)
        # unvaccinated healthy people
        for _ in range(self.pop_size - initial_infected - vaccinated_amount):
            self.next_person_id += 1
            person = Person(self.next_person_id, False, None)
            self.population.append(person)

    def _simulation_should_continue(self):
        ''' The simulation should only end if the entire population is dead
        or everyone is vaccinated.
            Returns:
                bool: True for simulation should continue, False if it should end.
        '''
        if self.total_dead >= self.pop_size - self.vaccinated_amount:
            return False
        else:
            return True

    def run(self):
        ''' This method should run the simulation until all requirements for ending
        the simulation are met.
        '''
        self.logger.write_metadata(self.pop_size, self.vaccinated_amount, self.virus.name, self.virus.mortality_rate, self.virus.repro_rate)

        while self.should_continue:
            # for every iteration of this loop, call self.time_step() to compute another round of this simulation.
            self.time_step()
            self._infect_newly_infected()
            self.time_step_counter += 1
            self.should_continue = self._simulation_should_continue()
            if self.should_continue == False:
                self.logger.log_time_step(
                    self.time_step_counter, self.total_infected, self.total_dead, False)
                print(
                    f"The simulation has ended after {self.time_step_counter} turns.")
                print(f"The total population is {self.pop_size}.")
                print(f"The total infected people is {self.total_infected}.")
                print(
                    f"The total vaccinated people is {self.vaccinated_amount}.")
                print(f"The total dead people is {self.total_dead}.")
                print(
                    f"The total unvaccinated people is {self.pop_size - self.vaccinated_amount}.")
            else:
                self.logger.log_time_step(
                    self.time_step_counter, self.total_infected, self.total_dead, True)

    def time_step(self):
        ''' This method should contain all the logic for computing one time step
        in the simulation.

        This includes:
            1. 100 total interactions with a random person for each infected person
                in the population
            2. If the person is dead, grab another random person from the population.
                Since we don't interact with dead people, this does not count as an interaction.
            3. Otherwise call simulation.interaction(person, random_person) and
                increment interaction counter by 1.
            '''
        # find all infected people and place in a list
        infected_people = []
        # for person in population
        for person in self.population:
            # if person has infection
            if person.infection:
                # append person to infected list
                infected_people.append(person)

        # create empty list of newly infected
        newly_infected = []
        # loop over infected people
        for infected_person in infected_people:
            for _ in range(self.pop_size):
                # assign random person to variable
                # random_person = self.population[random.randint(self.pop_size)]
                random_person = random.choice(self.population)
                if random_person.is_alive == False:
                    continue
                # if random person is sick
                elif random_person.infection:
                    self.logger.log_interaction(
                        infected_person, random_person, random_person_sick=True)
                # if random person is vaccinated
                elif random_person.is_vaccinated:
                    self.logger.log_interaction(
                        infected_person, random_person, random_person_vacc=True)
                # else: if person is alive and not vaccinated
                else:
                    # check if random person caught virus
                    if infected_person.infection.repro_rate > random.random():
                        # give random person the virus
                        random_person.infection = infected_person.infection
                        self.logger.log_interaction(
                            infected_person, random_person, did_infect=True)
                        # append to newly enfected list
                        newly_infected.append(random_person)

        # return list of new infections
        self.newly_infected = newly_infected

    def _infect_newly_infected(self):
        ''' This method should iterate through the list of ._id stored in self.newly_infected
        and update each Person object with the disease. '''
        # TODO: Call this method at the end of every time step and infect each Person.
        # TODO: Once you have iterated through the entire list of self.newly_infected, remember
        # to reset self.newly_infected back to an empty list.

        for infected_person in self.newly_infected:
            for person in self.population:
                if infected_person._id == person._id:
                    person.infection = infected_person.infection

        # reset to empty list
        self.newly_infected = []
        infect_num = 0
        dead_num = 0
        for person in self.population:
            if person.is_alive == False:
                dead_num += 1
            else:
                if person.infection:
                    survived = person.did_survive_infection()
                    if not survived:
                        dead_num += 1
                        self.logger.log_infection_survival(person, True)
                    else:
                        infect_num += 1
                        self.logger.log_infection_survival(person, False)
        self.total_dead = dead_num
        self.total_infected = infect_num


if __name__ == "__main__":
    pop_size = 100
    vaccinated_amount = 10
    initial_infected = 5

    virus = Virus("HIV", 0.8, 0.3)
    sim = Simulation(virus, pop_size, vaccinated_amount, initial_infected)

    sim.run()
