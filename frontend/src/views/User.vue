<script setup>
import { ref, onMounted } from 'vue';
import apiAxios from "@/plugin/axios";

const user = ref(null);
const loading = ref(true); // ローディング状態
const error = ref(null); // エラー情報

const fetchUser = async () => {
  try {
    const response = await apiAxios.get('/api/users/me/profile');
    user.value = response.data;
  } catch (err) {
    error.value = 'Failed to load user information.';
    console.error(err);
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  fetchUser();
});
</script>


<template>
  <div>
    <h1>User Information</h1>
    <div v-if="loading">Loading...</div>
    <div v-else-if="error">{{ error }}</div>
    <div v-else>
      <p><strong>ID:</strong> {{ user.id }}</p>
      <p><strong>Name:</strong> {{ user.name }}</p>
      <img :src="user.picture" alt="profile">
    </div>
  </div>
</template>

