<template>
  <div>
    <h1>近くの神社を検索</h1>
    <div v-if="loading">ロード中...</div>
    <div v-if="error">{{ error }}</div>
    <div v-if="!loading && !error && shrines.length > 0">
      <h2>参拝したい神社を選択してください</h2>
      <ul>
        <li v-for="shrine in shrines" :key="shrine.name">
          <button class="shrine-button" @click="selectShrine(shrine)">
            {{ shrine.name }} ： {{ shrine.distance }}
          </button>
        </li>
      </ul>
    </div>
    <div v-if="selectedShrine">
      <h2>選択した神社:</h2>
      <p><strong>名前:</strong> {{ selectedShrine.name }}</p>
      <p><strong>住所:</strong> {{ selectedShrine.address }}</p>
    </div>
    <div v-if="!loading && !error && shrines.length === 0">神社が見つかりませんでした。</div>
  </div>
</template>

<script>
import apiAxios from "@/plugin/axios";

export default {
  data() {
    return {
      shrines: [], // 取得した神社のリスト
      selectedShrine: null, // 選択された神社
      loading: false, // ロード中フラグ
      error: null, // エラーメッセージ
    };
  },
  created() {
    // ページが表示されたときに神社を取得
    this.getLocation();
  },
  methods: {
    async getLocation() {
      if (navigator.geolocation) {
        this.loading = true;
        this.error = null;
        this.shrines = [];
        this.selectedShrine = null;

        navigator.geolocation.getCurrentPosition(
          async (position) => {
            const latitude = position.coords.latitude;
            const longitude = position.coords.longitude;

            try {
              const response = await apiAxios.get(
                "/api/location",
                { params: { latitude, longitude } }
              );
              if (response.data && response.data.shrines) {
                // 必要なデータだけを保持
                this.shrines = response.data.shrines.map((shrine) => ({
                  name: shrine.name,
                  address: shrine.address,
                  distance: shrine.distance,
                }));
              } else {
                this.error = "データの取得に失敗しました。";
              }
            } catch (err) {
              this.error = "サーバーとの通信に失敗しました。";
            } finally {
              this.loading = false;
            }
          },
          (error) => {
            this.error = "位置情報の取得に失敗しました。";
            this.loading = false;
          }
        );
      } else {
        this.error = "位置情報が利用できません。";
      }
    },
    selectShrine(shrine) {
      // 選択された神社を更新
      this.selectedShrine = shrine;
    },
  },
};
</script>

<style scoped>
h1 {
  font-size: 1.5em;
  margin-bottom: 1em;
}

button {
  padding: 0.5em 1em;
  font-size: 1em;
  cursor: pointer;
  margin-bottom: 1em;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  margin: 0.5em 0;
}

.shrine-button {
  display: inline-block; /* インラインブロックで幅を調整 */
  font-size: 1em;
  padding: 0.75em 1.5em;
  text-align: center;
  background-color: #f9f9f9;
  border: 1px solid #ccc;
  border-radius: 5px;
  cursor: pointer;
  width: auto; /* 自動調整 */
  white-space: nowrap; /* テキストが改行されないようにする */
}

.shrine-button:hover {
  background-color: #e6e6e6;
}

ul {
  display: flex;
  flex-direction: column;
  align-items: flex-start; /* ボタンを左揃え */
}

strong {
  margin-right: 0.5em;
}
</style>
