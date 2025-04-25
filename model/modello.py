from database.DAO import DAO


class Model:
    def __init__(self):
        self._solBest = []
        self._clientiMaxBest = 0
        self._listNerc = None
        self._listEvents = None
        self.loadNerc()



    def worstCase(self, nerc, maxY, maxH):
        self.loadEvents(nerc)
        parziale = []
        self.ricorsione([], maxY, maxH, 0)
        print(self._solBest)

    def ricorsione(self, parziale, maxY, maxH, pos):
        # terminazione
        if self.sumDurata(parziale) / 60 / 60 > maxH:  # self.getRangeAnni(parziale) > maxY or
            # print(f"Range{self.getRangeAnni(parziale)}")
            # print('durata: ', self.sumDurata(parziale))
            #
            # print(f"Max{maxH*60*60}")
            return

        # verifica se best
        if self.calcola_tot_persone(parziale) > self._clientiMaxBest:
            self._solBest = parziale[:]
            self._clientiMaxBest = self.calcola_tot_persone(parziale)

        # ricorsione
        i = pos
        for e in self._listEvents[pos:]:  # i, e in enumerate(self._listEvents[pos:]):
            parziale.append(e)
            if self.getRangeAnni(parziale) > maxY:
                parziale.remove(e)
                return
            i += 1
            self.ricorsione(parziale, maxY, maxH, i)
            parziale.remove(e)

    def getRangeAnni(self, listOutages):
        if len(listOutages) < 2:
            return 0

        first = listOutages[0].date_event_began
        last = listOutages[-1].date_event_finished
        return int(last.year - first.year)

    def calcola_tot_persone(self, listOutages):
        if len(listOutages) == 0:
            return 0

        numCustomers = 0
        for event in listOutages:
            numCustomers += event.customers_affected
        return numCustomers

    def loadEvents(self, nerc):
        self._listEvents = DAO.getAllEvents(nerc.value)

    def loadNerc(self):
        self._listNerc = DAO.getAllNerc()

    def sumDurata(self, listOutages):
        if len(listOutages) == 0:
            return 0

        sum = 0
        for i in listOutages:
            sum += self.durata(i)
        return sum

    def durata(self, event):
        return (event.date_event_finished-event.date_event_began).total_seconds()

    @property
    def listNerc(self):
        return self._listNerc