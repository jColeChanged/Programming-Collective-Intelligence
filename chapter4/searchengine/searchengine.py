import urllib2
from BeautifulSoup import *
from urlparse import urljoin
from pysqlite2 import dbapi2 as sqlite

IGNORE_WORDS = set(["the", "of", "to", "and", "a", "in", "is", "it"])


def exclude(function, collection):
    return [item for item in collection if not function(item)]


def unindexed_links(crawler, url, page):
    links = page("a")
    good_links = set()
    for link in links:
        if "href" in dict(link.attrs):
            edge = urljoin(url, link["href"])
            if edge.find("'") != -1:
                continue
            edge = edge.split('#')[0]
            if edge[0:4] == "http" and not crawler.is_indexed(edge):
                good_links.add(edge)
            crawler.add_link_ref(url, edge, crawler.get_text_only(link))
    return list(good_links)


def breadth_first(crawler, old, new):
    return new + old


class Crawler():
    def __init__(self, db_name):
        self.con = sqlite.connect(db_name)

    def __del__(self):
        self.con.close()

    def db_commit(self):
        self.con.commit()

    def calculate_page_rank(self, iterations=20):
        # Cleart out the current Page Rank tables
        self.con.execute("drop table if exists pagerank")
        self.con.execute("create table pagerank(urlid primary key, score)")

        # Initialize every url with a a page rank of 1
        self.con.execute('insert into pagerank select rowid, 1.0 from urllist')
        self.db_commit()

        for i in range(iterations):
            print "Iteration %d" % i
            for (urlid, ) in self.con.execute("select rowid from urllist"):
                pr = 0.15
                for (linker,) in self.con.execute('select distinct fromid from link where toid=%d' % urlid):
                    # Get the page rank of the linker
                    linkingpr = self.con.execute("select score from pagerank where urlid=%d" % linker).fetchone()[0]
                    # Get the total number of links from the linkers
                    linkingcount = self.con.execute('select count(*) from link where fromid=%d' % linker).fetchone()[0]
                    pr += 0.85 * linkingpr / linkingcount
                self.con.execute("update pagerank set score=%f where urlid=%d" % (pr, urlid))
            self.db_commit()

    def get_entry_id(self, table, field, value, create_new=True):
        """
        Helper function for getting an entry id and adding it if its not
        present.
        """
        try:
            command = "select rowid from %s where %s='%s'" % (table, field, value)
            cursor = self.con.execute(command)
        except:
            print command
        result = cursor.fetchone()
        if result is None:
            cursor = self.con.execute("insert into %s (%s) values ('%s')" % (table, field, value))
            return cursor.lastrowid
        else:
            return result[0]

    def add_to_index(self, url, soup):
        """
        Indexes an individual page.
        """
        if self.is_indexed(url):
            return
        print "Indexing %s" % url

        # Get the words
        text = self.get_text_only(soup)
        words = self.get_seperate_words(text)

        url_id = self.get_entry_id("urllist", 'url', url)

        for i in range(len(words)):
            word = words[i]
            if word in IGNORE_WORDS:
                continue
            word_id = self.get_entry_id("wordlist", "word", word)
            self.con.execute("insert into wordlocation(urlid, wordid, location) values (%d, %d, %d)" % (url_id, word_id, i))

    def get_text_only(self, soup):
        """
        Extracts the text from an HTML page (no tags).
        """
        return soup.getText()

    def get_seperate_words(self, text):
        """
        Seperates words by any non-whitespace character
        """
        splitter = re.compile("\\W*")
        return [s.lower() for s in splitter.split(text) if s != ""]

    def is_indexed(self, url):
        """
        Returns True if the url is already indexed.
        """
        u = self.con.execute("select rowid from urllist where url='%s'" % url).fetchone()
        if u is not None:
            # Check if actually crawled
            v = self.con.execute('select * from wordlocation where urlid=%d' % u[0]).fetchone()
            if v is not None:
                return True
        return False

    def add_link_ref(self, url_from, url_to, link_text):
        """
        Add a link between two pages.
        """
        words = self.get_seperate_words(link_text)
        from_id = self.get_entry_id('urllist', 'url', url_from)
        to_id = self.get_entry_id('urllist', 'url', url_to)
        if from_id == to_id:
            return
        cursor = self.con.execute("insert into link(fromid, toid) values (%d, %d)" % (from_id, to_id))
        link_id = cursor.lastrowid
        for word in words:
            if word in IGNORE_WORDS:
                continue
            word_id = self.get_entry_id("wordlist", "word", word)
            self.con.execute("insert into linkwords(linkid, wordid) values (%d, %d)" % (link_id, word_id))

    def crawl(self, urls, successor=unindexed_links, combiner=breadth_first):
        if not len(urls):
            return True
        url = urls.pop(0)
        try:
            page = BeautifulSoup(urllib2.urlopen(url).read())
        except:
            print "Could not open %s" % url
            return self.crawl(urls, successor, combiner)
        self.add_to_index(url, page)
        new_urls = successor(self, url, page)
        urls = combiner(self, urls, new_urls)
        return self.crawl(urls, successor, combiner)

    def create_index_tables(self):
        """
        Create the database tables.
        """
        self.con.execute("create table urllist(url)")
        self.con.execute("create table wordlist(word)")
        self.con.execute("create table wordlocation(urlid, wordid, location)")
        self.con.execute("create table link(fromid integer, toid integer)")
        self.con.execute("create table linkwords(wordid, linkid)")
        self.con.execute("create index wordidx on wordlist(word)")
        self.con.execute("create index ulidx on urllist(url)")
        self.con.execute("create index wordurlidx on wordlocation(wordid)")
        self.con.execute("create index urltoidx on link(toid)")
        self.con.execute("create index urlfromidx on link(fromid)")
        self.db_commit()


