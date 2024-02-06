from pendulum import DateTime

from airflow.decorators import task, task_group
from airflow.models.taskinstance import TaskInstance
from airflow.models.dagrun import DagRun

CURRENCY_BASE_URL = "https://www.cbr.ru/currency_base/daily/"


def get_currency_rates(date: DateTime) -> list:
    import requests
    from bs4 import BeautifulSoup

    url = CURRENCY_BASE_URL
    date_str = date.strftime("%d.%m.%Y")
    params = {"UniDbQuery.Posted": "True", "UniDbQuery.To": date_str}
    response = requests.get(url, params=params)
    soup = BeautifulSoup(response.content, "html.parser")

    table = soup.find("table", attrs={"class": "data"})
    rows = table.find_all("tr")

    currency_rates = []
    for row in rows[1:]:
        columns = row.find_all("td")
        currency_code = columns[1].text
        currency_unit = int(columns[2].text)
        currency_name = columns[3].text
        currency_rate = float(columns[4].text.replace(",", "."))
        currency_rates.append(
            {
                "code": currency_code,
                "name": currency_name,
                "unit": currency_unit,
                "rate": currency_rate,
            }
        )

    return currency_rates


def get_filename(date: DateTime) -> str:
    import os

    dir = os.path.join(os.getcwd(), "var")
    if not os.path.exists(dir):
        os.makedirs(dir)
    fn = os.path.join(dir, f"cbr_{date.date()}.json")
    return fn


@task_group(group_id="cbr_rates")
def cbr_rates(dag_run: DagRun = None):

    @task.python()
    def extract(date: DateTime) -> list:
        """
        #### Extract task
        Requests data from CBR
        """
        cr: list = get_currency_rates(date)
        print(f"{len(cr)} records extracted on {date}")
        return cr

    @task.python()
    def load(currency_rates: list, filename: str):
        """
        #### Load task
        Save data to local file
        """
        import json

        with open(filename, "w", encoding="utf8") as f:
            json.dump(currency_rates, f, ensure_ascii=False)

    query_date = dag_run.logical_date if dag_run else DateTime.now()
    currency_rates = extract(date=query_date)
    load(
        currency_rates=currency_rates,
        filename=get_filename(date=query_date),
    )


# cbr_rates()

# Пример использования
if __name__ == "__main__":
    rates = get_currency_rates(DateTime.now())
    for rate in rates:
        print(rate)
