from app.dao.base import BaseDAO
from app.incidents.models import IncidentModel


class IncidentsDAO(BaseDAO):
    model = IncidentModel

    async def get_incidents_info(visor_id: int, event_id: int):
        ...
        # query = (
        #     session.query(
        #         Incident,
        #         Teacher.name.label('current_teacher'),
        #         Group.name.label('current_group'),
        #         Schedule.subject.label('current_schedule'),
        #         Classroom.name.label('current_classroom'),
        #         User.full_name.label('current_visor')
        #     )
        #     .join(Schedule, Incident.event == Schedule.id)
        #     .join(Classroom, Schedule.classroom_id == Classroom.id)
        #     .join(Teacher, Schedule.teacher_id == Teacher.id)
        #     .join(Group, Schedule.group_id == Group.id)
        #     .join(User, Incident.visor_id == User.id)
        #     .filter(Incident.visor_id == 1, Incident.event == 4)
        # )