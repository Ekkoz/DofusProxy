# -*- coding: utf-8 -*-

import threading
import sqlite3
import queue
import datetime

from src.Logger import Logger

def singleton(cls):
    instance = None
    def ctor(*args, **kwargs):
        nonlocal instance
        if not instance:
            instance = cls(*args, **kwargs)
        return (instance)
    return (ctor)

@singleton
class DatabaseManager(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)

        self.condition = threading.Condition()
        self.tasks = queue.Queue()
        self.running = False

    def createDb(self):
        cursor = self.db.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS packets(id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, direction INTEGER, packet TEXT, date DATETIME);")
        self.db.commit()

    def addPacket(self, direction, packet):
        with self.condition:
            if self.running == False:
                self.running = True
                self.start()
            self.tasks.put((direction, packet))
            self.condition.notifyAll()

    def run(self):
        Logger.info("[DB] Starting the database...")
        self.db = sqlite3.connect('data.db')
        self.createDb()
        Logger.info("[DB] Waiting for data")
        while True:
            with self.condition:
                self.condition.wait()
                cursor = self.db.cursor()
                while self.tasks.empty() == False:
                    task = self.tasks.get()
                    cursor.execute("INSERT INTO packets(direction, packet, date) VALUES(?, ?, ?);", (task[0], task[1], datetime.datetime.now()))
                self.db.commit()