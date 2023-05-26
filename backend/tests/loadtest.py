import gevent
import os
import numpy.random as rand
import pandas as pd
from locust import FastHttpUser, task, events
from locust.env import Environment
from locust.stats import stats_printer, stats_history, StatsCSVFileWriter
from locust.log import setup_logging
from matplotlib import pyplot as plt


setup_logging("INFO", None)


class BuyhardwareUser(FastHttpUser):
    host = "http://localhost:8888"

    @task
    def t(self):
        self.client.get("/hardware")


def start_locust(time_hh: int, time_mm: int, time_ss: int, user: int, spawn_rate: int):
    # setup Environment and Runner
    env = Environment(user_classes=[BuyhardwareUser])
    env.create_local_runner()

    # CSV writer
    stats_path = os.path.join(os.getcwd(), "data")
    csv_writer = StatsCSVFileWriter(
        environment=env,
        base_filepath=stats_path,
        full_history=True,
        percentiles_to_report=[90.0, 95.0]
    )

    # Writing all the stats to a CSV file
    gevent.spawn(csv_writer.stats_writer)

    # start a WebUI instance
    env.create_web_ui(host="127.0.0.1", port=8089, stats_csv_writer=csv_writer)

    # start a greenlet that periodically outputs the current stats
    # gevent.spawn(stats_printer(env.stats))

    # start a greenlet that saves current stats to history
    gevent.spawn(stats_history, env.runner)

    # start the test
    env.runner.start(user_count=user, spawn_rate=spawn_rate)

    # stop the runner in a given time
    time_in_seconds = (time_hh * 60 * 60) + (time_mm * 60) + time_ss
    gevent.spawn_later(time_in_seconds, lambda: env.runner.quit())

    # wait for the greenlets
    env.runner.greenlet.join()

    # stop the web server for good measures
    env.web_ui.stop()


users_num = [10, 25, 50, 100, 250]


for i, n in enumerate(users_num):
    start_locust(0, 0, 10, n, n / 10)
    df = pd.read_csv("data_stats_history.csv")
    plt.plot(df["Total Request Count"], df["Total Average Response Time"])
    plt.title("Статистика запросов")
    plt.xlabel("Запросы")
    plt.ylabel("Время отклика")
    plt.savefig("requests_"+str(i)+".png")
