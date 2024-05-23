<template>
  <el-container class="login-container">
    <el-header class="login-header">
      <!-- <img src="@/assets/logo.svg" alt="Podwise Logo" class="logo"> -->
      <h1>The premier note-taking app for podcast lovers.</h1>
    </el-header>
    <el-main class="login-form">
      <el-form>
        <el-form-item>
          <el-input v-model="email" placeholder="Email address"></el-input>
        </el-form-item>
        <el-form-item>
          <el-input v-model="password" placeholder="Your Password" type="password"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="login">Sign in</el-button>
        </el-form-item>
        <div class="other-options">
          <el-button type="info">Sign in with Google</el-button>
          <el-button type="success">Sign in with Apple</el-button>
          <el-button type="warning">Sign in with Github</el-button>
        </div>
        <div class="links">
          <a href="#">Sign up</a>
          <a href="#">Send a magic link email</a>
          <a href="#">Forgot your password?</a>
          <a href="#">Back to Home</a>
        </div>
      </el-form>
    </el-main>
  </el-container>
</template>

<script>
import { ref } from 'vue';
import axios from 'axios';

export default {
  setup() {
    const email = ref('');
    const password = ref('');

    const login = async () => {
      try {
        const response = await axios.post('/api/login', {
          email: email.value,
          password: password.value
        });
        console.log('Login Success:', response.data);
        // 根据返回的数据处理登录后的逻辑，比如页面跳转
      } catch (error) {
        console.error('Login Error:', error.response.data);
        // 处理错误，比如显示错误消息
      }
    };

    return { email, password, login };
  }
};
</script>

<style scoped>
.login-container {
  color: #fff;
  background-color: #663399;
  height: 100vh;
  display: flex;
  flex-direction: column;
}

.login-header {
  text-align: center;
  padding: 20px;
}

.logo {
  height: 50px;
}

.login-form {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
}

.other-options {
  display: flex;
  justify-content: space-between;
  margin: 20px 0;
}

.links {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
}
</style>
