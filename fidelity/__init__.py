import math
from fidelity.keyword import get_fidelity_keyword
from utils import delay, setup_driver
import curl_cffi

from worker import get_data_by_worker_id, get_xlsx_data, write_csv_by_id


def fidelity_runner(id: int, max_w: int, sheet: str) -> None:
    driver = setup_driver(True)
    data = get_xlsx_data("fidelity.xlsx", sheet)
    funds_per_worker = get_data_by_worker_id(id, max_w, data)
    funds_per_worker = get_fidelity_keyword(driver, funds_per_worker)
    csv = f"fidelity_{id}_{sheet.lower()}.csv"
    write_csv_by_id(
        csv,
        funds_per_worker,
        [
            "index",
            "name",
            "isin",
            "url",
            "keyword",
            "sheet",
        ])
    driver.quit()


def get_fidelity_urls(config: dict) -> list[dict]:
    urls = []
    endpoint_start = "https://lt.morningstar.com/api/rest.svc/9vehuxllxs/security/screener?"
    pagination = f"page={1}&pageSize={1}"
    endpoint = config["endpoint"]
    api_url = f"{endpoint_start}{pagination}{endpoint}"
    res = curl_cffi.get(api_url, impersonate='chrome')
    total = res.json()
    total_funds = int(total["total"])
    size = 100
    total_pages = math.ceil(total_funds / size)
    sheet = config["sheet"]
    print(f'[Fidelity] Total {sheet} = {total_funds}\n')

    for page in range(1, total_pages + 1):
        print(f'[#] Fidelity {sheet} Page {page}/{total_pages} [#]')
        pagination = f"page={page}&pageSize={size}"
        current_url = f"{endpoint_start}{pagination}{config['endpoint']}"
        res = curl_cffi.get(current_url, impersonate='chrome')
        page_rows = res.json()["rows"]
        for row in page_rows:
            name = row["LegalName"]
            url = f'https://www.fidelity.co.uk/factsheets?id={row["SecId"]}&idCurrencyId=&idType=msid&marketCode=&intref=pi_tool_investment-finder'
            isin = row["isin"]
            urls.append(dict(name=name, isin=isin, url=url, sheet=sheet))
        delay(1, 3)

    return urls
