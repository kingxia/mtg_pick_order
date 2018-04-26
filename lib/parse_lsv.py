##Script to parse and automate writing of LSV's limited playability notes

import urllib
from card import Card

name_delimiters = ["<h2>",
                   "<p><strong>",
                   "<h1>"]
name_end_delimiters = ["</h2>",
                       "</strong><br />",
                       "</h1>"]
#rating_delimiter = "<p><b>Limited: "
#rating_end_delimiter = "</b></p>"

rating_delimiters = ["<p><b>Limited:</b> ",
                     "<p><b>Limited: ",
                     "<p>Limited: ",
					 "<h3>Limited: "]
rating_end_delimiters = ["</p>",
                         "</b></p>",
                         "</p>",
						 "</h3>"]

ignore_strings = ["Set Reviews", "Ratings Scale"]


def save(filename, cards):
    file_ = open(filename, 'a')
    for card in cards:
        card_str = str(card)
        card_split = card_str.split("\t")
        file_.write("%s\t%s\n" % (card.get_name(), card.ratings_str()))
    file_.close()

def fetch_webpage(webpage):
    #Would normally be able to input urls but unfortunately CFB doesn't allow basic scraping
    conn = urllib.urlopen(webpage)
    html = [line.strip() for line in conn.readlines()]
    conn.close()
    return html

def fetch_webpage_local(src):
    file_ = open(src, 'r')
    html = [line.strip() for line in file_.readlines()]
    file_.close()
    return html

def filter_webpage(html):
    names = []
    ratings = []
    for line in html:
        for i in range(len(name_delimiters)):
            if line.startswith(name_delimiters[i]):
                skip = False
                for s in ignore_strings:
                    if s in line:
                        skip = True
                if skip:
                    continue
                names.append(line[len(name_delimiters[i]):len(line)-len(name_end_delimiters[i])])

        for i in range(len(rating_delimiters)):
            if line.startswith(rating_delimiters[i]):
                ratings.append(line[len(rating_delimiters[i]):len(line)-len(rating_end_delimiters[i])])
    cards = []
    #print str(names)
    #print str(ratings)
    for i in range(min(len(names), len(ratings))):
        r_set = ratings[i].split(" // ")
        try:
            fr_set = [float(r) for r in r_set]
            cards.append(Card(names[i], fr_set))
        except ValueError:
            print "\tFailed to write %s %s" % (names[i], ratings[i])
    return cards

def store_cards(page_data, cardlist):
    return

def get_webpages_from_user():
    user_input = raw_input("Link: ")
    webpages = []
    while user_input != "":
        webpages.append(user_input)
        user_input = raw_input("Link: ")
    return webpages

def main():
    dest = raw_input("Save to: ")
    sites = get_webpages_from_user()
    cardlist = []
    for page in sites:
        html = fetch_webpage_local(page)
        cards = filter_webpage(html)
        print "Found %d cards." % len(cards)
        for card in cards:
            cardlist.append(card)
    save(dest, cardlist)

if __name__ == "__main__":
    main()
