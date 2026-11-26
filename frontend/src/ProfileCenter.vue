<script setup>
import { computed, ref } from 'vue'

const props = defineProps({ nickname: String, petName: { type: String, required: true } })
const emit = defineEmits(['help', 'save', 'redesign'])

const weekdays = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
const moods = ['舒适', '骄傲', '无聊', '开心', '伤心', '生气']
const sampleMoods = [4, 2, 3, 1, 0, 0, 0]
const week = ref(0)
const weekDates = computed(() => {
  const monday = new Date()
  monday.setDate(monday.getDate() - (monday.getDay() + 6) % 7 + week.value * 7)
  return weekdays.map((_, day) => {
    const date = new Date(monday)
    date.setDate(monday.getDate() + day)
    return date
  })
})
const weekTitle = computed(() => {
  const [start, , , , , , end] = weekDates.value
  const month = start.getMonth() === end.getMonth() ? '' : `${end.getMonth() + 1}月`
  return `${start.getMonth() + 1}月${start.getDate()}日至${month}${end.getDate()}日`
})

const menuOpen = ref(false)
const editor = ref(null)
const draftNickname = ref('')
const draftPetName = ref('')

function edit() {
  draftNickname.value = props.nickname
  draftPetName.value = props.petName
  menuOpen.value = false
  editor.value.showModal()
}

function save() {
  emit('save', { nickname: draftNickname.value, petName: draftPetName.value })
  editor.value.close()
}

function exportWeek() {
  const rows = weekDates.value.map((date, day) => `${date.toLocaleDateString('zh-CN')},${moods[sampleMoods[day]]}`)
  const data = new Blob([`\ufeff日期,情绪（示例）\r\n${rows.join('\r\n')}`], { type: 'text/csv;charset=utf-8' })
  const link = document.createElement('a')
  link.href = URL.createObjectURL(data)
  link.download = `情绪趋势示例-${weekTitle.value}.csv`
  link.click()
  setTimeout(() => URL.revokeObjectURL(link.href), 0)
}
</script>

<template>
  <section class="profile-page" aria-label="个人中心">
    <header class="profile-header">
      <button class="help-button" type="button" aria-label="旅程须知" @click="$emit('help')">?</button>
      <button class="profile-settings" type="button" :aria-expanded="menuOpen" aria-controls="profile-menu"
        @click="menuOpen = !menuOpen">
        <span aria-hidden="true"></span>设置
      </button>
      <div v-show="menuOpen" id="profile-menu" class="profile-menu">
        <button type="button" @click="edit">编辑资料</button>
        <button type="button" @click="$emit('redesign')">重新定制宠物</button>
        <button type="button" @click="$emit('help')">旅程须知</button>
      </div>
    </header>

    <section class="profile-card" aria-label="个人资料">
      <span class="profile-emblem" aria-hidden="true"></span>
      <button class="profile-edit" type="button" aria-label="编辑资料" @click="edit">
        <span aria-hidden="true"></span>编辑
      </button>
      <dl>
        <div><dt>昵称</dt><dd>{{ nickname || '未设置' }}</dd></div>
        <div><dt>宠物名称</dt><dd>{{ petName }}</dd></div>
      </dl>
    </section>

    <section class="mood-card" aria-labelledby="mood-title">
      <header class="mood-toolbar">
        <div>
          <h1 id="mood-title">情绪变化</h1>
          <p>{{ weekTitle }}<span v-if="week === 0" class="mood-sample">示例</span></p>
        </div>
        <button type="button" aria-label="导出情绪示例" :disabled="week !== 0" @click="exportWeek">⇧</button>
        <button type="button" aria-label="上一周" @click="week -= 1">‹</button>
        <button type="button" aria-label="下一周" :disabled="week === 0" @click="week += 1">›</button>
      </header>

      <div class="mood-chart" :aria-label="week === 0 ? '示例情绪趋势' : '本周暂无情绪记录'">
        <ul class="mood-axis" aria-hidden="true"><li v-for="mood in moods" :key="mood">{{ mood }}</li></ul>
        <div class="mood-plot">
          <span v-for="(mood, row) in moods" :key="mood" class="mood-gridline" :style="{ gridRow: row + 1 }" aria-hidden="true"></span>
          <template v-if="week === 0">
            <span v-for="(mood, day) in sampleMoods" :key="day" class="mood-point" role="img"
              :aria-label="`${weekdays[day]} ${moods[mood]}`" :title="`${weekdays[day]} ${moods[mood]}`"
              :style="{ gridColumn: day + 1, gridRow: mood + 1 }">{{ mood < 2 ? '•ᴗ•' : '·﹏·' }}</span>
          </template>
          <p v-else class="mood-empty">本周暂无记录</p>
        </div>
        <ul class="mood-days" aria-hidden="true"><li v-for="day in weekdays" :key="day">{{ day }}</li></ul>
      </div>
    </section>

    <dialog ref="editor" class="profile-dialog exercise-dialog" aria-labelledby="profile-edit-title">
      <form @submit.prevent="save">
        <h2 id="profile-edit-title">编辑资料</h2>
        <label>昵称<input v-model.trim="draftNickname" maxlength="20" placeholder="输入昵称" /></label>
        <label>宠物名称<input v-model.trim="draftPetName" maxlength="20" required /></label>
        <div class="profile-form-actions">
          <button type="button" @click="editor.close()">取消</button>
          <button class="primary-button" type="submit" :disabled="!draftPetName">保存</button>
        </div>
      </form>
    </dialog>
  </section>
</template>

