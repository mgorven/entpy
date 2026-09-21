import asyncio

from entpy import db
from evc import ExampleViewerContext
from generated.ent_test_object import EntTestObject, EntTestObjectExample


async def gen_locked(vc: ExampleViewerContext) -> asyncio.Lock:
    obj = await EntTestObjectExample.gen_create(vc)
    await EntTestObject.gen(vc, obj.id, for_update=True)
    (lock,) = db.session.info["for_update"]
    assert lock.locked()
    return lock


async def test_release_on_commit(vc: ExampleViewerContext) -> None:
    lock = await gen_locked(vc)
    await db.session.commit()
    assert not lock.locked()
    assert "for_update" not in db.session.info


async def test_release_on_rollback(vc: ExampleViewerContext) -> None:
    lock = await gen_locked(vc)
    await db.session.rollback()
    assert not lock.locked()
    assert "for_update" not in db.session.info


async def test_release_on_close(vc: ExampleViewerContext) -> None:
    lock = await gen_locked(vc)
    await db.session.close()
    assert not lock.locked()
    assert "for_update" not in db.session.info


async def test_savepoint_commit_keeps_lock(vc: ExampleViewerContext) -> None:
    lock = await gen_locked(vc)
    async with db.session.begin_nested():
        await EntTestObjectExample.gen_create(vc)
    assert lock.locked()
    await db.session.commit()
    assert not lock.locked()
