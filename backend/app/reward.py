from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.transaction import Base


class Reward(Base):
    __tablename__ = "rewards"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True,
    )

    description: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    coin_cost: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    active: Mapped[bool] = mapped_column(
        nullable=False,
        default=True,
    )


class RewardRedemption(Base):
    __tablename__ = "reward_redemptions"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    reward_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    coin_cost: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.utcnow,
    )
