##Script to parse and automate writing of Frank Karsten's pick order notes

from bs4 import BeautifulSoup
from card import Card

def save(filename, cards):
    file_ = open(filename, 'a')
    for i in range(len(cards)):
        file_.write("%s\t%d\n" % (cards[i], i + 1))
        #card_str = str(card)
        #card_split = card_str.split("\t")
        #file_.write("%s\t%s\n" % (card.get_name(), card.ratings_str()))
    file_.close()

def get_cards_from_page(src):
    links = BeautifulSoup(open(src), 'html5lib').find_all('a')
    card_links = filter(lambda x : x.has_attr('data-name'), links)
    card_names = map(lambda x : x.get('data-name'), card_links)
    return card_names
    #cards = map(lambda x : Card(card_names[x], x + 1), range(len(card_names)))
    #return cards

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
        cards = get_cards_from_page(page)
        print "Found %d cards." % len(cards)
        for card in cards:
            cardlist.append(card)
    save(dest, cardlist)

if __name__ == "__main__":
    main()
