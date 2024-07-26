import akshare as ak
import pandas as pd

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
        # 获取基金基本信息
        fund_name_em_df = ak.fund_name_em()
        # 获取基金申购状态
        fund_purchase_em_df = ak.fund_purchase_em()
        # 按照基金代码合并，并只保留两个 DataFrame 中都有的基金代码
        merged_df = pd.merge(fund_name_em_df, fund_purchase_em_df, on="基金代码", how="inner", suffixes=('', '_duplicate'))

        # 删除所有带有 '_duplicate' 后缀的列
        merged_df = merged_df.loc[:, ~merged_df.columns.str.endswith('_duplicate')]


        print(merged_df)
        html = merged_df.to_html()
        with open('merged_dataframe.html', 'w') as f:
            f.write(html)
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
        return fund_name_em_df.to_dict(orient="records")


if __name__ == "__main__":
    fund_data_provider = AkshareFundDataProvider()
    fund_data = fund_data_provider.get_fund_data()
    # print(fund_data)
    fund_purchase_em_df = ak.fund_purchase_em()
    # print(fund_purchase_em_df)
    for item in fund_data:
        try:
            pass
            # fund_individual_basic_info_xq_df = ak.fund_individual_basic_info_xq(
            #     symbol=item['symbol']
            # )
            # print(fund_individual_basic_info_xq_df)
        except Exception as e:
            print(e)