class Searcher():
    def __init__(self, db_name):
        """
        Opens the connection to the database.
        """
        self.con = sqlite.connect(db_name)

    def __del__(self):
        """
        Closes the connection to the database.
        """
        self.con.close()

    def get_match_rows(self, query):
        field_list = 'w0.urlid'
        table_list = ""
        clause_list = ""
        word_ids = []
        words = query.split(' ')
        table_number = 0

        for word in words:
            word_row = self.con.execute("select rowid from wordlist where word='%s'" % word).fetchone()
            if word_row is not None:
                word_id = word_row[0]
                word_ids.append(word_id)
                if table_number > 0:
                    table_list += ","
                    clause_list += " and "
                    clause_list += "w%d.urlid=w%d.urlid and " % (table_number-1, table_number)
            field_list += ',w%d.location' % table_number
            table_list += 'wordlocation w%d' % table_number
            clause_list += "w%d.wordid=%d" % (table_number, word_id)
            other_clause = " "
            table_number += 1
        full_query = "select %s from %s where %s" % (field_list, table_list, clause_list)
        cursor = self.con.execute(full_query)
        rows = [row for row in cursor]
        return rows, word_ids

    def get_scored_list(self, rows, word_ids):
        total_scores = dict([(row[0], 0) for row in rows])
 
        weights = [(1.0, self.length_score(rows))]

        for weight, scores in weights:
            for url in total_scores:
                total_scores[url] += weight * scores[url]
        return total_scores

    def get_url_name(self, id):
        return self.con.execute("select url from urllist where rowid=%d" % id).fetchone()[0]

    def normalized_scores(self, scores, small_is_better=0):
        very_small = 0.00001
        if small_is_better:
            min_score = min(scores.values())
            return dict([(u, float(min_score)/max(very_small, l)) for (u, l) in scores.items()])
        else:
            max_score = max(scores.values())
            if max_score == 0:
                max_score = very_small
            return dict([(u, float(c) / max_score) for (u, c) in scores.items()])

    def frequency_score(self, rows):
        counts = dict([(row[0], 0) for row in rows])
        for row in rows:
            counts[row[0]] += 1
        return self.normalized_scores(counts)

    #ex5
    def length_score(self, rows):
        counts = dict([(row[0], 0) for row in rows])
        for row in rows:
            counts[row[0]] = self.con.execute("select count(*) from wordlocation where urlid=%d" % row[0]).fetchone()[0]
        return self.normalized_scores(counts)


    def location_score(self, rows):
        locations = dict([(row[0], 1000000) for row in rows])
        for row in rows:
            loc = sum(row[1:])
            if loc < locations[row[0]]:
                locations[row[0]] = loc
        return self.normalized_scores(locations, small_is_better=1)

    def distance_score(self, rows):
        if len(rows[0]) <= 2:
            return dict([(row[0], 1.0) for row in rows])

        min_distance = dict([(row[0], 1000000) for row in rows])
        for row in rows:
            dist = sum([abs(row[i] - row[i-1]) for i in range(2, len(row))])
            if dist < min_distance[row[0]]:
                min_distance[row[0]] = dist
        return self.normalized_scores(min_distance, small_is_better=1)

    def pagerank_score(self, rows):
        pageranks = dict([(row[0], self.con.execute('select score from pagerank where urlid=%d' % row[0]).fetchone()[0]) for row in rows])
        maxrank = max(pageranks.values())
        normalizedscores = dict([(u, float(l)/maxrank) for (u, l) in pageranks.items()])
        return normalizedscores

    def inbound_link_score(self, rows):
        unique_urls = set([row[0] for row in rows])
        inbound_counts = {}
        for url in unique_urls:
            command = "select count(*) from link where toid=%d" % url
            inbound_counts[url] = self.con.execute(command).fetchone()[0]
        return self.normalized_scores(inbound_counts)

    # def link_text_score(self, rows, word_ids):
    #     link_scores = dict([(row[0], 0) for row in rows])
    #     for word_id in word_ids:
    #         cursor = self.con.execute('select link.fromid,link.toid from linkwords,link where wordid=%d and linkwords.linkid=link.rowid' % word_id)
    #         for (from_id, to_id) in cursor:
    #             if to_id in link_scores:
    #                 pr = self.con.execute('select score from pagerank where urlid=%d' % fromid).fetchone()[0]
    #                 link_scores[to_id] += pr
    #     maxscore = max(link_scores.values())
    #     return dict([(u, float(l)/maxscore) for (u, l) in link_scores.items()])

    def query(self, q):
        rows, word_ids = self.get_match_rows(q)
        scores = self.get_scored_list(rows, word_ids)
        ranked_scores = sorted([(score, url) for (url, score) in scores.items()], reverse=True)
        for score, url_id in ranked_scores[0:10]:
            print '%f\t%s' % (score, self.get_url_name(url_id))



engine = Searcher("searchindex.db")