<script setup>
import { ref } from 'vue'

const apiBase = import.meta.env.VITE_API_BASE_URL || '/api'
const status = ref('未检测')
const checking = ref(false)

async function checkHealth() {
  checking.value = true
  try {
    const res = await fetch(`${apiBase}/health`)
    const data = await res.json()
    status.value = data.status === 'ok' ? '后端连接正常' : '后端返回异常'
  } catch (err) {
    status.value = '后端连接失败'
  } finally {
    checking.value = false
  }
}
</script>

<template>
  <main class="page">
    <img class="hero" src="/images/hero.jpg" alt="Pet Healing" />
    <h1>Pet Healing</h1>
    <p>宠物健康与治愈服务平台</p>
    <button :disabled="checking" @click="checkHealth">
      {{ checking ? '检测中…' : '检测后端接口' }}
    </button>
    <p class="status">{{ status }}</p>
  </main>
</template>
