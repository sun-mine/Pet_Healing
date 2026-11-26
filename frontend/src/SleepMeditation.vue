<script setup>
import { computed, ref } from 'vue'
import PetAvatar from './PetAvatar.vue'
import cues from './meditation-cues.json'

defineProps({ pet: { type: Object, required: true }, outfit: { type: Object, required: true } })
const emit = defineEmits(['close'])

const stage = ref('intro')
const audio = ref(null)
const playing = ref(false)
const position = ref(0)
const duration = ref(0)
const cueIndex = computed(() => cues.findLastIndex((cue) => cue.start <= position.value))

function formatTime(seconds) {
  const whole = Math.floor(seconds)
  return `${Math.floor(whole / 60)}:${String(whole % 60).padStart(2, '0')}`
}

function start() {
  audio.value.currentTime = 0
  position.value = 0
  stage.value = 'session'
  audio.value.play()
}

function togglePlayback() {
  if (audio.value.paused) audio.value.play()
  else audio.value.pause()
}

function seek(seconds) {
  const next = Math.min(Math.max(seconds, 0), duration.value)
  audio.value.currentTime = next
  position.value = next
  if (next === duration.value) finish()
}

function moveCue(offset) {
  const index = Math.min(Math.max(cueIndex.value + offset, 0), cues.length - 1)
  seek(cues[index].start)
}

function finish() {
  audio.value.pause()
  stage.value = 'complete'
}

function back() {
  if (stage.value === 'session') {
    audio.value.pause()
    stage.value = 'intro'
  } else {
    emit('close')
  }
}
</script>

<template>
  <section class="meditation" :class="`meditation--${stage}`" aria-label="助眠冥想">
    <button class="back-button" type="button" aria-label="返回" @click="back"><span aria-hidden="true"></span></button>
    <audio
      ref="audio"
      src="/audio/sleep-meditation.wav"
      preload="metadata"
      @loadedmetadata="duration = audio.duration"
      @timeupdate="position = audio.currentTime"
      @play="playing = true"
      @pause="playing = false"
      @ended="finish"
    ></audio>

    <template v-if="stage === 'intro'">
      <div class="meditation-intro notice-card">
        <h1 class="notice-title">助眠冥想</h1>
        <p>找一个安静、舒服的地方，跟着语音把注意力放回呼吸，慢慢放松身体。</p>
      </div>
      <button class="primary-button meditation-start" type="button" @click="start">开始</button>
    </template>

    <template v-else-if="stage === 'session'">
      <h1 class="meditation-title">助眠冥想</h1>
      <p class="meditation-cue">{{ cues[cueIndex].text }}</p>
      <div class="meditation-pet"><PetAvatar :pet="pet" :outfit="outfit" /></div>
      <div class="meditation-player">
        <label class="sr-only" for="meditation-progress">播放进度</label>
        <input id="meditation-progress" type="range" min="0" :max="duration" step="any" :value="position"
          :aria-valuetext="formatTime(position)" :disabled="!duration" @input="seek($event.target.valueAsNumber)" />
        <div class="meditation-times"><span>{{ formatTime(position) }}</span><span>{{ formatTime(duration) }}</span></div>
        <div class="meditation-controls">
          <button type="button" aria-label="后退十秒" :disabled="!duration" @click="seek(position - 10)">↶<small>10</small></button>
          <button type="button" aria-label="上一段" :disabled="!duration" @click="moveCue(-1)">❮❮</button>
          <button class="meditation-play" type="button" :aria-label="playing ? '暂停' : '播放'" @click="togglePlayback">
            {{ playing ? 'Ⅱ' : '▶' }}
          </button>
          <button type="button" aria-label="下一段" :disabled="!duration" @click="moveCue(1)">❯❯</button>
          <button type="button" aria-label="前进十秒" :disabled="!duration" @click="seek(position + 10)">↷<small>10</small></button>
        </div>
      </div>
    </template>

    <template v-else>
      <div class="meditation-pet"><PetAvatar :pet="pet" :outfit="outfit" /></div>
      <div class="meditation-result">
        <span class="meditation-check" aria-hidden="true"></span>
        <h1>恭喜你完成了助眠练习</h1>
        <button class="primary-button" type="button" @click="$emit('close')">完成</button>
      </div>
    </template>
  </section>
</template>

<style scoped>
.meditation {
  position: relative;
  height: max(620px, 100svh);
  overflow: hidden;
  background: #fff;
  text-align: center;
}

.meditation-intro { position: absolute; top: 25%; padding: 60px 15%; text-align: center; }
.meditation-start { position: absolute; bottom: 17%; left: 50%; translate: -50% 0; }
.meditation-start, .meditation-result .primary-button { background: #94b75a; }

.meditation-title {
  position: absolute;
  top: 6%;
  left: 50%;
  padding: 11px 25px;
  border-radius: 24px;
  background: #94b75a;
  font-size: 1rem;
  font-weight: 500;
  translate: -50% 0;
}

.meditation-cue {
  position: absolute;
  top: 24%;
  left: 50%;
  width: 73%;
  padding: 23px 16px;
  border-radius: 36px;
  background: var(--green);
  line-height: 1.5;
  translate: -50% 0;
}

.meditation-cue::after {
  content: '';
  position: absolute;
  top: calc(100% - 8px);
  left: 44%;
  width: 20px;
  height: 20px;
  border-radius: 4px;
  background: var(--green);
  rotate: 45deg;
}

.meditation-pet {
  position: absolute;
  top: 40%;
  left: 50%;
  z-index: 1;
  width: min(75%, 43svh);
  translate: -50% 0;
}

.meditation-pet::before {
  content: '';
  position: absolute;
  inset: 81% 16% 2%;
  border-radius: 51% 49% 41% 44%;
  background: radial-gradient(ellipse at 50% 26%, #acc975, #8eac51 72%);
}

.meditation-player { position: absolute; inset: auto 7% 5%; }
.meditation-player input { width: 100%; margin: 0; accent-color: #bd5c77; }
.meditation-times { display: flex; justify-content: space-between; font-size: .78rem; }
.meditation-controls { display: flex; align-items: center; justify-content: space-between; gap: 4px; margin-top: 7px; }
.meditation-controls button { min-width: 44px; min-height: 44px; border-radius: 50%; color: #426f31; background: transparent; font-size: 1.15rem; }
.meditation-controls small { font-size: .69rem; }
.meditation-controls .meditation-play { width: 50px; height: 50px; background: var(--green); }

.meditation--complete .meditation-pet { top: 9%; width: min(62%, 36svh); }
.meditation-result {
  position: absolute;
  inset: 36% 0 0;
  display: grid;
  align-content: center;
  justify-items: center;
  gap: 24px;
  border-radius: 45px 45px 0 0;
  background: #fff6bc url('/images/onboarding-background.png') center / cover;
}
.meditation-result h1 { font-size: 1.05rem; font-weight: 500; }
.meditation-check { display: grid; width: 88px; height: 88px; place-items: center; border: 11px solid #f3a8ba; border-radius: 50%; }
.meditation-check::after { content: ''; width: 34px; height: 17px; border: solid var(--leaf); border-width: 0 0 7px 7px; rotate: -45deg; }
</style>
