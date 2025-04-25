from database.DB_connect import DBConnect
from model.nerc import Nerc
from model.powerOutages import Event


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getAllNerc():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT * 
        FROM NERC n
        """

        cursor.execute(query)

        for row in cursor:
            result.append(Nerc(row["id"], row["value"]))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllEvents(nerc):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT p.id AS pid, p.event_type_id, p.tag_id, p.area_id, p.nerc_id, 
       p.responsible_id, p.customers_affected, 
       p.date_event_began, p.date_event_finished, p.demand_loss
            FROM POWEROUTAGES p, NERC n
            WHERE n.value = %s and p.nerc_id = n.id
            order by p.date_event_began"""

        cursor.execute(query, (nerc,))

        for row in cursor:
            result.append(
                Event(row["pid"], row["event_type_id"],
                      row["tag_id"], row["area_id"],
                      row["nerc_id"], row["responsible_id"],
                      row["customers_affected"], row["date_event_began"],
                      row["date_event_finished"], row["demand_loss"]))

        cursor.close()
        conn.close()
        return result


if __name__ == '__main__':
    DAO = DAO()
    print(DAO.getAllEvents("MAAC"))

