<script setup>
  import LoginButton from "@/components/LoginButton.vue"

  const handleLogin = () => {
    window.location.href = "http://localhost:8000/auth/login"
  }
</script>

<template>
  <LoginButton />
  <h2>バックエンド(開発中)</h2>
  <button @click="handleLogin">LINEでログイン</button>
</template>
