

def reduce_chain(chain, remove='@'):

    stack = []

    upper = remove.upper()
    for c in chain:

        if c in {remove, upper}:
            continue

        if not stack:
            stack.append(c)
            continue

        lower_upper = c.islower() != stack[-1].islower()
        reaction = lower_upper and stack[-1].lower() == c.lower()
        if reaction:
            stack.pop()
        else:
            stack.append(c)

    return stack


with open('input_data') as in_f:
    data = next(in_f)

initial_size = len(reduce_chain(data))

polymers = (chr(p) for p in range(97, 123))

smaller_size = min(len(reduce_chain(data, remove=p)) for p in polymers)

print(f'P5-1: {initial_size}')
print(f'P5-2: {smaller_size}')
