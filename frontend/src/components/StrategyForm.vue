<template>
  <el-form :model="form" :rules="rules" ref="form" label-width="100px">
    <el-form-item label="数据源" prop="dataSource">
      <el-select v-model="form.dataSource" placeholder="请选择数据源">
        <el-option label="数据源 1" value="source1"></el-option>
        <el-option label="数据源 2" value="source2"></el-option>
        <el-option label="数据源 3" value="source3"></el-option>
      </el-select>
    </el-form-item>
    <el-form-item label="策略名称" prop="strategyName">
      <el-input v-model="form.strategyName"></el-input>
    </el-form-item>
    <el-form-item label="初始资金" prop="initialCash">
      <el-input v-model="form.initialCash"></el-input>
    </el-form-item>
    <el-form-item label="开始日期" prop="startDate">
      <el-date-picker v-model="form.startDate" type="date"></el-date-picker>
    </el-form-item>
    <el-form-item label="结束日期" prop="endDate">
      <el-date-picker v-model="form.endDate" type="date"></el-date-picker>
    </el-form-item>
    <el-form-item>
      <el-button type="primary" @click="submitForm">提交</el-button>
    </el-form-item>
    <el-dialog v-model:visible="loading" title="加载中" center>
      <span>策略执行中，请稍候...</span>
    </el-dialog>
  </el-form>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      form: {
        dataSource: '',
        strategyName: '',
        initialCash: '',
        startDate: '',
        endDate: ''
      },
      rules: {
        dataSource: [
          { required: true, message: '请选择数据源', trigger: 'change' }
        ],
        strategyName: [
          { required: true, message: '请输入策略名称', trigger: 'blur' }
        ],
        initialCash: [
          { required: true, message: '请输入初始资金', trigger: 'blur' },
          { type: 'number', message: '初始资金必须为数字', trigger: 'blur' }
        ],
        startDate: [
          { type: 'date', required: true, message: '请选择开始日期', trigger: 'change' }
        ],
        endDate: [
          { type: 'date', required: true, message: '请选择结束日期', trigger: 'change'}
        ]
      },
      loading: false
    };
  },
  methods: {
    async submitForm() {
      this.$refs.form.validate(async (valid) => {
        if (valid) {
          try {
            this.loading = true;
            const response = await axios.post('/api/execute_strategy', this.form);
            this.loading = false;
            this.$router.push({name: 'result', query: {id: response.data.id}});
          } catch (error) {
            this.loading = false;
            this.$message.error('策略执行失败，请重试');
            console.error('Failed to execute strategy:', error);
          }
        } else {
          this.$message.error('表单校验失败，请检查输入项');
        }
      });
    }
  }
};
</script>
