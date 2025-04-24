class BlockWorldPlanner:
    def __init__(self, initial_state, goal_state):
        self.initial_state = initial_state
        self.goal_state = goal_state
        self.plan = []

    def print_state(self, state):
        stacks = self.get_stacks(state)
        max_height = max(len(s) for s in stacks)
        print("\nCurrent State:")
        for level in range(max_height - 1, -1, -1):
            row = ""
            for stack in stacks:
                if level < len(stack):
                    row += f"  {stack[level]}  "
                else:
                    row += "     "
            print(row)
        print("-" * (5 * len(stacks)))

    def get_stacks(self, state):
        above = {}
        for block, pos in state.items():
            if pos != "Table":
                above.setdefault(pos, []).append(block)

        roots = [b for b, p in state.items() if p == "Table"]
        stacks = []
        for root in roots:
            stack = [root]
            current = root
            while current in above:
                current = above[current][0]
                stack.append(current)
            stacks.append(stack)
        return stacks

    def is_clear(self, block, state):
        return all(v != block for v in state.values())

    def move_block(self, block, destination, state, step_count):
        if not self.is_clear(block, state):
            top = next(k for k, v in state.items() if v == block)
            print(f"\nStep {step_count}: Move {top} from {block} to Table")
            self.plan.append(f"Step {step_count}: Move {top} from {block} to Table")
            state[top] = "Table"
            self.print_state(state)
            step_count += 1
            step_count = self.move_block(block, destination, state, step_count)
        if state[block] != destination:
            print(f"\nStep {step_count}: Move {block} to {destination}")
            self.plan.append(f"Step {step_count}: Move {block} to {destination}")
            state[block] = destination
            self.print_state(state)
            step_count += 1
        return step_count

    def generate_plan(self):
        print("\nInitial Configuration:")
        self.print_state(self.initial_state)
        state = self.initial_state.copy()
        step = 1

        # Build goal stack from bottom to top
        goal_stack = []
        bottom = next(b for b, p in self.goal_state.items() if p == "Table")
        goal_stack.append(bottom)
        while True:
            next_block = next((b for b, p in self.goal_state.items() if p == bottom), None)
            if not next_block:
                break
            goal_stack.append(next_block)
            bottom = next_block

        for i in range(len(goal_stack)):
            block = goal_stack[i]
            destination = self.goal_state[block]
            step = self.move_block(block, destination, state, step)

        print("\nGoal state achieved!")

    def display_plan(self):
        print("\nFinal Plan:")
        for step in self.plan:
            print(step)


# ------------------------------
# Take user input
# ------------------------------
initial_state = {}
goal_state = {}

num = int(input("Enter number of blocks: "))
print("Enter initial state (format: Block Position):")
for _ in range(num):
    block, pos = input().split()
    initial_state[block] = pos

print("Enter goal state (format: Block Position):")
for _ in range(num):
    block, pos = input().split()
    goal_state[block] = pos

# Execute
planner = BlockWorldPlanner(initial_state, goal_state)
planner.generate_plan()
planner.display_plan()

