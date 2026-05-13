from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal
from typing import Any, cast

import sqlalchemy as sa
from sqlalchemy import Engine
from src.domain.market.snapshot import (
    MarketRegime,
    MarketSnapshot,
    PriceOHLCV,
    ProviderProvenance,
)
from src.domain.market.snapshot_persistence import PersistedMarketSnapshot
from src.infrastructure.persistence.postgres import PostgresConnectionSettings

_METADATA = sa.MetaData()

_MARKET_ADVISORY_SNAPSHOTS = sa.Table(
    "market_advisory_snapshots",
    _METADATA,
    sa.Column("snapshot_id", sa.BigInteger(), primary_key=True),
    sa.Column("provider_id", sa.Text(), nullable=False),
    sa.Column("provider_version", sa.Text(), nullable=False),
    sa.Column("symbol", sa.Text(), nullable=False),
    sa.Column("fetched_at", sa.DateTime(timezone=True), nullable=False),
    sa.Column("data_as_of", sa.DateTime(timezone=True), nullable=False),
    sa.Column("open_price", sa.Text(), nullable=False),
    sa.Column("high_price", sa.Text(), nullable=False),
    sa.Column("low_price", sa.Text(), nullable=False),
    sa.Column("close_price", sa.Text(), nullable=False),
    sa.Column("volume", sa.BigInteger(), nullable=False),
    sa.Column("regime", sa.Text(), nullable=False, server_default="unknown"),
    sa.Column(
        "persisted_at",
        sa.DateTime(timezone=True),
        nullable=False,
        server_default=sa.text("now()"),
    ),
)


class PostgresMarketSnapshotStore:
    """Postgres-backed advisory market snapshot persistence store.

    Stores full OHLCV snapshots in the market_advisory_snapshots table,
    which is separate from the canonical event_ledger. All stored records
    are advisory context — never canonical facts.

    Decimal prices are stored as TEXT to preserve precision through the
    JSON/Postgres round-trip (consistent with the API serialization approach).

    Satisfies MarketSnapshotPersistenceStore structurally (no inheritance).
    """

    def __init__(
        self,
        database_url: str | None = None,
        engine: Engine | None = None,
    ) -> None:
        if database_url is not None and engine is not None:
            raise ValueError("database_url and engine are mutually exclusive")
        self._engine = engine or sa.create_engine(
            _sqlalchemy_url(
                database_url
                or PostgresConnectionSettings.from_environment().database_url
            )
        )

    def persist(self, snapshot: MarketSnapshot) -> None:
        with self._engine.begin() as conn:
            conn.execute(
                _MARKET_ADVISORY_SNAPSHOTS.insert().values(
                    provider_id=snapshot.provenance.provider_id,
                    provider_version=snapshot.provenance.provider_version,
                    symbol=snapshot.symbol,
                    fetched_at=snapshot.provenance.fetched_at,
                    data_as_of=snapshot.provenance.data_as_of,
                    open_price=str(snapshot.price.open),
                    high_price=str(snapshot.price.high),
                    low_price=str(snapshot.price.low),
                    close_price=str(snapshot.price.close),
                    volume=snapshot.price.volume,
                    regime=snapshot.regime.value,
                )
            )

    def get_snapshots(
        self,
        since: datetime | None = None,
        until: datetime | None = None,
        provider_id: str | None = None,
        symbol: str | None = None,
    ) -> tuple[PersistedMarketSnapshot, ...]:
        stmt = _MARKET_ADVISORY_SNAPSHOTS.select().order_by(
            _MARKET_ADVISORY_SNAPSHOTS.c.persisted_at
        )
        if since is not None:
            stmt = stmt.where(_MARKET_ADVISORY_SNAPSHOTS.c.persisted_at >= since)
        if until is not None:
            stmt = stmt.where(_MARKET_ADVISORY_SNAPSHOTS.c.persisted_at <= until)
        if provider_id is not None:
            stmt = stmt.where(
                _MARKET_ADVISORY_SNAPSHOTS.c.provider_id == provider_id
            )
        if symbol is not None:
            stmt = stmt.where(_MARKET_ADVISORY_SNAPSHOTS.c.symbol == symbol)

        with self._engine.connect() as conn:
            rows = conn.execute(stmt).mappings().all()

        return tuple(_row_to_persisted(row) for row in rows)


def _sqlalchemy_url(database_url: str) -> str:
    if database_url.startswith("postgresql://"):
        return database_url.replace("postgresql://", "postgresql+psycopg://", 1)
    return database_url


def _row_to_persisted(row: Any) -> PersistedMarketSnapshot:
    fetched_at = cast(datetime, row["fetched_at"])
    if fetched_at.tzinfo is None:
        fetched_at = fetched_at.replace(tzinfo=UTC)

    data_as_of = cast(datetime, row["data_as_of"])
    if data_as_of.tzinfo is None:
        data_as_of = data_as_of.replace(tzinfo=UTC)

    persisted_at = cast(datetime, row["persisted_at"])
    if persisted_at.tzinfo is None:
        persisted_at = persisted_at.replace(tzinfo=UTC)

    price = PriceOHLCV(
        symbol=cast(str, row["symbol"]),
        open=Decimal(cast(str, row["open_price"])),
        high=Decimal(cast(str, row["high_price"])),
        low=Decimal(cast(str, row["low_price"])),
        close=Decimal(cast(str, row["close_price"])),
        volume=cast(int, row["volume"]),
        as_of=data_as_of,
    )
    provenance = ProviderProvenance(
        provider_id=cast(str, row["provider_id"]),
        provider_version=cast(str, row["provider_version"]),
        fetched_at=fetched_at,
        data_as_of=data_as_of,
    )
    regime_str = cast(str, row["regime"])
    try:
        regime = MarketRegime(regime_str)
    except ValueError:
        regime = MarketRegime.UNKNOWN

    snapshot = MarketSnapshot(price=price, provenance=provenance, regime=regime)
    return PersistedMarketSnapshot(
        snapshot_id=cast(int, row["snapshot_id"]),
        snapshot=snapshot,
        persisted_at=persisted_at,
    )
