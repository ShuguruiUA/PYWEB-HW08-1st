from models import Author, Quote

from typing import List, Any


def find_by_tag(tag: str) -> list[str | None]:
    print(f"Find by {tag}")
    n_quotes = Quote.objects(tags__iregex=tag)
    result = [q.quote for q in n_quotes]
    return result


def find_by_author(author: str) -> dict[list[Any]]:
    print(f"Find by {author}")
    authors = Author.objects(fullname__iregex=author)
    result = {}
    for a in authors:
        quotes = Quote.objects(author=a)
        result[a.fullname] = [q.quote for q in quotes]
    return result


def main():
    while True:
        user_input = input('>>>: ')
        if user_input.lower() == 'exit':
            exit(0)
        elif user_input.lower not in ['name', 'exit', 'tag', 'tags']:
            print(f'Wrong command "{user_input}", try again...')
            continue
        else:
            command, value = user_input.split(":")
            if command == 'name':
                author = value
                author_quotes = find_by_author(author)
                if author_quotes:
                    print(author_quotes)
                else:
                    print('aaa')
            elif command == 'tag':
                tag = value
                tag_res = find_by_tag(tag)
                if tag_res:
                    print(tag_res)
            elif command == 'tags':
                value.split(',')
                print('oO')
                continue
            else:
                continue


if __name__ == '__main__':
    # main()
    print(find_by_author('al'))
