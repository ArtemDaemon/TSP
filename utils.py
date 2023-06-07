# END OF SUBSET

def format_steps(steps):
    for i, step_i in enumerate(steps):
        for j, step_j in enumerate(steps):
            if j <= i:
                continue
            if step_j[0] >= step_i[0]:
                step_j[0] += 1
            if step_j[1] >= step_i[1]:
                step_j[1] += 1
