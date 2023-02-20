import random


def main():
    prompt = input('Prompt: ')
    n = 3
    with open('quantum_information_wikipedia_page.txt', 'r') as f:
        corpus = f.read()
    words = corpus.lower().split()
    words = [word.lower() for word in words]    # list comprehension syntax
    big_probability_mapping = {}
    for m in range(1, n+1):
        probability_mapping = extract_continuation_probabilities(words, n)
        big_probability_mapping.update(probability_mapping)

    generate_words(prompt, big_probability_mapping, n)


def sample_next_word(probability_distribution):
    candidates = list(probability_distribution.keys())
    probabilities = list(probability_distribution.values())
    choice = random.choices(candidates, weights=probabilities)[0]
    return choice


def extract_continuation_probabilities(words, n):

    prefix_to_ngrams = {}
    for i in range(len(words) - (n-1)):
        ngram = tuple(words[i:i+n])
        prefix = ngram[:(n-1)]
        if prefix not in prefix_to_ngrams:
            prefix_to_ngrams[prefix] = []
        prefix_to_ngrams[prefix].append(ngram)

    big_counts_dictionary = {}
    for prefix, ngrams in prefix_to_ngrams.items():
        continuations = [ngram[-1] for ngram in ngrams]
        counts = {word: 0 for word in continuations}
        for word in continuations:
            counts[word] += 1
        big_counts_dictionary[prefix] = counts

    return big_counts_dictionary


def generate_words(prompt, probability_mapping, n):

    n_generated_words = 0
    all_text = prompt

#    print(prompt, ' (prompt)')

    while n_generated_words < 50:

        n_generated_words += 1
        words = all_text.split()

        for m in range(n, 0, -1):
            try:
                prompt_as_tuple = tuple(words[-(m-1):]) if m > 1 else tuple()
                probability_distribution_for_next_word = probability_mapping[prompt_as_tuple]
            except KeyError:
                continue
            next_word = sample_next_word(probability_distribution_for_next_word)
            all_text = all_text + ' ' + next_word

    print(all_text)


if __name__ == '__main__':
    main()


