# Define Events

events = ["Burglary", "Earthquake", "Alarm", "JohnCalls", "MaryCalls"]
print("\nEvents in the network:", events)

# Store Conditional Probability Tables (CPTs)
prob_burglary = {"True": 0.001, "False": 0.999}
prob_earthquake = {"True": 0.002, "False": 0.998}
prob_alarm = {
    ("True", "True"): {"True": 0.95, "False": 0.05},
    ("True", "False"): {"True": 0.94, "False": 0.06},
    ("False", "True"): {"True": 0.29, "False": 0.71},
    ("False", "False"): {"True": 0.001, "False": 0.999}
}

prob_john_calls = {
    "True": {"True": 0.90, "False": 0.10},
    "False": {"True": 0.05, "False": 0.95}
}

prob_mary_calls = {
    "True": {"True": 0.70, "False": 0.30},
    "False": {"True": 0.01, "False": 0.99}
}

cpts = {
    "Burglary": prob_burglary,
    "Earthquake": prob_earthquake,
    "Alarm": prob_alarm,
    "JohnCalls": prob_john_calls,
    "MaryCalls": prob_mary_calls,
}

print("\nConditional Probability Tables (CPTs):")
for event, cpt in cpts.items():
    print(f"\nCPT for {event}:")
    print(cpt)

# Function to calculate full joint probability
def calculate_joint_probability(b, e, a, j, m):
    p_b = cpts["Burglary"][str(b)]
    p_e = cpts["Earthquake"][str(e)]
    p_a_given_be = cpts["Alarm"][(str(b), str(e))][str(a)]
    p_j_given_a = cpts["JohnCalls"][str(a)][str(j)]
    p_m_given_a = cpts["MaryCalls"][str(a)][str(m)]
    return p_m_given_a * p_j_given_a * p_a_given_be * p_e * p_b

# Query processor
def query_joint_distribution(query):
    if not all(event in query for event in events):
        print("Error: Query must specify the state for all events.")
        return None

    b = query["Burglary"]
    e = query["Earthquake"]
    a = query["Alarm"]
    j = query["JohnCalls"]
    m = query["MaryCalls"]
    return calculate_joint_probability(b, e, a, j, m)

# Query a
query_a = {
    "Burglary": False,
    "Earthquake": False,
    "Alarm": True,
    "JohnCalls": True,
    "MaryCalls": True
}
probability_a = query_joint_distribution(query_a)

print("\n--- Query Results ---")
print(f"Probability (A=True, B=False, E=False, J=True, M=True): {probability_a:.8f}")

# Additional Queries
query_1 = {"Burglary": True, "Earthquake": True, "Alarm": True, "JohnCalls": True, "MaryCalls": True}
query_2 = {"Burglary": False, "Earthquake": False, "Alarm": False, "JohnCalls": False, "MaryCalls": False}
query_3 = {"Burglary": True, "Earthquake": False, "Alarm": True, "JohnCalls": False, "MaryCalls": True}
query_4 = {"Burglary": False, "Earthquake": True, "Alarm": False, "JohnCalls": True, "MaryCalls": False}
query_5 = {"Burglary": False, "Earthquake": False, "Alarm": True, "JohnCalls": False, "MaryCalls": False}

probability_1 = query_joint_distribution(query_1)
probability_2 = query_joint_distribution(query_2)
probability_3 = query_joint_distribution(query_3)
probability_4 = query_joint_distribution(query_4)
probability_5 = query_joint_distribution(query_5)

print(f"Probability (B=True, E=True, A=True, J=True, M=True): {probability_1:.8f}")
print(f"Probability (B=False, E=False, A=False, J=False, M=False): {probability_2:.8f}")
print(f"Probability (B=True, E=False, A=True, J=False, M=True): {probability_3:.8f}")
print(f"Probability (B=False, E=True, A=False, J=True, M=False): {probability_4:.8f}")
print(f"Probability (B=False, E=False, A=True, J=False, M=False): {probability_5:.8f}")

