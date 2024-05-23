<template>
    <el-container>
      <el-header class="page-header">
        <el-button type="primary" @click="updateData" class="update-button">更新数据</el-button>
      </el-header>
      <el-main class="main-content">
        <el-row :gutter="20" class="toolbar">
          <el-col :span="24">
            <el-input v-model="stockSymbol" placeholder="搜索股票" @keyup.enter="fetchStockData">
              <template v-slot:append>
                <el-button @click="fetchStockData">搜索</el-button>
              </template>
            </el-input>
          </el-col>
        </el-row>
        <div v-if="stockData" class="chart-container">
          <h2>{{ stockSymbol }} K 线图</h2>
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
      stockData: null
    };
  },
  methods: {
    async fetchStockData() {
      if (!this.stockSymbol) {
        this.$message.warning('请输入股票代码');
        return;
      }
      try {
        const response = await axios.get(`/api/stock_data/${this.stockSymbol}`);
        this.stockData = response.data;
        if (this.stockData && this.stockData.dates && this.stockData.prices) {
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
        await axios.post('/api/update_stock_data');
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
      const option = {
        title: {
          text: 'K 线图',
          left: 'center'
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'cross'
          }
        },
        xAxis: {
          type: 'category',
          data: this.stockData.dates,
          boundaryGap: false
        },
        yAxis: {
          scale: true,
          splitArea: {
            show: true
          }
        },
        series: [
          {
            name: 'K线',
            type: 'candlestick',
            data: this.stockData.prices,
            itemStyle: {
              color: '#00da3c',
              color0: '#ec0000',
              borderColor: '#008F28',
              borderColor0: '#8A0000'
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
</style>
