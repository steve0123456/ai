class VacuumCleanerWorld:
    def __init__(self, left_state, right_state, position):
        # Initializing the environment state
        self.left_state = left_state  # True = dirty, False = clean
        self.right_state = right_state  # True = dirty, False = clean
        self.position = position  # "left" or "right"
        self.path_cost = 0  # The cost of the path (1 for each transition)

    def is_goal_state(self):
        # Goal state is when both left and right states are clean
        return self.left_state == False and self.right_state == False

    def successors(self):
        # Generate all possible successor states
        successors = []

        if self.position == 'left' and self.left_state:
            new_state = VacuumCleanerWorld(False, self.right_state, 'left')
            new_state.path_cost = self.path_cost + 1
            successors.append(("Suck", new_state))

        elif self.position == 'left' and not self.left_state:
            if not self.right_state:
                new_state = VacuumCleanerWorld(self.left_state, self.right_state, 'left')
                new_state.path_cost = self.path_cost
                successors.append(("Exit", new_state))
            else:
                new_state = VacuumCleanerWorld(self.left_state, self.right_state, 'right')
                new_state.path_cost = self.path_cost
                successors.append(("Move Right", new_state))

        if self.position == 'right' and self.right_state:
            new_state = VacuumCleanerWorld(self.left_state, False, 'right')
            new_state.path_cost = self.path_cost + 1
            successors.append(("Suck", new_state))

        elif self.position == 'right' and not self.right_state:
            if not self.left_state:
                new_state = VacuumCleanerWorld(self.left_state, self.right_state, 'right')
                new_state.path_cost = self.path_cost
                successors.append(("Exit", new_state))
            else:
                new_state = VacuumCleanerWorld(self.left_state, self.right_state, 'left')
                new_state.path_cost = self.path_cost
                successors.append(("Move Left", new_state))

        return successors

    def __str__(self):
        return f"Position: {self.position}, Left Dirty: {self.left_state}, Right Dirty: {self.right_state}, Cost: {self.path_cost}"


def display_menu():
    print("\n--- Vacuum Cleaner World ---")
    print("1. Set Initial States")
    print("2. Run Reflex Agent")
    print("3. Exit")


def set_initial_states():
    print("\nEnter the initial states of the environment:")

    left_dirty = input("Is the left state dirty? (y/n): ").lower()
    left_state = True if left_dirty == 'y' else False

    right_dirty = input("Is the right state dirty? (y/n): ").lower()
    right_state = True if right_dirty == 'y' else False

    position = input("Where is the vacuum cleaner? (left/right): ").lower()

    return left_state, right_state, position


def run_reflex_agent(left_state, right_state, position):
    current_state = VacuumCleanerWorld(left_state, right_state, position)
    print(f"\nInitial State: {current_state}")

    while not current_state.is_goal_state():
        successors = current_state.successors()
        print("\nSuccessor States:")
        for action, successor in successors:
            print(f"Action: {action} -> {successor}")
        current_state = successors[0][1]

    print("\nGoal State Reached!")
    print(f"Final State: {current_state}")


def main():
    left_state = None
    right_state = None
    position = None

    while True:
        display_menu()
        choice = input("Enter your choice: ").strip()

        if choice == '1':
            left_state, right_state, position = set_initial_states()
        elif choice == '2':
            if left_state is None or right_state is None or position is None:
                print("Please set the initial states first!")
            else:
                run_reflex_agent(left_state, right_state, position)
        elif choice == '3':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
