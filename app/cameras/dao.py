import logging
from sqlalchemy import func, select
from sqlalchemy.exc import SQLAlchemyError
from app.database import async_session_maker
from app.buildings.models import BuildingModel
from app.cameras.models import CameraModel
from app.classrooms.models import ClassroomModel
from app.dao.base import BaseDAO
from app.utils.filter_factory import filter_factory


class CamerasDAO(BaseDAO):
    model = CameraModel

    @classmethod
    async def find_all(cls, **filter_by):
        filter_mapping = {
            "classroom_id": ClassroomModel.id,
            "building_id": BuildingModel.id,
            "camera_ip": CameraModel.camera_ip,
            "reg_ip": CameraModel.reg_ip,
            "view": CameraModel.view,
            "camera_type": CameraModel.camera_type,
        }
        conditions = filter_factory(filter_mapping, filter_by)

        try:
            query = (
                select(
                    CameraModel.__table__,
                    ClassroomModel.name.label("classroom_name"),
                    BuildingModel.id.label("building_id"),
                    BuildingModel.name.label("building_name"),
                )
                .select_from(CameraModel)
                .join(ClassroomModel, CameraModel.classroom_id == ClassroomModel.id)
                .join(BuildingModel, ClassroomModel.building_id == BuildingModel.id)
                .filter(*conditions)
            )
            async with async_session_maker() as session:
                result = await session.execute(query)
                return result.mappings().all()
        except (SQLAlchemyError, Exception) as e:
            if isinstance(e, SQLAlchemyError):
                msg = "Database Exc: Data not found"
            elif isinstance(e, Exception):
                msg = "Unknown Exc: Data not found"

            logging.error(msg, extra={"table": cls.model.__tablename__}, exc_info=True)
            return None

    @classmethod
    async def find_all_count(cls, **filter_by):
        filter_mapping = {
            "classroom_id": ClassroomModel.id,
            "building_id": BuildingModel.id,
            "camera_ip": CameraModel.camera_ip,
            "reg_ip": CameraModel.reg_ip,
            "view": CameraModel.view,
            "camera_type": CameraModel.camera_type,
        }
        conditions = filter_factory(filter_mapping, filter_by)

        try:
            query = (
                select(
                    func.count(CameraModel.id),
                )
                .select_from(CameraModel)
                .join(ClassroomModel, CameraModel.classroom_id == ClassroomModel.id)
                .join(BuildingModel, ClassroomModel.building_id == BuildingModel.id)
                .filter(*conditions)
            )
            async with async_session_maker() as session:
                result = await session.execute(query)
                return result.scalar()
        except (SQLAlchemyError, Exception) as e:
            if isinstance(e, SQLAlchemyError):
                msg = "Database Exc: Data not found"
            elif isinstance(e, Exception):
                msg = "Unknown Exc: Data not found"

            logging.error(msg, extra={"table": cls.model.__tablename__}, exc_info=True)
            return None