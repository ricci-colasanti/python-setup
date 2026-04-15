import random
import math
import matplotlib.pyplot as plt

# Constants
MEAN_AGE = 40
STD_DEV_AGE = 15
MEAN_POP = 100
STD_DEV_POP = 10
GRID_SIZE = 10
SIMILARITY_THRESHOLD = 0.45
MAX_AGE = 120
MIN_AGE = 0

def init_population(population, grid):
    c_max = len(grid)
    r_max = len(grid[0])
    pop_count = 0
    r = 0
    while r < r_max:
        c = 0
        while c < c_max:
            # Explicit float conversion for safety in other languages
            act_pop = int(random.gauss(MEAN_POP, STD_DEV_POP))
            p = 0
            while p < act_pop:
                age = random.gauss(MEAN_AGE, STD_DEV_AGE)
                if age < MIN_AGE:
                    age = MIN_AGE
                if age > MAX_AGE:
                    age = MAX_AGE
                age = int(age)
                
                # Explicit float division
                threshold = float(r) / float(r_max)
                if random.random() < 0.5:#threshold:
                    person_type = 0
                else:
                    person_type = 1
                
                grid[r][c].append(pop_count)
                population.append([pop_count, person_type, age, r, c])
                pop_count = pop_count + 1
                p = p + 1
            c = c + 1
        r = r + 1

def init_grid(grid, similarity, distance, size):
    row = 0
    while row < size:
        grid.append([])
        similarity.append([])
        distance.append([])
        
        col = 0
        while col < size:
            grid[row].append([])
            similarity[row].append(0.0)
            
            # Initialize distance array with a loop instead of multiplication
            dist_row = []
            k = 0
            while k < size * size:
                dist_row.append(0.0)
                k = k + 1
            distance[row].append(dist_row)
            
            col = col + 1
        row = row + 1

def calc_similarity(grid, population, similarity):
    r_max = len(grid)
    c_max = len(grid[0])
    
    r = 0
    while r < r_max:
        c = 0
        while c < c_max:
            # Reset counts for each cell
            count_t0 = 0
            count_t1 = 0
            
            pop = len(grid[r][c])
            p_idx = 0
            while p_idx < pop:
                p_id = grid[r][c][p_idx]
                if population[p_id][1] == 1:
                    count_t0 = count_t0 + 1
                else:
                    count_t1 = count_t1 + 1
                p_idx = p_idx + 1
            
            # Assign similarity - fixed index order (r,c)
            total = count_t0 + count_t1
            if total > 0:
                similarity[r][c] = float(count_t0) / float(total)
            else:
                similarity[r][c] = 0.0
                
            c = c + 1
        r = r + 1

