#
#
import sys, bisect
from file_ops import (
    read_sb_solution_wordlist,
    read_sb_wordlist,
    read_found_wordlist,
    write_sb_wordlist,
)
from utils import add_words, remove_words, get_solve_date


def main(days_ago=1):
    # First, determine the solve date in iso format
    iso_solve_date = get_solve_date(days_ago)

    # Then, insert words from the solution file to the sb_wordlist
    sb_wordlist, sb_wordlist_len = read_sb_wordlist()

    sb_solutions = read_sb_solution_wordlist(iso_solve_date)

    sb_wordlist, added_words, num_of_added_words = add_words(sb_wordlist, sb_solutions)
    print("\nNum of added words:\t\t\t", num_of_added_words)
    print("\nAdded words")
    print("===========")
    print(added_words)

    # Save the sb_wordlist containing the added words
    print("\nNumber of words before additions:\t", sb_wordlist_len)
    sb_wordlist_len_after_adding = write_sb_wordlist(sb_wordlist)
    print("\nNumber of words after additions:\t", sb_wordlist_len_after_adding)
    print(
        "\nNumber of words added:\t",
        sb_wordlist_len_after_adding - sb_wordlist_len,
        "\n",
    )

    # Second, remove words from the sb_wordlist that were found but not included
    # in the sb_solutions

    try:
        found_words = read_found_wordlist(iso_solve_date)
    except FileNotFoundError:
        return

    words_to_remove = []
    for word in found_words:
        if word not in sb_solutions:
            words_to_remove.append(word)

    sb_wordlist, removed_words, num_of_removed_words = remove_words(
        sb_wordlist, words_to_remove
    )
    print("\nNumber of removed words:\t\t", num_of_removed_words, "\n")
    print("Removed Words")
    print("=============")
    print(removed_words)

    sb_wordlist_len_after_removal = write_sb_wordlist(sb_wordlist)
    print("\nNumber of words after removal:\t\t", sb_wordlist_len_after_removal)
    net_change_wordlist = sb_wordlist_len_after_removal - sb_wordlist_len
    if net_change_wordlist < 0:
        change_text = "removed"
    else:
        change_text = "added"

    txt = (
        "\nNet number of words " + change_text + ":\t\t" + str(abs(net_change_wordlist))
    )
    print(txt)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        try:
            main(sys.argv[1])
        except:
            print("\nError: incorrect argument for days_ago.\n")
    else:
        main(1)

    # print("argv:", sys.argv[1])
