import configparser
import smtplib
import time
from typing import List, Set

import wikipediaapi

wiki = wikipediaapi.Wikipedia('Testing (mv1492412131@gmail.com)', 'en')


def parse_man_page(man_page: wikipediaapi.WikipediaPage):
    if 'ru' in man_page.langlinks.keys():
        return man_page.fullurl, man_page.langlinks['ru'].summary.split('\n')[0]
    else:
        return man_page.fullurl, man_page.summary.split('\n')[0]


def parse_death_page(page: wikipediaapi.WikipediaPage) -> List[wikipediaapi.WikipediaPage]:
    current_deaths = []
    for day in page.sections[0].sections:
        for i in day.text.split('\n'):
            name = i[:i.find(',')]
            for j in page.links.keys():
                if name in j:
                    current_deaths.append(page.links[j])
                    break
    return current_deaths


def send_emails(sender, login, password, server, recipient, diff: Set[wikipediaapi.WikipediaPage]):
    server = smtplib.SMTP(server)
    server.login(login, password)
    for i in diff:
        server.sendmail(sender, [recipient], i.fullurl + '\n' + i.summary)


def check_for_new_deaths(sender, login, password, server, recipient, timer):
    page = wiki.page('Deaths_in_2023')
    before = parse_death_page(page)
    while True:
        current = parse_death_page(page)
        diff = set(current) - set(before)
        if len(diff) > 0:
            send_emails(sender, login, password, server, recipient, diff)
        time.sleep(int(timer))


def main():
    parser = configparser.ConfigParser()
    parser.read('config.ini')
    config = list(parser['MAIN'].values())
    check_for_new_deaths(*config)


if __name__ == '__main__':
    main()
