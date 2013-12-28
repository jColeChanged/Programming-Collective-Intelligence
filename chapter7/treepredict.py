from PIL import Image, ImageDraw

my_data = []
for line in file("decision_tree_example.txt"):
    my_data.append([item.strip() for item in line.split("\t")])
for row in my_data:
    row[3] = int(row[3])


class DecisionNode:
    def __init__(self, col=-1, value=None, results=None, tb=None, fb=None):
        self.col = col
        self.value = value
        self.results = results
        self.tb = tb
        self.fb = fb


def divide_set(rows, column, value):
    """
    Divides a set on a specified column. Can handle numberic or nominal
    values.
    """
    # Make a function that tells us if a row is in the first group (true)
    # or the second group (false)
    if isinstance(value, int) or isinstance(value, float):
        split_function = lambda row: row[column] >= value
    else:
        split_function = lambda row: row[column] == value

    set1 = [row for row in rows if split_function(row)]
    set2 = [row for row in rows if not split_function(row)]
    return (set1, set2)


def unique_counts(rows):
    """
    Create counts of possible results.
    """
    results = {}
    for row in rows:
        # The last column is the results
        r = row[-1]
        if r not in results:
            results[r] = 0
        results[r] += 1
    return results


def gini_impurity(rows):
    """
    Probability that a randomly placed item will be in the wrong category.
    """
    total = len(rows)
    counts = unique_counts(rows)
    imp = 0
    for k1 in counts:
        p1 = float(counts[k1]) / total
        for k2 in counts:
            if k1 == k2:
                continue
            p2 = float(counts[k2]) / total
            imp += p1 * p2
    return imp


def entropy(rows):
    """
    Entroy is the sum of p(x)log(p(x)) across all the different possible
    results
    """
    from math import log
    log2 = lambda x: log(x) / log(2)
    results = unique_counts(rows)
    ent = 0.0
    for r in results.keys():
        p = float(results[r]) / len(rows)
        ent = ent - p * log2(p)
    return ent


def build_tree(rows, scoref=entropy):
    if len(rows) == 0:
        return DecisionNode()
    current_score = scoref(rows)

    # Set up some variables to track the best criteria
    best_gain = 0.0
    best_criteria = None
    best_sets = None

    column_count = len(rows[0]) - 1
    for col in range(0, column_count):
        # Generate list of different values for this column
        column_values = {}
        for row in rows:
            column_values[row[col]] = 1
        
        # Now try dividing the rows up for each column
        for value in column_values.keys():
            set1, set2 = divide_set(rows, col, value)

            # Information gain
            p = float(len(set1)) / len(rows)
            gain = current_score - p * scoref(set1) - (1-p) * scoref(set2)
            if gain > best_gain and len(set1) > 0 and len(set2) > 0:
                best_gain = gain
                best_criteria = (col, value)
                best_sets = (set1, set2)

    # Create the subbranches
    if best_gain > 0:
        true_branch = build_tree(best_sets[0], scoref)
        false_branch = build_tree(best_sets[1], scoref)
        return DecisionNode(col=best_criteria[0], value=best_criteria[1],
                            tb=true_branch, fb=false_branch)
    else:
        return DecisionNode(results=unique_counts(rows))

def print_tree(tree, indent=""):
    # Is This a leaf node?
    if tree.results != None:
        print str(tree.results)
    else:
        # Print the criteria
        print str(tree.col) + ":" + str(tree.value) + "?"
        print indent + "T->",
        print_tree(tree.tb, indent + "  ")
        print indent + "F->",
        print_tree(tree.fb, indent + "  ")


def get_width(tree):
    if tree.tb == None and tree.fb == None:
        return 1
    else:
        return get_width(tree.fb) + get_width(tree.tb)

def get_depth(tree):
    if tree.tb == None and tree.fb == None:
        return 0
    else:
        return max(get_depth(tree.fb), get_depth(tree.tb)) + 1


def draw_node(draw, tree, x, y):
    if tree.results == None:
        # Get the width of each branch
        w1 = get_width(tree.fb) * 100
        w2 = get_width(tree.tb) * 100
        
        # Determine the total space that is required
        left = x - (w1 + w2) / 2
        right = x + (w1 + w2) / 2
        
        # Draw the condition string
        draw.text((x-20, y-10), str(tree.col) + ":" + str(tree.value), (0, 0, 0))
        
        # Draws the branch nodes
        draw.line((x, y, left + w1 / 2, y + 100), fill=(255, 0, 0))
        draw.line((x, y, right - w2 / 2, y + 100), fill=(255, 0, 0))
        
        # Draw the child branches
        draw_node(draw, tree.fb, left + w1/2, y+100)
        draw_node(draw, tree.tb, right - w2/2, y+100)
    else:
        txt = "\n".join("%s:%d" % v for v in tree.results.items())
        draw.text((x-20, y), txt, (0, 0, 0))

        
        
def draw_tree(tree, jpeg="tree.jpg"):
    w = get_width(tree) * 100
    h = get_depth(tree) * 100 + 120
    
    img = Image.new("RGB", (w, h), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    draw_node(draw, tree, w/2, 20)
    img.save(jpeg, "JPEG")
    

def classify(observation, tree):
    if tree.results != None:
        return tree.results
    else:
        v = observation[tree.col]
        branch = None
        if isinstance(v, int) or isinstance(v, float):
            if v >= tree.value:
                branch = tree.tb
            else:
                branch = tree.fb
        else:
            if v == tree.value:
                branch = tree.tb
            else:
                branch = tree.fb
        return classify(observation, branch)
        
def prune(tree,mingain):
  # If the branches aren't leaves, then prune them
  if tree.tb.results==None:
    prune(tree.tb,mingain)
  if tree.fb.results==None:
    prune(tree.fb,mingain)
    
  # If both the subbranches are now leaves, see if they
  # should merged
  if tree.tb.results!=None and tree.fb.results!=None:
    # Build a combined dataset
    tb,fb=[],[]
    for v,c in tree.tb.results.items():
      tb+=[[v]]*c
    for v,c in tree.fb.results.items():
      fb+=[[v]]*c
    
    # Test the reduction in entropy
    delta=entropy(tb+fb)-(entropy(tb)+entropy(fb)/2)

    if delta<mingain:
      # Merge the branches
      tree.tb,tree.fb=None,None
      tree.results=unique_counts(tb+fb)


def mdclassify(observation,tree):
  if tree.results!=None:
    return tree.results
  else:
    v=observation[tree.col]
    if v==None:
      tr,fr=mdclassify(observation,tree.tb),mdclassify(observation,tree.fb)
      tcount=sum(tr.values())
      fcount=sum(fr.values())
      tw=float(tcount)/(tcount+fcount)
      fw=float(fcount)/(tcount+fcount)
      result={}
      for k,v in tr.items(): result[k]=v*tw
      for k,v in fr.items(): result[k]=v*fw      
      return result
    else:
      if isinstance(v,int) or isinstance(v,float):
        if v>=tree.value: branch=tree.tb
        else: branch=tree.fb
      else:
        if v==tree.value: branch=tree.tb
        else: branch=tree.fb
      return mdclassify(observation,branch)


def variance(rows):
  if len(rows)==0: return 0
  data=[float(row[len(row)-1]) for row in rows]
  mean=sum(data)/len(data)
  variance=sum([(d-mean)**2 for d in data])/len(data)
  return variance
        