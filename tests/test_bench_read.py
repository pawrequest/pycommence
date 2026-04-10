"""
Benchmark: item_read_dde vs item_read_csr vs cursor.read_rows()

Fetches all Contact records using three approaches and compares elapsed time.
"""

import time

import pytest
from loguru import logger
from pawlogger import configure_loguru
from sample_data import CONTACT_ITEM_NAMES

from pycommence.core.pagination import Pagination
from pycommence.pycommence_client import PyCommence

CATEGORY = 'Contact'
PK = 'Musk.Elon'
ITERATIONS = 100


@pytest.fixture(scope='module')
def client():
    configure_loguru(logger, level='INFO')
    from pycommence.threads import com_context

    with com_context(), PyCommence(CATEGORY) as c:
        yield c


# ── helpers ───────────────────────────────────────────────────────────────

def _run_bench(fn, label):
    """Run *fn* once, return (label, total_s)."""
    start = time.perf_counter()
    result = fn()
    elapsed = time.perf_counter() - start
    assert result, f'{label} returned empty result'
    return label, elapsed, result


def _print_comparison(rows):
    """Pretty-print a comparison table from a list of (label, total_s, n_records) tuples."""
    sep = '=' * 70
    lines = [
        '',
        sep,
        f'  Benchmark: read ALL Contact records',
        sep,
    ]

    fastest = min(rows, key=lambda r: r[1])

    for label, total, n_records in rows:
        per_rec = total / n_records * 1000
        tag = ' ◄ winner' if label == fastest[0] else ''
        ratio_vs_best = total / fastest[1]
        x_text = f'  ({ratio_vs_best:.1f}×)' if label != fastest[0] else ''
        lines.append(
            f'  {label:<30}: {total:>7.3f}s | {n_records:>3} records | {per_rec:>6.1f} ms/rec{x_text}{tag}'
        )

    lines += [sep, '']
    print('\n'.join(lines))


# ── the test ──────────────────────────────────────────────────────────────

def test_compare_all_methods(client: PyCommence):
    """Fetch every contact with DDE, CSR (one-by-one), and CSR read_rows(); compare."""

    names = CONTACT_ITEM_NAMES
    n = len(names)

    # ── warm-up ──
    client.item_read_dde(CATEGORY, names[0])
    client.item_read_csr(csrname=CATEGORY, pk=names[0])
    list(client.cursor(CATEGORY).read_rows(pagination=Pagination(limit=1)))

    # ── 1. DDE one-by-one ──
    def dde_all():
        results = []
        for name in names:
            results.append(client.item_read_dde(CATEGORY, name))
        return results

    lbl_dde, t_dde, res_dde = _run_bench(dde_all, 'DDE  (one-by-one)')

    # ── 2. CSR one-by-one (read_row per pk) ──
    def csr_one():
        results = []
        for name in names:
            results.append(client.item_read_csr(csrname=CATEGORY, pk=name))
        return results

    lbl_csr1, t_csr1, res_csr1 = _run_bench(csr_one, 'CSR  (one-by-one)')

    # ── 3. CSR one-by-one by pre-resolved row_id ──
    csr = client.cursor(CATEGORY)
    row_ids = {name: csr.pk_to_id(name) for name in names}

    def csr_by_id():
        results = []
        for name in names:
            results.append(client.item_read_csr(csrname=CATEGORY, row_id=row_ids[name]))
        return results

    lbl_csr_id, t_csr_id, res_csr_id = _run_bench(csr_by_id, 'CSR  (by row_id)')

    # ── 4. CSR pk_to_id only (filter overhead) ──
    def pk_resolve_only():
        results = []
        for name in names:
            results.append(csr.pk_to_id(name))
        return results

    lbl_resolve, t_resolve, res_resolve = _run_bench(pk_resolve_only, 'CSR  pk_to_id only')

    # ── 5. CSR read_rows() bulk generator ──
    def csr_bulk():
        csr_ = client.cursor(CATEGORY)
        pagination = Pagination(limit=n, offset=0)
        return list(csr_.read_rows(pagination=pagination))

    lbl_bulk, t_bulk, res_bulk = _run_bench(csr_bulk, 'CSR  read_rows() bulk')

    # ── comparison ──
    results = [
        (lbl_dde, t_dde, len(res_dde)),
        (lbl_csr1, t_csr1, len(res_csr1)),
        (lbl_csr_id, t_csr_id, len(res_csr_id)),
        (lbl_resolve, t_resolve, len(res_resolve)),
        (lbl_bulk, t_bulk, len(res_bulk)),
    ]
    _print_comparison(results)


def test_single_record_x100(client: PyCommence):
    """Read Musk.Elon 100× with each method for a focused single-record comparison."""

    # warm-up
    client.item_read_dde(CATEGORY, PK)
    client.item_read_csr(csrname=CATEGORY, pk=PK)

    def dde_100():
        for _ in range(ITERATIONS):
            r = client.item_read_dde(CATEGORY, PK)
        return [r]

    def csr_100():
        for _ in range(ITERATIONS):
            r = client.item_read_csr(csrname=CATEGORY, pk=PK)
        return [r]

    _, t_dde, _ = _run_bench(dde_100, 'DDE')
    _, t_csr, _ = _run_bench(csr_100, 'CSR')

    results = [
        (f'DDE  ×{ITERATIONS}', t_dde, ITERATIONS),
        (f'CSR  ×{ITERATIONS}', t_csr, ITERATIONS),
    ]
    _print_comparison(results)
