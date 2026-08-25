from typing import List

from pydantic import BaseModel, ConfigDict


class RewardResponse(BaseModel):
    id: int
    name: str
    description: str
    coin_cost: int
    active: bool

    model_config = ConfigDict(from_attributes=True)


class RewardListResponse(BaseModel):
    items: List[RewardResponse]


class RewardBalanceResponse(BaseModel):
    balance: int
    earned_coins: int
    redeemed_coins: int


class RewardRedeemRequest(BaseModel):
    reward_id: int


class RewardRedeemResponse(BaseModel):
    success: bool
    message: str
    reward: RewardResponse
    coins_spent: int
    remaining_balance: int
