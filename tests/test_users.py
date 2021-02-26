import pytest
from pytest import raises
from hackthebox import HTBClient, HTBObject


@pytest.mark.asyncio
async def test_get_user(htb_client: HTBClient):
    """Tests the ability to retrieve a specific user"""
    user = await htb_client.get_user(83743)
    assert user.id == 83743
    assert user.name == "clubby789"
    print(user)


@pytest.mark.asyncio
async def test_get_non_existent_user(htb_client: HTBClient):
    """Tests for a failure upon a non existent user"""
    with raises(Exception):
        await htb_client.get_user(10000000)


@pytest.mark.asyncio
async def test_get_user_team(htb_client: HTBClient):
    """Tests retrieving a Team from a User"""
    htb_bot = await htb_client.get_user(16)
    assert htb_bot.team is not None

    # Joke account, should never have a team
    istarcheaters = await htb_client.get_user(272569)
    assert istarcheaters.team is None


@pytest.mark.asyncio
async def test_get_activity(htb_client: HTBClient):
    """Tests retrieving a user's activity"""
    activity = await (await htb_client.user).activity
    assert activity is not None
    assert isinstance(await (await (activity[0]).item), HTBObject)
