from models import Author, Quote

from typing import List, Dict, Any

import redis
from redis_lru import RedisLRU

client = redis.StrictRedis(host="localhost", port=6379, password=None)
cache = RedisLRU(client)


@cache
def find_by_tag(tag: str) -> list[str | None]:
    print(f"Find by {tag}")
    n_quotes = Quote.objects(tags__iregex=tag)
    if len(tag) > 0:
        result = [q.quote for q in n_quotes]
        return result
    else:
        return []


@cache
def find_by_author(author: str) -> dict[list[Any]]:
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
    while True:
        user_input = input('>>>: ').lower()
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
                elif command == 'tags':
                    tags = value.split(',')
                    tags = [tag.strip() for tag in tags]
                    matching_quotes = []
                    for tag in tags:
                        matching_quotes.extend(find_by_tag(tag))
                    print(matching_quotes)
                    continue
                else:
                    continue
            except ValueError:
                print('Use ":" between command and text which you want to find without spaces')
                continue
        else:
            print(f'Command "{user_input}" is not a right command')


if __name__ == '__main__':
    main()
    # print(find_by_author('mar'))
