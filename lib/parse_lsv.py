##Script to parse and automate writing of LSV's limited playability notes

import urllib
from card import Card

name_delimiters = ["<h2>"]
name_end_delimiters = ["</h2>"]
#rating_delimiter = "<p><b>Limited: "
#rating_end_delimiter = "</b></p>"

rating_delimiters = ["<p><b>Limited:</b> ",
                     "<p><b>Limited: "]
rating_end_delimiters = ["</p>",
                         "</b></p>"]


def save(filename, cards):
    file_ = open(filename, 'a')
    for card in cards:
        card_str = str(card)
        card_split = card_str.split("\t")
        file_.write("%s\t%s\n" % (card_split[1], card_split[0]))
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
                names.append(line[len(name_delimiters[i]):len(line)-len(name_end_delimiters[i])])

        for i in range(len(rating_delimiters)):
            if line.startswith(rating_delimiters[i]):
                ratings.append(line[len(rating_delimiters[i]):len(line)-len(rating_end_delimiters[i])])
    cards = []
    for i in range(min(len(names), len(ratings))):
        try:
            cards.append(Card(names[i], float(ratings[i])))
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
