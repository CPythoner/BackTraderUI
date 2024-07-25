import akshare as ak

class FundDataProvider(object):
    """
    基金数据提供器的基类
    """
    def __init__(self):
        pass

    def get_fund_data(self):
        """
        获取基金数据
        :return: 所有基金的名称和类型
        """
        pass


class AkshareFundDataProvider(FundDataProvider):

    def get_fund_data(self):
        fund_name_em_df = ak.fund_name_em()
        # 替换列名
        fund_name_em_df.rename(
            columns={
                "基金代码": "symbol",
                "拼音缩写": "abbreviation",
                "基金简称": "short_name",
                "基金类型": "type",
                "拼音全称": "full_name",
            },
            inplace=True,
        )
        # 将 DataFrame 转换为字典列表
        return fund_name_em_df.to_dict(orient="records")


if __name__ == "__main__":
    fund_data_provider = AkshareFundDataProvider()
    fund_data = fund_data_provider.get_fund_data()
    print(fund_data[1])
    for item in fund_data:
        try:
            pass
            # fund_individual_basic_info_xq_df = ak.fund_individual_basic_info_xq(
            #     symbol=item['symbol']
            # )
            # print(fund_individual_basic_info_xq_df)
        except Exception as e:
            print(e)
