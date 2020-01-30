
def choice_sort(array, item):
    result = []

    if item is not None:
        index_of_elm = array.index(item)

        if index_of_elm > 0:
            array.insert(0, array.pop(index_of_elm))

    result = array

    for i, elm in enumerate(result):
        result[i] = (i, elm)

    return result
