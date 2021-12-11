class Logger(object):
    ''' Utility class responsible for logging all interactions during the simulation. '''
    # TODO: Write a test suite for this class to make sure each method is working
    # as expected.

    # PROTIP: Write your tests before you solve each function, that way you can
    # test them one by one as you write your class.

    def __init__(self, file_name):
        # TODO:  Finish this initialization method. The file_name passed should be the
        # full file name of the file that the logs will be written to.
        self.file_name = file_name

    def write_metadata(self, pop_size, vaccinated_amount, virus_name, mortality_rate, repro_rate):
        '''
        The simulation class should use this method immediately to log the specific
        parameters of the simulation as the first line of the file.
        '''
        # TODO: Finish this method. This line of metadata should be tab-delimited
        # it should create the text file that we will store all logs in.
        # TIP: Use 'w' mode when you open the file. For all other methods, use
        # the 'a' mode to append a new log to the end, since 'w' overwrites the file.
        # NOTE: Make sure to end every line with a '/n' character to ensure that each
        # event logged ends up on a separate line!
        with open(self.file_name, 'w') as f:
            f.write(f"Population size: {pop_size}\n")
            f.write(f"Vaccinated amount: {vaccinated_amount}\n")
            f.write(f"Virus name: {virus_name}\n")
            f.write(f"Mortality rate: {mortality_rate}\n")
            f.write(f"Reproduction rate: {repro_rate}\n")
            f.write(f"==================================\n")

    def log_interaction(self, person, random_person, random_person_sick=None, random_person_vacc=None, did_infect=None):
        '''
        The Simulation object should use this method to log every interaction
        a sick person has during each time step.

        The format of the log should be: "{person.ID} infects {random_person.ID} \n"

        or the other edge cases:
            "{person.ID} didn't infect {random_person.ID} because {'vaccinated' or 'already sick'} \n"
        '''
        # TODO: Finish this method. Think about how the booleans passed (or not passed)
        # represent all the possible edge cases. Use the values passed along with each person,
        # along with whether they are sick or vaccinated when they interact to determine
        # exactly what happened in the interaction and create a String, and write to your logfile.
        with open(self.file_name, 'a') as f:
            if random_person_sick:
                f.write(
                    f"{person._id} didn't infect {random_person._id} because he/she is already sick.\n")
            elif random_person_vacc:
                f.write(
                    f"{person._id} didn't infect {random_person._id} because he/she is already vaccinated.\n")
            elif did_infect:
                f.write(f"{person._id} infects {random_person._id}\n")

    def log_infection_survival(self, person, did_die_from_infection):
        ''' The Simulation object uses this method to log the results of every
        call of a Person object's .resolve_infection() method.

        The format of the log should be:
            "{person.ID} died from infection\n" or "{person.ID} survived infection.\n"
        '''
        # TODO: Finish this method. If the person survives, did_die_from_infection
        # should be False.  Otherwise, did_die_from_infection should be True.
        # Append the results of the infection to the logfile
        with open(self.file_name, 'a') as f:
            if did_die_from_infection:
                f.write(f"{person._id} died from infection\n")
            else:
                f.write(f"{person._id} survived infection\n")

    def log_time_step(self, time_step_number, total_infected, total_dead, conti):
        ''' STRETCH CHALLENGE DETAILS:

        If you choose to extend this method, the format of the summary statistics logged
        are up to you.

        At minimum, it should contain:
            The number of people that were infected during this specific time step.
            The number of people that died on this specific time step.
            The total number of people infected in the population, including the newly infected
            The total number of dead, including those that died during this time step.

        The format of this log should be:
            "Time step {time_step_number} ended, beginning {time_step_number + 1}\n"
        '''
        # TODO: Finish this method. This method should log when a time step ends, and a
        # new one begins.
        # NOTE: Here is an opportunity for a stretch challenge!
        with open(self.file_name, 'a') as f:
            f.write(f"==================================\n")
            f.write(f"Total Dead: {total_dead}\n")
            f.write(f"Total Infected: {total_infected}\n")
            if conti:
                f.write(
                    f"Time step {time_step_number} ended, beginning {time_step_number+1}\n")
            else:
                f.write(
                    f"Time step {time_step_number} ended, no more time steps\n")
            f.write(f"==================================\n")
