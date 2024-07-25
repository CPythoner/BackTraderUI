<template>
  <el-card>
    <div id="chart"></div>
  </el-card>
</template>

<script>
import * as echarts from 'echarts';

export default {
  props: ['data'],
  mounted() {
    this.renderChart();
  },
  methods: {
    renderChart() {
      const chart = echarts.init(document.getElementById('chart'));
      const option = {
        xAxis: {
          type: 'category',
          data: this.data.dates
        },
        yAxis: {
          type: 'value'
        },
        series: [
          {
            data: this.data.values,
            type: 'line'
          }
        ]
      };
      chart.setOption(option);
    }
  }
};
</script>

<style>
#chart {
  width: 100%;
  height: 400px;
}
</style>