def inverse_sqr_distance(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    dist_sq = dx * dx + dy * dy
    if dist_sq == 0:
        return 0.0
    return 1.0 / dist_sq

def move(y, x, grid, population, similarity):
    # Calculate roulette wheel weights
    r_max = len(grid)
    c_max = len(grid[0])
    total_weight = 0.0
    weights = []
    
    r = 0
    while r < r_max:
        c = 0
        while c < c_max:
            if y == r and x == c:
                d = 0.0
            else:
                d = inverse_sqr_distance(y, x, r, c)
            weights.append(d)
            total_weight = total_weight + d
            c = c + 1
        r = r + 1
    
    # Normalize to probabilities (roulette wheel)
    roulette_wheel = []
    accumulate = 0.0
    i = 0
    while i < len(weights):
        if total_weight > 0:
            accumulate = accumulate + (weights[i] / total_weight)
        roulette_wheel.append(accumulate)
        i = i + 1
    
    def move_to():
        choice = random.random()
        i = 0
        while i < len(roulette_wheel):
            # Use <= for proper inclusive probability range
            if choice <= roulette_wheel[i]:
                return i // GRID_SIZE, i % GRID_SIZE
            i = i + 1
        return 0, 0  # Fallback (should not happen)
    
    movers = []
    cell_pop = grid[y][x]
    p_idx = 0
    while p_idx < len(cell_pop):
        p = cell_pop[p_idx]
        p_type = population[p][1]
        
        # Use correct index order (y,x)
        sim_val = similarity[y][x]
        
        condition_move = False
        if p_type == 0 and sim_val < SIMILARITY_THRESHOLD:
            condition_move = True
        elif p_type == 1 and (1.0 - sim_val) < SIMILARITY_THRESHOLD:
            condition_move = True
            
        if condition_move:
            nr, nc = move_to()
            # Store the actual index p, not p_id (p is the index)
            movers.append([p, nr, nc])
            
        p_idx = p_idx + 1
        
    return movers

def migrate(grid, population, similarity):
    movers = []
    r_max = len(grid)
    c_max = len(grid[0])
    
    # Collect all movers
    r = 0
    while r < r_max:
        c = 0
        while c < c_max:
            m = move(r, c, grid, population, similarity)
            # Append movers
            i = 0
            while i < len(m):
                movers.append(m[i])
                i = i + 1
            c = c + 1
        r = r + 1
    
    # Execute moves
    i = 0
    while i < len(movers):
        m = movers[i]
        p_id = m[0]  # This is the actual index in population array
        new_r = m[1]
        new_c = m[2]
        
        # Boundary checking
        if new_r < 0 or new_r >= r_max or new_c < 0 or new_c >= c_max:
            i = i + 1
            continue  # Skip invalid moves
        
        p = population[p_id]
        old_r = p[3]
        old_c = p[4]
        
        # Skip if moving to same cell
        if old_r == new_r and old_c == new_c:
            i = i + 1
            continue
        
        # Update population record
        p[3] = new_r
        p[4] = new_c
        
        # Remove from old cell
        old_cell = grid[old_r][old_c]
        j = 0
        found = False
        while j < len(old_cell) and not found:
            if old_cell[j] == p_id:
                # Remove element by shifting remaining elements
                k = j
                while k < len(old_cell) - 1:
                    old_cell[k] = old_cell[k + 1]
                    k = k + 1
                old_cell.pop()  # Remove last element
                found = True
            j = j + 1
        
        # Add to new cell
        grid[new_r][new_c].append(p_id)
        
        i = i + 1
    
    return len(movers)

# Take this on faith - plot the grid
def plot_grid(grid):
    plt.imshow(grid, vmin=0.0, vmax=1.0)
    plt.colorbar()
    plt.show()

def main():
    # Initialize data structures
    grid = []
    similarity = []
    distance = []
    population = []
    
    # Initialize grid and population
    init_grid(grid, similarity, distance, GRID_SIZE)
    init_population(population, grid)
    calc_similarity(grid, population, similarity)
    
    # Plot initial similarity
    print("Initial similarity grid:")
    plot_grid(similarity)
    
    # Run simulation for 600 steps
    print("Running simulation for 600 steps...")
    for t in range(600):
        migrate(grid, population, similarity)
        calc_similarity(grid, population, similarity)
        
        # Optional: Print progress every 100 steps
        if (t + 1) % 100 == 0:
            print(f"Completed step {t + 1}/600")
            plot_grid(similarity)
    
    # Plot final similarity
    print("\nFinal similarity grid:")
    plot_grid(similarity)
    
    # Print summary statistics
    print("\n=== Simulation Summary ===")
    r_max = len(similarity)
    c_max = len(similarity[0])
    total_similarity = 0.0
    cell_count = 0
    
    r = 0
    while r < r_max:
        c = 0
        while c < c_max:
            total_similarity = total_similarity + similarity[r][c]
            cell_count = cell_count + 1
            c = c + 1
        r = r + 1
    
    avg_similarity = total_similarity / float(cell_count)
    print(f"Average similarity across all cells: {avg_similarity:.3f}")
    print(f"Total cells: {cell_count}")

if __name__ == "__main__":
    main()
