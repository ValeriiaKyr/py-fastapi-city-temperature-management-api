from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from city import schemas, models


async def get_all_cities(db: AsyncSession):
    query = select(models.City)
    result = await db.execute(query)
    cities_list = result.scalars().all()
    return cities_list


async def create_city(db: AsyncSession, city: schemas.CityBase):
    new_city = models.City(name=city.name, additional_info=city.additional_info)
    db.add(new_city)
    await db.commit()
    await db.refresh(new_city)
    return new_city


async def get_city(db: AsyncSession, city_id: int):
    return await db.get(models.City, city_id)


async def delete_city(db: AsyncSession, city_id: int):
    city = await get_city(db, city_id)
    if city:
        await db.delete(city)
        await db.commit()
        return city

    return None