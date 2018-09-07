from collections import defaultdict


def tree(categories):
    category_tree = defaultdict(set)

    for category_entry in categories:
        if not category_entry:
            continue
        for category, subcategories in category_entry.items():
            category_tree[category].update(subcategories)
    return {category: list(sorted(subcategories))
            for category, subcategories in category_tree.items()}
