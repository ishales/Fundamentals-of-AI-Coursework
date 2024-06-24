##############
# Homework 3 #
##############

# Exercise: Fill this function.
# Returns the index of the variable that corresponds to the fact that
# "Node n gets Color c" when there are k possible colors
def node2var(n, c, k):
    var_ind = (n - 1) * k
    var_ind += c
    return var_ind

# Exercise: Fill this function
# Returns *a clause* for the constraint:
# "Node n gets at least one color from the set {1, 2, ..., k}"
def at_least_one_color(n, k):

    least_clause = []
    
    for c in range(1, k+1):
        curr_ind = node2var(n, c, k)
        least_clause.append(curr_ind)
    
    return least_clause

# Exercise: Fill this function
# Returns *a list of clauses* for the constraint:
# "Node n gets at most one color from the set {1, 2, ..., k}"
def at_most_one_color(n, k):

    most_clauses = []

    most_clauses.append(at_least_one_color(n, k))

    for c in range (1, k+1):

        for x in range(c+1, k+1):
            curr = []
            curr.append(-(node2var(n,c,k)))
            curr.append(-(node2var(n,x,k)))
            most_clauses.append(curr)

    return most_clauses

# Exercise: Fill this function
# Returns *a list of clauses* for the constraint:
# "Node n gets exactly one color from the set {1, 2, ..., k}"
def generate_node_clauses(n, k):

    node_c = at_most_one_color(n, k)

    return node_c
    

# Exercise: Fill this function
# Returns *a list of clauses* for the constraint:
# "Nodes connected by an edge e (represented by a list)
# cannot have the same color"
def generate_edge_clauses(e, k):

    node1, node2 = e
    cons = []

    for c in range(1, k+1):
        var1 = node2var(node1, c, k)
        var2 = node2var(node2, c, k)
        curr = [-(var1), -(var2)]
        cons.append(curr)

    return cons

# The function below converts a graph coloring problem to SAT
# DO NOT MODIFY
def graph_coloring_to_sat(graph_fl, sat_fl, k):
    clauses = []
    with open(graph_fl) as graph_fp:
        node_count, edge_count = tuple(map(int, graph_fp.readline().split()))
        for n in range(1, node_count + 1):
            clauses += generate_node_clauses(n, k)
        for _ in range(edge_count):
            e = tuple(map(int, graph_fp.readline().split()))
            clauses += generate_edge_clauses(e, k)
    var_count = node_count * k
    clause_count = len(clauses)
    with open(sat_fl, 'w') as sat_fp:
        sat_fp.write("p cnf %d %d\n" % (var_count, clause_count))
        for clause in clauses:
            sat_fp.write(" ".join(map(str, clause)) + " 0\n")

sat_fl = "o2_15c.txt"
graph_fl = "graph2.txt"
graph_coloring_to_sat(graph_fl, sat_fl, 15)

# Example function call
# if __name__ == "__main__":
#    graph_coloring_to_sat("graph1.txt", "graph1_3colors.txt", 3)
