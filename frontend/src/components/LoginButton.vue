<template>
  <button @click="handleLogin"><img src="@/assets/btn_login_base.png" alt="LINEでログイン" /></button>
</template>

<script>
import { useAuth } from "@/composables/useAuth";

export default {
  setup() {
    const { login } = useAuth();

    function handleLogin() {
      login();
    }

    return {
      handleLogin,
    };
  },
};
</script>
