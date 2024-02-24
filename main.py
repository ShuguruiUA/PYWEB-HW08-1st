from models import Author, Quote

from typing import List, Dict, Any

import redis
from redis_lru import RedisLRU

# створюємо підключення до бази Redis та кеш за допомогою RedisLRU
client = redis.StrictRedis(host="localhost", port=6379, password=None)
cache = RedisLRU(client)


@cache
def find_by_tag(tag: str) -> list[str | None]:
    """
    Функція отримує строку введену користувачем та шукає у базі тегів - тег.
    Можливо співпадіння від 1 літери та повертає список усіх
    знайдених цитат за тегом. також пошук кешується
    """
    print(f"Find by {tag}")
    n_quotes = Quote.objects(tags__iregex=tag)
    if len(tag) > 0:
        result = [q.quote for q in n_quotes]
        return result
    else:
        return f'The search value "{tag}" is not present in DB'


@cache
def find_by_author(author: str) -> dict[list[Any]]:
    """
    Функція отримує строку введену користувачем та шукає у базі цитат автора.
    Можливо співпадіння від 1 літери та повертає словник у якому ключ - автор,
    а значення - список усіх знайдених цитат цього автора. також пошук кешується
    """
    print(f"Find by {author}")
    authors = Author.objects(fullname__iregex=author)
    result = {}
    if author:
        for a in authors:
            quotes = Quote.objects(author=a)
            result[a.fullname] = [q.quote for q in quotes]
        return result
    else:
        return {}


def main():
    """
    Функція працює у безкінечному циклі поки користувач не введе 'exit'
    Приймає у себе команду для пошуку через ":". доступні команди: name, tag, tags
    у випадку tags - усі теги, які необхідно знайти розділяються комою.
    """
    while True:
        user_input = input('>>> ').lower()
        if user_input.lower() == 'exit':
            exit(0)
        elif user_input.lower().startswith('name') or user_input.lower().startswith('tag'):
            try:
                command, value = user_input.split(":")
                if command == 'name':
                    author = value
                    author_quotes = find_by_author(author)
                    if author_quotes:
                        print(author_quotes)
                    else:
                        print(f'Author with name "{author}" is not present in the DB')
                elif command == 'tag':
                    tag = value
                    tag_res = find_by_tag(tag)
                    if tag_res:
                        print(tag_res)
                    else:
                        print(f'The search value {value} is not present in DB')
                elif command == 'tags':
                    tags = value.split(',')
                    tags = [tag.strip() for tag in tags]
                    matching_quotes = []
                    for tag in tags:
                        if tag:
                            matching_quotes.extend(find_by_tag(tag))
                    if len(matching_quotes) > 0:
                        print(matching_quotes)
                    else:
                        print(f'The search value "{tag}" is not present in DB')
                else:
                    continue
            except ValueError:
                print('Use ":" between command and text which you want to find without spaces and separated by coma')
                continue
        else:
            print(f'Command "{user_input}" is not a right command')


if __name__ == '__main__':
    main()

