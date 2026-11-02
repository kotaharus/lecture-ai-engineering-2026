#!/usr/bin/env python3
"""Conservative dictionary-only retrieval baseline for AIE Lecture 02.
No model call, no answer leakage (term_id/expected never used for retrieval).
Usage: python glossary_retrieval_baseline.py --glossary data/glossary.json \
       --before glossary_before.json --after glossary_after.json
"""
import argparse
import json
import re
import unicodedata
from collections import Counter
from pathlib import Path


def norm(s):
    return unicodedata.normalize('NFKC', str(s)).casefold().replace(' ', '')


def load_terms(path):
    obj = json.loads(Path(path).read_text(encoding='utf-8'))
    terms = obj['terms'] if isinstance(obj, dict) else obj
    if isinstance(terms, dict):
        terms = list(terms.values())
    if not isinstance(terms, list):
        raise ValueError('Expected a list at glossary["terms"]')
    result = []
    for item in terms:
        if not isinstance(item, dict):
            continue
        aliases = item.get('aliases') or []
        if isinstance(aliases, str):
            aliases = [aliases]
        definition = item.get('definition') or ''
        term = item.get('term') or item.get('name') or ''
        tid = item.get('id') or item.get('term_id')
        if term and definition:
            result.append({'id': tid, 'term': term, 'definition': definition,
                           'aliases': aliases})
    if not result:
        raise ValueError('Could not find terms with term and definition fields')
    return result


def retrieve(question, terms):
    """Match glossary terms/aliases in question; no gold IDs, no expected answers."""
    q = norm(question)
    matches = []
    for entry in terms:
        candidates = [entry['term'], *entry['aliases']]
        hits = [v for v in candidates if len(norm(v)) >= 3 and norm(v) in q]
        if hits:
            best = max(hits, key=lambda s: len(norm(s)))
            matches.append((len(norm(best)), entry))
    if not matches:
        return None
    # Prefer the longest explicit expression. If tied, reject ambiguity.
    matches.sort(key=lambda e: e[0], reverse=True)
    top = [entry for length, entry in matches if length == matches[0][0]]
    return top[0] if len(top) == 1 else None


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--glossary', required=True)
    p.add_argument('--before', required=True)
    p.add_argument('--after', required=True)
    p.add_argument('--output', default='glossary_retrieval_results.json')
    args = p.parse_args()
    terms = load_terms(args.glossary)
    before = json.loads(Path(args.before).read_text(encoding='utf-8'))
    after = json.loads(Path(args.after).read_text(encoding='utf-8'))
    if len(before) != len(after):
        raise ValueError('Before/after item counts differ')
    rows = []
    for i, (b, a) in enumerate(zip(before, after), 1):
        if (b['category'], b['question']) != (a['category'], a['question']):
            raise ValueError(f'Question mismatch at row {i}')
        hit = retrieve(b['question'], terms)
        answer = hit['definition'] if hit else '用語集に根拠なし'
        gold_id = b.get('term_id')
        if b['category'] in ('known', 'paraphrase'):
            # Only for evaluation, never used in search
            success = bool(hit and str(hit['id']) == str(gold_id))
        elif b['category'] == 'unknown':
            success = hit is None
        else:
            # Held-out gold is an exact glossary definition
            success = bool(hit and norm(hit['definition']) == norm(b.get('expected') or ''))
        rows.append({'number': i, 'category': b['category'], 'question': b['question'],
                     'gold_id': gold_id, 'retrieved_id': hit['id'] if hit else None,
                     'retrieved_term': hit['term'] if hit else None,
                     'retrieval_success': success, 'retrieval_answer': answer,
                     'before_answer': b['answer'], 'after_answer': a['answer']})
    output = Path(args.output)
    output.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f'Glossary terms: {len(terms)}; compared questions: {len(rows)}')
    for category in ('known', 'paraphrase', 'unknown', 'held_out'):
        subset = [r for r in rows if r['category'] == category]
        if subset:
            n = sum(r['retrieval_success'] for r in subset)
            print(f'  {category:10s}: {n}/{len(subset)} correct retrieval/abstention')
    print('\nDetailed results (a failed retrieval is not necessarily a model error):')
    for r in rows:
        mark = 'OK ' if r['retrieval_success'] else 'MISS'
        print(f"{r['number']:2d}. [{mark}] {r['category']:10s} | {r['retrieved_term'] or '(none)'} | {r['question']}")
    print(f'\nSaved: {output.resolve()}')
    print('NOTE: This is exact/alias lookup, not LLM+RAG; lexical paraphrases may miss.')


if __name__ == '__main__':
    main()
