def create_decision_tree(data, attributes, target_attr, fitness_func):
    """
    Returns a new decision tree based on the examples given.
    """
    data = data[:]
    vals = [record[target_attr] for record in data]
    default = majority_value(data, target_attr)

    # If the dataset is empty or the attrributes list is empty, return the default
    # value. When checking attributes list for emptiness, we need to subtract i
    # to account for the target attribute.
    if not data or len(attributes) - 1 <= 0:
        return default
    # If all the records in the dataset have the same classification return that
    # classification
    elif vals.count(vals[0]) == len(vals):
        return vals[0]
    else:
        # Choose the best attribute to classify our data
        best = choose_attribute(data, attributes, target_attr, fitness_func)
        
        # Create a new decision tree/node with the best and attributes and an empty
        # dictionary object -- we'll fill it up next
        tree = {best: {}}

        # Create a new decision tree/sub-node for each of the values in the best
        # attribute field
        for val in get_values(data, best):
            # Create  a subtree for the current value under the 'best' field
            subtree = create_decision_tree(
                get_examples(data, best, val),
                [attr for attr in attributes if attr != best],
                target_attr,
                fitness_func)

            # Add the new subtree to the empty dictionary object in our new tree/node
            # we just created
            tree[best][val] = subtree
    return tree

def entropy(data, target_attr):
    """
    Calculates the entropy of the given data set for the target attribute.
    """
    val_freq     = {}
    data_entropy = 0.0

    # Calculate the frequency of each of the values in the target attr
    for record in data:
        if (val_freq.has_key(record[target_attr])):
            val_freq[record[target_attr]] += 1.0
        else:
            val_freq[record[target_attr]]  = 1.0

    # Calculate the entropy of the data for the target attribute
    for freq in val_freq.values():
        data_entropy += (-freq/len(data)) * math.log(freq/len(data), 2) 
        
    return data_entropy

