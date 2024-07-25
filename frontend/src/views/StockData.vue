<template>
  <el-container>
    <el-header class="page-header">
      <el-button type="primary" @click="updateData" class="update-button">更新数据</el-button>
    </el-header>
    <el-main class="main-content">
      <el-row :gutter="20" class="toolbar">
        <el-col :span="24">
          <el-autocomplete
            v-model="stockSymbol"
            :fetch-suggestions="querySearch"
            placeholder="搜索股票"
            @select="handleSelect"
            popper-class="autocomplete-custom"
          >
            <template v-slot:suffix>
              <el-button @click="fetchStockData">搜索</el-button>
            </template>
            <template v-slot="{ item }">
              <div class="name-code">
                <span>{{ item.value }}</span>
                <span>{{ item.name }}</span>
              </div>
            </template>
          </el-autocomplete>
        </el-col>
      </el-row>
      <div v-if="stockData" class="chart-container">
        <h2>{{ stockData.name }} K 线图</h2>
        <div id="kline-chart" class="chart"></div>
      </div>
    </el-main>
  </el-container>
</template>

<script>
import axios from 'axios';
import * as echarts from 'echarts';

export default {
  data() {
    return {
      stockSymbol: '',
      stockData: null,
      allStocks: []
    };
  },
  mounted() {
    this.fetchAllStocks();
  },
  methods: {
    async fetchAllStocks() {
      try {
        const response = await axios.get('/api/all_stocks/');
        this.allStocks = response.data;
      } catch (error) {
        console.error('Failed to fetch all stocks:', error);
        this.$message.error('获取股票列表失败');
      }
    },
    querySearch(queryString, cb) {
      const results = queryString
        ? this.allStocks.filter(stock => stock.a_stock_code.includes(queryString) || stock.abbreviation.includes(queryString))
        : this.allStocks;
      cb(results.map(stock => ({
        value: stock.a_stock_code,
        name: stock.abbreviation
      })));
    },
    handleSelect(item) {
      this.stockSymbol = item.value;
    },
    async fetchStockData() {
      if (!this.stockSymbol) {
        this.$message.warning('请输入股票代码');
        return;
      }
      try {
        const response = await axios.get(`/api/stock_data/${this.stockSymbol}`);
        this.stockData = response.data;
        if (this.stockData && this.stockData.data) {
          this.$nextTick(() => {
            this.renderChart();
          });
        } else {
          this.$message.error('获取的股票数据不完整');
        }
      } catch (error) {
        console.error('Failed to fetch stock data:', error);
        this.$message.error('获取股票数据失败');
      }
    },
    async updateData() {
      try {
        await axios.post('/api/update_stock_data/');
        this.$message.success('数据更新成功');
      } catch (error) {
        console.error('Failed to update data:', error);
        this.$message.error('数据更新失败');
      }
    },
    renderChart() {
      const chartDom = document.getElementById('kline-chart');
      if (!chartDom) {
        console.error('Chart DOM element not found');
        return;
      }
      const myChart = echarts.init(chartDom);

      const dates = this.stockData.data.map(item => item.date);
      const data = this.stockData.data.map(item => [
        item.open, item.close, item.low, item.high
      ]);
      const ma5 = this.stockData.data.map(item => item.ma5);
      const ma10 = this.stockData.data.map(item => item.ma10);
      const ma20 = this.stockData.data.map(item => item.ma20);
      const nineTurnSignal = this.stockData.data.map((item, index) => item.nine_turn_signal_count !== 0 ? [index, item.nine_turn_signal_count, data[index][3]] : null).filter(item => item !== null);

      const option = {
        title: {
          text: `${this.stockData.stock_name} K 线图`,
          left: 'center'
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'cross'
          }
        },
        legend: {
          data: ['K线', 'MA5', 'MA10', 'MA20', '九转信号'],
          left: 'left'
        },
        xAxis: {
          type: 'category',
          data: dates,
          boundaryGap: false
        },
        yAxis: {
          scale: true,
          splitArea: {
            show: true
          }
        },
        dataZoom: [
          {
            type: 'slider',
            xAxisIndex: [0],
            start: 50, // 初始选择的起始位置
            end: 100 // 初始选择的结束位置
          },
          {
            type: 'inside',
            xAxisIndex: [0],
            start: 50,
            end: 100
          }
        ],
        series: [
          {
            name: 'K线',
            type: 'candlestick',
            data: data,
            itemStyle: {
              color0: '#00da3c',
              color: '#ec0000',
              borderColor0: '#008F28',
              borderColor: '#8A0000'
            }
          },
          {
            name: 'MA5',
            type: 'line',
            data: ma5,
            smooth: true,
            lineStyle: {
              color: '#FF0000', // MA5颜色
              opacity: 0.5
            },
            symbol: 'none' // 不显示圆圈标记
          },
          {
            name: 'MA10',
            type: 'line',
            data: ma10,
            smooth: true,
            lineStyle: {
              color: '#00FF00', // MA10颜色
              opacity: 0.5
            },
            symbol: 'none' // 不显示圆圈标记
          },
          {
            name: 'MA20',
            type: 'line',
            data: ma20,
            smooth: true,
            lineStyle: {
              color: '#0000FF', // MA20颜色
              opacity: 0.5
            },
            symbol: 'none' // 不显示圆圈标记
          },
          {
            name: '九转信号',
            type: 'scatter',
            data: nineTurnSignal.map(item => [item[0], item[2]]), // 将九转信号的位置与 K 线柱的高值对齐
            symbolSize: 0, // 隐藏 scatter 的点
            label: {
              show: true,
              formatter: params => nineTurnSignal.find(signal => signal[0] === params.data[0])[1],
              position: 'top',
              color: '#000'
            }
          }
        ]
      };
      myChart.setOption(option);
    }
  }
};
</script>

<style scoped>
.stock-data-page {
  height: 100vh;
  display: flex;
  flex-direction: column;
}

.page-header {
  background-color: #f5f5f5;
  padding: 20px;
  text-align: center;
  border-bottom: 1px solid #ebeef5;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.update-button {
  margin-left: 20px;
}

.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 20px;
}

.toolbar {
  margin-bottom: 20px;
  width: 100%;
  display: flex;
  justify-content: center;
}

.chart-container {
  margin-top: 20px;
  text-align: center;
  width: 100%;
  flex: 1;
}

.chart {
  width: 100%;
  height: 500px;
}

.autocomplete-custom .el-autocomplete-suggestion__wrap {
  max-height: 300px;
}

.autocomplete-custom .name-code {
  display: flex;
  justify-content: space-between;
}
</style>
