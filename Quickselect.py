def quickselect(A, k = int):
    #A is an array, wherein we want to find the K - th largest element
    # in the weak sense [1 ≤ K ≤ length(A)]

    if len(A) == 1:
        return A[0]

    pivot = A[-1]
    left = [x for x in A if x > pivot]   # elements larger than pivot
    right = [x for x in A if x <= pivot] # elements smaller or to equal
    right.remove(pivot) #removes an instance of the pivot from ‘right’

    if k <= len(left):
        return quickselect(left, k)
    elif k == len(left) + 1:
        return pivot
    else:
        return quickselect(right, ((k - len(left)) - 1))

def randomized_quickselect(A, k = int): 
    # A variation of the quickselect algorithm with randomized pivot selection
    if len(A) == 1:
        return A[0]

    pivot = A[random.randint(1, len(A)-1)] # random selection of pivot
    left = [x for x in A if x > pivot]  # elements larger than pivot
    right = [x for x in A if x <= pivot] # elements smaller or to equal
    right.remove(pivot) #removes an instance of the pivot from ‘right’
    if k <= len(left):
        return randomized_quickselect(left, k)
    elif k == len(left) + 1:
        return pivot
    else:
        return randomized_quickselect(right, ((k - len(left)) - 1))

A = [81, 2, 25, 33, 69, 39, 42, 17, 62, 15]
k = 5
result = quickselect(A, k)
print(f"The {k}-th largest element is {result}")

