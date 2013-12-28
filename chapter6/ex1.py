"""
Varying assumed probabilities

Change the classifier class os it supports different assumed probabilities
for different features. Change the init method so that it will take another
classifier and start with a better guess than 0.5 for the assume probs.
"""


class Classifier:
    def __init__(self, get_features, other_classifier, file_name=None):
        self.feature_count = {}
        self.category_count = {}
        self.other_classifier = other_classifier
        self.get_features = get_features

    def increment_feature(self, feature, category):
        self.feature_count.setdefault(feature, {})
        self.feature_count[feature].setdefault(category, 0)
        self.feature_count[feature][category] += 1

    def increment_category(self, category):
        self.category_count.setdefault(category, 0)
        self.category_count[category] += 1

    def get_feature_count(self, feat, cat):
        if feat in self.feature_count and cat in self.feature_count[feat]:
            return float(self.feature_count[feat][cat])
        return 0.0

    def get_category_count(self, category):
        if category in self.category_count:
            return float(self.category_count[category])
        return 0.0

    def total_count(self):
        return sum(self.category_count.values())

    def categories(self):
        return self.category_count.keys()

    def train(self, item, category):
        features = self.get_features(item)
        for feature in features:
            self.increment_feature(feature, category)
        self.increment_category(category)

    def feature_pr(self, feature, category):
        c_count = self.get_category_count(category)
        f_count = self.get_feature_count(feature, category)
        return 0 if c_count == 0 else f_count / c_count

    def weighted_pr(self, f, c, pf_fun, weight=1.0):
        assumed_pr = self.other_classifier.prob(f, c)
        basic_pr = pf_fun(f, c)
        totals = sum([self.get_feature_count(f, c) for c in self.categories()])

        weighted_average = (weight * assumed_pr + totals * basic_pr) / (weight + totals)
        return weighted_average