<style scoped>
.profile-page {
  position: relative;
  isolation: isolate;
  flex: 1;
  padding: clamp(24px, 6svh, 50px) 7.7% clamp(36px, 11svh, 94px);
  background: #c9d8ad;
}

.profile-page::before, .profile-page::after {
  content: '';
  position: absolute;
  bottom: 0;
  z-index: -1;
  background: url('/images/profile-artwork.jpg') no-repeat;
  background-size: 390px 844px;
}
.profile-page::before {
  left: 0;
  width: 135px;
  height: 143px;
  background-position: 0 -613px;
  mask-image: linear-gradient(transparent 9px, #000 9px), radial-gradient(circle 14px at 48px 16px, #000 96%, transparent);
}
.profile-page::after { right: 0; width: 82px; height: 94px; background-position: -308px -662px; }

.profile-header { position: relative; display: flex; justify-content: space-between; }
.profile-settings, .profile-edit {
  display: grid;
  min-width: 44px;
  min-height: 44px;
  place-items: center;
  gap: 3px;
  background: transparent;
  font-size: .75rem;
}

.profile-settings span {
  width: 26px;
  height: 18px;
  border-block: 3px solid var(--cream);
  background: linear-gradient(var(--cream), var(--cream)) center / 100% 3px no-repeat;
}

.profile-menu {
  position: absolute;
  top: 100%;
  right: 0;
  z-index: 3;
  display: grid;
  min-width: 122px;
  padding: 3px;
  border-radius: 12px;
  background: var(--cream);
  box-shadow: 0 5px 16px #28492b20;
}
.profile-menu button { min-height: 40px; padding-inline: 12px; border-radius: 10px; background: transparent; }
.profile-menu button:hover { background: #e5edc9; }

.profile-card {
  position: relative;
  margin-top: clamp(49px, 9svh, 77px);
  padding: clamp(56px, 9svh, 76px) 10% clamp(19px, 4svh, 32px);
  border-radius: 12px;
  background: var(--cream);
}
.profile-card dl { display: grid; gap: 9px; margin: 0; }
.profile-card dl div { display: flex; align-items: baseline; gap: 4px; }
.profile-card dt { white-space: nowrap; }
.profile-card dt::after { content: '：'; }
.profile-card dd { min-width: 0; margin: 0; overflow-wrap: anywhere; }

.profile-emblem {
  position: absolute;
  top: -72px;
  left: 50%;
  width: 137px;
  height: 127px;
  translate: -50% 0;
  background: url('/images/profile-artwork.jpg') -130px -105px / 390px 844px;
  mask-image: radial-gradient(circle 62px at 63px 63px, #000 97%, #0000),
    radial-gradient(circle 24px at 111px 85px, #000 96%, #0000),
    radial-gradient(ellipse 14px 13px at 112px 112px, #000 96%, #0000);
}

.profile-edit { position: absolute; top: 5px; right: 4px; }
.profile-edit span {
  width: 9px;
  height: 27px;
  border-radius: 5px 5px 1px 1px;
  background: linear-gradient(#f3d273 22%, #f8a9ba 22% 75%, #eac48c 75%);
  rotate: 35deg;
  clip-path: polygon(0 0, 100% 0, 100% 73%, 50% 100%, 0 73%);
}

.mood-card { position: relative; margin-top: 19px; overflow: hidden; border-radius: 16px; background: var(--cream); }
.mood-toolbar { display: flex; align-items: center; padding: 4px 6px 4px 12px; background: #94b75a; }
.mood-toolbar div { flex: 1; }
.mood-toolbar h1 { font-size: .91rem; font-weight: 600; }
.mood-toolbar p { margin-top: 2px; font-size: .73rem; }
.mood-sample { margin-left: 4px; }
.mood-toolbar button { min-width: 34px; min-height: 40px; padding: 0 3px; color: #fffee0; background: transparent; font-size: 1.8rem; }
.mood-toolbar button:disabled { opacity: .46; cursor: default; }

.mood-chart { display: grid; grid-template-columns: 34px 1fr; gap: 5px 4px; padding: 14px 12px 11px 4px; }
.mood-chart ul { margin: 0; padding: 0; list-style: none; text-align: center; font-size: .69rem; }
.mood-axis { display: grid; grid-template-rows: repeat(6, 1fr); align-items: center; }
.mood-days { display: grid; grid-column: 2; grid-template-columns: repeat(7, 1fr); }

.mood-plot {
  position: relative;
  display: grid;
  height: clamp(116px, 18svh, 155px);
  grid-template: repeat(6, 1fr) / repeat(7, 1fr);
  border: solid #527f35;
  border-width: 0 0 5px 5px;
  border-radius: 5px;
  background: #c9d8ad;
}
.mood-gridline { grid-column: 1 / -1; border-bottom: 1px dashed #ffe5d9; }
.mood-point { z-index: 1; display: grid; width: clamp(18px, 5vw, 23px); aspect-ratio: 1; place-self: center; place-items: center; border-radius: 50%; background: #fff; font-size: .59rem; }
.mood-empty { position: absolute; inset: 0; display: grid; place-items: center; font-size: .88rem; }

.profile-dialog label { display: grid; gap: 5px; margin-top: 15px; }
.profile-dialog input { width: 100%; padding: 9px 12px; border: 1px solid var(--green); border-radius: 12px; background: #fff; }
.profile-form-actions { display: flex; justify-content: flex-end; gap: 8px; margin-top: 20px; }
.profile-form-actions button { min-height: 44px; padding: 8px 14px; border-radius: 24px; }
.profile-form-actions button:disabled { opacity: .55; }
</style>
