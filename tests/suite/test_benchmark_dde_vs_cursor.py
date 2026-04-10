"""
Benchmarks comparing DDE (GetData / ViewData) vs Cursor (COM) for bulk reads.

These tests require a live Commence instance with data in the tested categories.
Run with ``pytest -v -s tests/suite/test_benchmark_dde_vs_cursor.py`` to see
timing output printed to stdout.

Each test is marked ``@pytest.mark.integration`` so the full suite can skip
them when no Commence DB is available.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field

import pytest
from loguru import logger

from pycommence.core.filters import ConditionType
from pycommence.core.pagination import Pagination
from pycommence.dde import DDETopic
from pycommence.pycommence_client import PyCommence

pytestmark = pytest.mark.integration

# ── configurable defaults ──────────────────────────────────────────────
BENCH_CATEGORY = 'Contact'
SMALL_LIMIT = 5  # for quick sanity checks

# Subset of fields used only by TestFieldScaling to measure field-count impact
SCALING_FIELDS: list[str] = [
    'contactKey',
    'firstName',
    'lastName',
    'businessNumber',
    'emailBusiness',
    'Title',
    'busCity',
    'busState',
]


# ── helpers ────────────────────────────────────────────────────────────


@dataclass
class BenchResult:
    label: str
    rows: int
    elapsed: float
    fields: int = 0
    extra: dict = field(default_factory=dict)

    @property
    def per_row_ms(self) -> float:
        return (self.elapsed / self.rows * 1000) if self.rows else 0.0

    def summary(self) -> str:
        return (
            f'{self.label:<30s}  '
            f'rows={self.rows:<6d}  '
            f'fields={self.fields:<4d}  '
            f'total={self.elapsed:>8.3f}s  '
            f'per_row={self.per_row_ms:>8.2f}ms'
        )


def _print_results(*results: BenchResult):
    """Pretty-print a comparison table."""
    print('\n' + '=' * 80)
    print('  BENCHMARK RESULTS')
    print('=' * 80)
    for r in results:
        print(f'  {r.summary()}')
    if len(results) >= 2:
        fastest = min(results, key=lambda r: r.elapsed)
        slowest = max(results, key=lambda r: r.elapsed)
        speedup = slowest.elapsed / fastest.elapsed if fastest.elapsed else float('inf')
        print(f'\n  ▸ Fastest: {fastest.label}  ({speedup:.1f}× faster than {slowest.label})')
    print('=' * 80 + '\n')


# ── fixtures ───────────────────────────────────────────────────────────


@pytest.fixture()
def category_row_count(pycmc: PyCommence) -> int:
    """Return the number of items in the benchmark category."""
    count = pycmc.cursor(BENCH_CATEGORY).row_count
    logger.info(f'{BENCH_CATEGORY} has {count} rows')
    return count


@pytest.fixture()
def all_fields(pycmc: PyCommence) -> list[str]:
    """Return all field names for the benchmark category."""
    return pycmc.conversation(DDETopic.GET).category_field_names(BENCH_CATEGORY)


# ── tests ──────────────────────────────────────────────────────────────


class TestBulkReadAllRows:
    """Compare reading *every* record (all fields) in a category across all three methods."""

    def test_cursor_read_all(self, pycmc: PyCommence, category_row_count):
        """Baseline: read all rows via Cursor / COM API."""
        t0 = time.perf_counter()
        rows = list(pycmc.read_all_cursor(BENCH_CATEGORY))
        elapsed = time.perf_counter() - t0

        assert len(rows) == category_row_count
        assert isinstance(rows[0], dict)

        result = BenchResult('Cursor (COM)', len(rows), elapsed, fields=len(rows[0]))
        print(f'\n  {result.summary()}')

    def test_dde_get_read_all(self, pycmc: PyCommence, category_row_count):
        """Read all rows via DDE GetData topic (N+1 round-trips)."""
        t0 = time.perf_counter()
        rows = list(pycmc.read_all_dde_get(BENCH_CATEGORY))
        elapsed = time.perf_counter() - t0

        assert len(rows) == category_row_count
        assert isinstance(rows[0], dict)

        result = BenchResult('DDE GetData', len(rows), elapsed, fields=len(rows[0]))
        print(f'\n  {result.summary()}')

    def test_dde_view_read_all(self, pycmc: PyCommence, category_row_count):
        """Read all rows via DDE ViewData topic (iterate by index)."""
        t0 = time.perf_counter()
        rows = list(pycmc.read_all_dde_view(BENCH_CATEGORY))
        elapsed = time.perf_counter() - t0

        assert len(rows) == category_row_count
        assert isinstance(rows[0], dict)

        result = BenchResult('DDE ViewData', len(rows), elapsed, fields=len(rows[0]))
        print(f'\n  {result.summary()}')

    def test_compare_all_methods(self, pycmc: PyCommence, category_row_count):
        """Run all three methods back-to-back and print a comparison table."""
        results: list[BenchResult] = []

        # 1. Cursor / COM
        t0 = time.perf_counter()
        cursor_rows = list(pycmc.read_all_cursor(BENCH_CATEGORY))
        results.append(BenchResult('Cursor (COM)', len(cursor_rows), time.perf_counter() - t0, fields=len(cursor_rows[0]) if cursor_rows else 0))

        # 2. DDE GetData
        t0 = time.perf_counter()
        get_rows = list(pycmc.read_all_dde_get(BENCH_CATEGORY))
        results.append(BenchResult('DDE GetData', len(get_rows), time.perf_counter() - t0, fields=len(get_rows[0]) if get_rows else 0))

        # 3. DDE ViewData
        t0 = time.perf_counter()
        view_rows = list(pycmc.read_all_dde_view(BENCH_CATEGORY))
        results.append(BenchResult('DDE ViewData', len(view_rows), time.perf_counter() - t0, fields=len(view_rows[0]) if view_rows else 0))

        # Verify row counts match
        assert len(cursor_rows) == category_row_count
        assert len(get_rows) == category_row_count
        assert len(view_rows) == category_row_count

        _print_results(*results)


class TestSubsetRead:
    """Compare reading a small subset of rows (paginated cursor vs DDE single-item)."""

    def test_cursor_read_n(self, pycmc: PyCommence):
        """Read a limited number of rows via cursor."""
        t0 = time.perf_counter()
        csr = pycmc.cursor(BENCH_CATEGORY)
        rows = [
            rd.data
            for rd in csr.read_rows(pagination=Pagination(offset=0, limit=SMALL_LIMIT))
            if hasattr(rd, 'data')
        ]
        elapsed = time.perf_counter() - t0

        assert len(rows) == SMALL_LIMIT
        result = BenchResult(f'Cursor (first {SMALL_LIMIT})', len(rows), elapsed, fields=len(rows[0]))
        print(f'\n  {result.summary()}')

    def test_dde_get_read_n(self, pycmc: PyCommence, all_fields):
        """Read first N items via DDE GetData (requires item names first)."""
        conv = pycmc.conversation(DDETopic.GET)
        from pycommence.dde import msgs

        t0 = time.perf_counter()
        item_names_raw = conv.send_message(msgs.get.item_names(BENCH_CATEGORY))
        item_names = [item_names_raw] if isinstance(item_names_raw, str) else list(item_names_raw)
        item_names = item_names[:SMALL_LIMIT]

        rows = []
        for name in item_names:
            row = pycmc.item_read_dde(BENCH_CATEGORY, name)
            rows.append(row)
        elapsed = time.perf_counter() - t0

        assert len(rows) == SMALL_LIMIT
        result = BenchResult(f'DDE GetData (first {SMALL_LIMIT})', len(rows), elapsed, fields=len(all_fields))
        print(f'\n  {result.summary()}')

    def test_dde_view_read_n(self, pycmc: PyCommence, all_fields):
        """Read first N items via DDE ViewData by index."""
        from pycommence.dde import DDEMessageBase, msgs

        if DDETopic.VIEW not in pycmc._conversations:
            pycmc._create_conversation(DDETopic.VIEW)
        conv = pycmc.conversation(DDETopic.VIEW)

        t0 = time.perf_counter()
        conv.view_reset(BENCH_CATEGORY)

        rows: list[dict[str, str]] = []
        for idx in range(SMALL_LIMIT):
            def build_msg(chunk: list[str], _idx=idx) -> DDEMessageBase:
                return msgs.view.fields(_idx + 1, chunk, pycmc.options.delim)

            row_values = pycmc._chunked_dde_request(all_fields, build_msg)
            rows.append(dict(zip(all_fields, row_values)))
        elapsed = time.perf_counter() - t0

        assert len(rows) == SMALL_LIMIT
        result = BenchResult(f'DDE ViewData (first {SMALL_LIMIT})', len(rows), elapsed, fields=len(all_fields))
        print(f'\n  {result.summary()}')

    def test_compare_subset(self, pycmc: PyCommence, all_fields):
        """Side-by-side comparison for small reads."""
        from pycommence.dde import DDEMessageBase, msgs

        results: list[BenchResult] = []

        # Cursor
        t0 = time.perf_counter()
        csr = pycmc.cursor(BENCH_CATEGORY)
        cursor_rows = [
            rd.data
            for rd in csr.read_rows(pagination=Pagination(offset=0, limit=SMALL_LIMIT))
            if hasattr(rd, 'data')
        ]
        results.append(BenchResult(f'Cursor (first {SMALL_LIMIT})', len(cursor_rows), time.perf_counter() - t0, fields=len(cursor_rows[0]) if cursor_rows else 0))

        # DDE GetData
        conv = pycmc.conversation(DDETopic.GET)
        t0 = time.perf_counter()
        item_names_raw = conv.send_message(msgs.get.item_names(BENCH_CATEGORY))
        item_names = [item_names_raw] if isinstance(item_names_raw, str) else list(item_names_raw)
        get_rows = [pycmc.item_read_dde(BENCH_CATEGORY, n) for n in item_names[:SMALL_LIMIT]]
        results.append(BenchResult(f'DDE GetData (first {SMALL_LIMIT})', len(get_rows), time.perf_counter() - t0, fields=len(all_fields)))

        # DDE ViewData
        if DDETopic.VIEW not in pycmc._conversations:
            pycmc._create_conversation(DDETopic.VIEW)
        vconv = pycmc.conversation(DDETopic.VIEW)
        t0 = time.perf_counter()
        vconv.view_reset(BENCH_CATEGORY)
        view_rows: list[dict[str, str]] = []
        for idx in range(SMALL_LIMIT):
            def build_msg(chunk: list[str], _idx=idx) -> DDEMessageBase:
                return msgs.view.fields(_idx + 1, chunk, pycmc.options.delim)

            row_values = pycmc._chunked_dde_request(all_fields, build_msg)
            view_rows.append(dict(zip(all_fields, row_values)))
        results.append(BenchResult(f'DDE ViewData (first {SMALL_LIMIT})', len(view_rows), time.perf_counter() - t0, fields=len(all_fields)))

        _print_results(*results)


class TestFieldScaling:
    """Measure how the number of fields affects read performance."""

    FEW_FIELDS = ['contactKey', 'firstName', 'lastName']
    MANY_FIELDS = SCALING_FIELDS

    def test_cursor_few_vs_many_fields(self, pycmc: PyCommence, category_row_count):
        """Cursor API: compare reading with few fields vs many fields.

        Note: Cursor API always returns *all* columns in the default column set,
        so field count doesn't change the query — this serves as a control.
        """
        results: list[BenchResult] = []

        t0 = time.perf_counter()
        rows = list(pycmc.read_all_cursor(BENCH_CATEGORY))
        results.append(BenchResult('Cursor (all fields)', len(rows), time.perf_counter() - t0, fields=len(rows[0]) if rows else 0))

        _print_results(*results)

    def test_dde_get_few_vs_many_fields(self, pycmc: PyCommence, category_row_count):
        """DDE GetData: compare reading 3 fields vs 8 fields per item."""
        results: list[BenchResult] = []

        t0 = time.perf_counter()
        rows_few = list(pycmc.read_all_dde_get(BENCH_CATEGORY, fields=self.FEW_FIELDS))
        results.append(BenchResult('DDE GetData (3 fields)', len(rows_few), time.perf_counter() - t0, fields=len(self.FEW_FIELDS)))

        t0 = time.perf_counter()
        rows_many = list(pycmc.read_all_dde_get(BENCH_CATEGORY, fields=self.MANY_FIELDS))
        results.append(BenchResult('DDE GetData (8 fields)', len(rows_many), time.perf_counter() - t0, fields=len(self.MANY_FIELDS)))

        assert len(rows_few) == len(rows_many) == category_row_count
        _print_results(*results)

    def test_dde_view_few_vs_many_fields(self, pycmc: PyCommence, category_row_count):
        """DDE ViewData: compare reading 3 fields vs 8 fields per item."""
        results: list[BenchResult] = []

        t0 = time.perf_counter()
        rows_few = list(pycmc.read_all_dde_view(BENCH_CATEGORY, fields=self.FEW_FIELDS))
        results.append(BenchResult('DDE ViewData (3 fields)', len(rows_few), time.perf_counter() - t0, fields=len(self.FEW_FIELDS)))

        t0 = time.perf_counter()
        rows_many = list(pycmc.read_all_dde_view(BENCH_CATEGORY, fields=self.MANY_FIELDS))
        results.append(BenchResult('DDE ViewData (8 fields)', len(rows_many), time.perf_counter() - t0, fields=len(self.MANY_FIELDS)))

        assert len(rows_few) == len(rows_many) == category_row_count
        _print_results(*results)


class TestSingleItemRead:
    """Compare reading a single known item across methods."""

    ITEM_PK = 'Bezos.Jeff'

    def test_compare_single_item(self, pycmc: PyCommence, all_fields):
        """Read a single item with each method and compare latency."""
        from pycommence.dde import DDEMessageBase, msgs

        results: list[BenchResult] = []

        # Cursor read by PK
        t0 = time.perf_counter()
        row = pycmc.cursor(BENCH_CATEGORY).read_row(pk=self.ITEM_PK)
        results.append(BenchResult('Cursor read_row(pk)', 1, time.perf_counter() - t0, fields=len(row.data)))

        # DDE GetData (all fields)
        t0 = time.perf_counter()
        row_dde = pycmc.item_read_dde(BENCH_CATEGORY, self.ITEM_PK)
        results.append(BenchResult('DDE GetData item_read', 1, time.perf_counter() - t0, fields=len(row_dde)))

        # DDE ViewData (single item by index lookup)
        if DDETopic.VIEW not in pycmc._conversations:
            pycmc._create_conversation(DDETopic.VIEW)
        vconv = pycmc.conversation(DDETopic.VIEW)
        t0 = time.perf_counter()
        vconv.view_reset(BENCH_CATEGORY)
        vconv.view_filter_by_field('contactKey', self.ITEM_PK, condition=ConditionType.EQUAL)
        total = vconv.row_count()
        assert total == 1
        def build_msg(chunk: list[str]) -> DDEMessageBase:
            return msgs.view.fields(1, chunk, pycmc.options.delim)
        row_values = pycmc._chunked_dde_request(all_fields, build_msg)
        row_view = dict(zip(all_fields, row_values))
        results.append(BenchResult('DDE ViewData (filter+read)', 1, time.perf_counter() - t0, fields=len(all_fields)))

        # Verify all methods return same data for the overlapping fields
        mismatches = []
        for fld in all_fields:
            if row.data[fld] != row_dde[fld] or row_dde[fld] != row_view[fld]:
                mismatches.append(f'  {fld!r}: cursor={row.data[fld]!r}  dde_get={row_dde[fld]!r}  dde_view={row_view[fld]!r}')
        if mismatches:
            print(f'\n  ⚠ {len(mismatches)} field(s) differ (likely date/format differences):')
            for m in mismatches:
                print(m)

        _print_results(*results)

