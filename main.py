import argparse
import os
import time
from utils import get_xlsx_filepath, save_xlsx, email_title
from fidelity import fidelity_runner, get_fidelity_urls
from worker import (
    merge_csv_to_xlsx,
)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--id", type=str, help="id worker")
    parser.add_argument("--max", type=str, help="max worker")
    parser.add_argument("--sheet", type=str, help="sheet name")
    parser.add_argument("--url", action="store_true", help="sheet name")

    args = parser.parse_args()
    xlsx_out = get_xlsx_filepath("fidelity.xlsx")
    if args.url and args.sheet:
        url_it_end = "&sortOrder=LegalName asc&outputType=json&version=1&languageId=en-GB&currencyId=GBP&universeIds=FCGBR$$ALL_3519&securityDataPoints=SecId|Name|TenforeId|holdingTypeId|isin|sedol|QR_MonthDate|ExchangeId|ExchangeCode|Currency|CustomIsFavourite|CustomIsRecommended|LegalName|TDYNAV|AnnualReportOngoingCharge|StarRatingM255|CustomCategoryId3Name|QR_GBRReturnM12_5|QR_GBRReturnM12_4|QR_GBRReturnM12_3|QR_GBRReturnM12_2|QR_GBRReturnM12_1|CustomMinimumPurchaseAmount|TransactionFeeEstimated|PerformanceFee|GBRReturnM0|GBRReturnM12|GBRReturnM36|GBRReturnM60|GBRReturnM120|TrackRecordExtension&filters=&term=&subUniverseId=ITEI"
        url_mf_end = "&sortOrder=LegalName%20asc&outputType=json&version=1&languageId=en-GB&currencyId=GBP&universeIds=FOGBR%24%24ALL_3521&securityDataPoints=SecId%7CName%7CTenforeId%7CholdingTypeId%7Cisin%7Csedol%7CCustomAttributes1%7CCustomAttributes2%7CCustomExternalURL1%7CCustomExternalURL2%7CCustomExternalURL3%7CCustomIsClosed%7CCustomIsFavourite%7CCustomIsRecommended%7CCustomMarketCommentary%7CQR_MonthDate%7CExchangeId%7CExchangeCode%7CCurrency%7CLegalName%7CCustomBuyFee%7CYield_M12%7COngoingCostEstimated%7CCustomCategoryId3Name%7CStarRatingM255%7CQR_GBRReturnM12_5%7CQR_GBRReturnM12_4%7CQR_GBRReturnM12_3%7CQR_GBRReturnM12_2%7CQR_GBRReturnM12_1%7CCustomMinimumPurchaseAmount%7CCustomAdditionalBuyFee%7CCustomSellFee%7CTransactionFeeEstimated%7CPerformanceFee%7CGBRReturnM0%7CGBRReturnM12%7CGBRReturnM36%7CGBRReturnM60%7CGBRReturnM120%7CTrackRecordExtension&filters=&term=&subUniverseId=MFEI"
        url_etf_end = "&sortOrder=LegalName%20asc&outputType=json&version=1&languageId=en-GB&currencyId=GBP&universeIds=ETEXG%24XLON_3518%7CETALL%24%24ALL_3518&securityDataPoints=SecId%7CName%7CTenforeId%7CholdingTypeId%7Cisin%7Csedol%7CQR_MonthDate%7CCustomIsFavourite%7CCustomIsRecommended%7CExchangeId%7CExchangeCode%7CCurrency%7CLegalName%7CYield_M12%7COngoingCostEstimated%7CStarRatingM255%7CCustomCategoryId3Name%7CCollectedSRRI%7CQR_GBRReturnM12_5%7CQR_GBRReturnM12_4%7CQR_GBRReturnM12_3%7CQR_GBRReturnM12_2%7CQR_GBRReturnM12_1%7CCustomMinimumPurchaseAmount%7CTransactionFeeEstimated%7CPerformanceFee%7CGBRReturnM0%7CGBRReturnM12%7CGBRReturnM36%7CGBRReturnM60%7CGBRReturnM120%7CTrackRecordExtension&filters=&term=&subUniverseId=ETFEI"
        config = dict()
        match args.sheet:
            case "Investment":
                config.update(dict(endpoint=url_it_end, sheet="Investment"))
            case "ETF":
                config.update(dict(endpoint=url_etf_end, sheet="ETF"))
            case "MF":
                config.update(dict(endpoint=url_mf_end, sheet="MF"))
        data = get_fidelity_urls(config)
        save_xlsx(xlsx_out, data, ["name", "isin", "url"], config["sheet"])
        return

    elif args.id and args.max and args.sheet:
        fidelity_runner(id=int(args.id), max_w=int(args.max), sheet=args.sheet)
        return

    elif args.sheet:
        merge_csv_to_xlsx(
            xlsx_out, ["name", "isin", "url", "keyword"], args.sheet)
        return


if __name__ == "__main__":
    start = time.perf_counter()
    main()
    elapsed = time.perf_counter() - start
    print(f"Execution time: {elapsed:.2f} seconds.")
