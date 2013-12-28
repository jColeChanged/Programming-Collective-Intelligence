import re
import math


def sampletrain(cl):
    cl.train("Nobody owns the water", "good")
    cl.train("the quick rabbit jumps fences", "good")
    cl.train("buy drugs now", "bad")
    cl.train("make quick money at the online casino", "bad")
    cl.train("the quick brown fox jumps", "good")


def get_words(doc):
    splitter = re.compile("\\W*")
    words = [s.lower() for s in splitter.split(doc) if len(s) > 2 and len(s) < 20]
    return dict([(w, 1) for w in words])


class Classifier:
    def __init__(self, get_features, file_name=None):
        self.feature_count = {}
        self.category_count = {}
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

    def weighted_pr(self, f, c, pf_fun, weight=1.0, assumed_pr=0.5):
        basic_pr = pf_fun(f, c)
        totals = sum([self.get_feature_count(f, c) for c in self.categories()])

        weighted_average = (weight * assumed_pr + totals * basic_pr) / (weight + totals)
        return weighted_average


class NiaveBayes(Classifier):
    def __init__(self, get_features):
        Classifier.__init__(self, get_features)
        self.thresholds = {}

    def set_threshold(self, cat, t):
        self.thresholds[cat] = t

    def get_threshold(self, cat):
        if cat not in self.thresholds:
            return 1.0
        return self.thresholds[cat]

    def classify(self, item, default=None):
        probs = {}
        # Find the category with the highest probability
        max = 0.0
        for cat in self.categories():
            probs[cat] = self.bayes_pr(item, cat)
            if probs[cat] > max:
                max = probs[cat]
                best = cat

        for cat in probs:
            if cat == best:
                continue
            if probs[cat] * self.get_threshold(best) > probs[best]:
                return default
        return best

    def doc_pr(self, item, category):
        features = self.get_features(item)
        pr = 1
        for feature in features:
            pr *= self.weighted_pr(feature, category, self.feature_pr)
        return pr

    def bayes_pr(self, item, category):
        cat_prob = self.get_category_count(category) / self.total_count()
        doc_prob = self.doc_pr(item, category)
        return doc_prob * cat_prob


class FisherClassifier(Classifier):
    def __init__(self, get_features):
        Classifier.__init__(self, get_features)
        self.minimums = {}

    def set_minimum(self, cat, min):
        self.minimums[cat] = min

    def get_minimum(self, cat):
        if cat not in self.minimums:
            return 0
        return self.minimums[cat]

    def cprob(self, f, cat):
        # The frequency of this feature in this category
        clf = self.feature_pr(f, cat)
        if clf == 0:
            return 0

        # The frequency of this feature in all the categories
        freqsum = sum([self.feature_pr(f, c) for c in self.categories()])

        # The probability of this feature in all the categories divided by
        # the overall frequency
        return clf / freqsum

    def fisher_pr(self, item, category):
        pr = 1
        features = self.get_features(item)
        p = 1
        for feature in features:
            p *= self.weighted_pr(feature, category, self.cprob)
        fscore = -2 * math.log(p)
        return self.invchi2(fscore, len(features) * 2)

    def invchi2(self, chi, df):
        m = chi / 2.0
        sum = term = math.exp(-m)
        for i in range(1, df//2):
            term *= m / i
            sum += term
        return min(sum, 1.0)

    def classify(self, item, default=None):
        best = default
        max = 0.0
        for c in self.categories():
            pr = self.fisher_pr(item, c)
            if pr > self.get_minimum(c) and pr > max:
                best = c
                max = pr
        return best


