import pendulum

from airflow.decorators import dag

from my_company.tasks.cbr import cbr_rates


@dag(
    schedule="@daily",
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup=False,
    tags=["test"],
)
def test_cbr_to_file():
    """
    ### Loads cbr rates to file
    """
    tg = cbr_rates()


test_cbr_to_file()
