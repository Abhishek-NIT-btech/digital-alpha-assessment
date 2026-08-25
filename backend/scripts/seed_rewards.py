from app.database import SessionLocal
from app.reward import Reward


REWARDS = [
    {
        "name": "Amazon ₹500 Voucher",
        "description": "Amazon shopping voucher worth ₹500.",
        "coin_cost": 5000,
    },
    {
        "name": "Swiggy ₹250 Voucher",
        "description": "Swiggy voucher worth ₹250.",
        "coin_cost": 2500,
    },
    {
        "name": "Myntra ₹500 Voucher",
        "description": "Myntra shopping voucher worth ₹500.",
        "coin_cost": 5000,
    },
    {
        "name": "Cashback ₹100",
        "description": "₹100 cashback reward.",
        "coin_cost": 1000,
    },
    {
        "name": "Movie Ticket",
        "description": "Reward voucher for a movie ticket.",
        "coin_cost": 2000,
    },
    {
        "name": "Food Delivery ₹200 Voucher",
        "description": "Food delivery voucher worth ₹200.",
        "coin_cost": 2000,
    },
]


def seed_rewards():
    db = SessionLocal()

    try:
        existing = db.query(Reward).count()

        if existing > 0:
            print(f"Rewards already seeded: {existing}")
            return

        for reward_data in REWARDS:
            db.add(
                Reward(**reward_data)
            )

        db.commit()

        print(
            f"Successfully seeded {len(REWARDS)} rewards."
        )

    finally:
        db.close()


if __name__ == "__main__":
    seed_rewards()
