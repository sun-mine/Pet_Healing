<script setup>
import { computed, ref } from 'vue'

const assessments = {
  feeling: {
    prompt: (name) => `哈喽，${name}，你现在感觉怎么样？`,
    options: ['悲伤', '内疚', '恐惧', '愤怒', '自我否定', '自责'],
    action: '继续',
    next: 'concern',
  },
  concern: {
    prompt: (name) => `${name}，最近你有被这些问题困扰吗？`,
    options: ['精力不足', '入睡困难', '记忆减退', '暴饮暴食', '厌食', '嗜睡'],
    action: '确定',
    next: 'result',
  },
}
const previous = { name: 'appearance', feeling: 'name', concern: 'feeling', result: 'concern' }
const outcomes = [
  ['↓', '焦虑水平'], ['↑', '睡眠质量'], ['↓', '神经敏感性'],
  ['↑', '自我效能感'], ['↑', '自爱程度'], ['↓', '抑郁情绪'],
]
const topics = ['暴食', '焦虑', '失眠', '专注力差', '精神紧绷']
const tabs = ['宠物', '地图', '发现', '我的']
const exercises = {
  白噪音: '听一会儿平稳的背景声，把注意力轻轻放回此刻。',
  助眠冥想: '把注意力放到呼吸上，跟着呼吸的节奏慢慢放松身体。',
}

const page = ref('appearance')
const petName = ref('')
const answers = ref({ feeling: '', concern: '' })
const sleepOpen = ref(false)
const exercise = ref('')
const exerciseDialog = ref(null)
const assessment = computed(() => assessments[page.value])

function showExercise(title) {
  exercise.value = title
  exerciseDialog.value.showModal()
}
</script>

<template>
  <main class="app-shell">
    <section v-if="page !== 'discover'" class="onboarding" :class="`onboarding--${page}`">
      <button
        v-if="previous[page]"
        class="back-button"
        type="button"
        aria-label="返回上一步"
        @click="page = previous[page]"
      >
        <span aria-hidden="true"></span>
      </button>

      <template v-if="page === 'appearance'">
        <h1 class="step-title">确认你的宠物形象</h1>
        <img class="step-pet" src="/images/pet-waving.png" alt="挥手的粉色小狗" />
        <button class="primary-button step-action" type="button" @click="page = 'name'">确定</button>
      </template>

      <form v-else-if="page === 'name'" class="name-form" @submit.prevent="page = 'feeling'">
        <label class="name-field">
          <span class="sr-only">宠物名字</span>
          <input v-model.trim="petName" maxlength="20" placeholder="输入宠物的名字" />
          <span class="name-count">{{ petName.length }}/20</span>
        </label>
        <img class="step-pet" src="/images/pet-waving.png" alt="等你起名的小狗" />
        <button v-show="petName" class="primary-button name-action" type="submit" :disabled="!petName">完成</button>
        <p v-if="!petName" class="name-hint">接下来的旅程由我来陪伴你<br />给我起个名字吧</p>
      </form>

      <template v-else-if="assessment">
        <h1 class="step-title">{{ assessment.prompt(petName) }}</h1>
        <img class="step-pet assessment-pet" src="/images/pet-waving.png" alt="" />
        <div class="assessment-options" role="group" :aria-label="assessment.prompt(petName)">
          <button
            v-for="option in assessment.options"
            :key="option"
            type="button"
            :aria-pressed="answers[page] === option"
            @click="answers[page] = answers[page] === option ? '' : option"
          >
            {{ option }}
          </button>
        </div>
        <button class="primary-button step-action" type="button" @click="page = assessment.next">
          {{ assessment.action }}
        </button>
      </template>

      <template v-else-if="page === 'result'">
        <div class="result-art" role="img" aria-label="坐在白色花朵上的小狗"></div>
        <p class="result-message">正在为你构建沿途的风景～</p>
        <button class="primary-button result-action" type="button" @click="page = 'notice'">确定</button>
      </template>

      <template v-else>
        <h1 class="notice-title">旅程须知</h1>
        <div class="notice-card">
          <section>
            <h2>内容简介</h2>
            <p>「宠愈」以认知行为疗法为基础，通过每日 10–20 分钟的练习，陪你缓解丧宠带来的伤痛，回顾与宠物相处的时光。</p>
          </section>
          <section>
            <h2>预期效果</h2>
            <ul class="outcomes">
              <li v-for="[direction, label] in outcomes" :key="label">
                <span>{{ direction }}</span>{{ label }}
              </li>
            </ul>
          </section>
          <section>
            <h2>适用人群</h2>
            <p>刚经历丧宠、常常想起与宠物的过往，或正在尝试重新适应日常生活的人。</p>
          </section>
        </div>
        <button class="primary-button" type="button" @click="page = 'discover'">确定</button>
      </template>
    </section>

    <section v-else class="discover" aria-label="发现">
      <header class="discover-header">
        <button class="help-button" type="button" aria-label="旅程须知" @click="page = 'notice'">?</button>
      </header>
      <div class="topics" role="group" aria-label="练习分类">
        <template v-for="topic in topics" :key="topic">
          <button
            v-if="topic === '失眠'"
            class="topic"
            type="button"
            :aria-expanded="sleepOpen"
            aria-controls="sleep-exercises"
            @click="sleepOpen = !sleepOpen"
          >
            <span>{{ topic }}</span>
            <img src="/images/pet-paw.png" alt="" />
          </button>
          <div v-else class="topic">
            <span>{{ topic }}</span>
            <img src="/images/pet-paw.png" alt="" />
          </div>
        </template>
      </div>

      <div v-show="sleepOpen" id="sleep-exercises" class="exercise-panel">
        <button v-for="(_, title) in exercises" :key="title" type="button" @click="showExercise(title)">{{ title }}</button>
      </div>
      <div class="sleeping-pet" :class="{ 'sleeping-pet--small': sleepOpen }">
        <img src="/images/pet-sleeping.png" alt="倚在花丛里打盹的小狗" />
      </div>

      <nav class="bottom-bar" aria-label="主导航">
        <span v-for="tab in tabs" :key="tab" :aria-current="tab === '发现' ? 'page' : undefined">
          <i class="tab-icon" aria-hidden="true"></i>{{ tab }}
        </span>
      </nav>

      <dialog ref="exerciseDialog" class="exercise-dialog" aria-labelledby="exercise-title">
        <h2 id="exercise-title">{{ exercise }}</h2>
        <p>{{ exercises[exercise] }}</p>
        <form method="dialog"><button class="primary-button" type="submit">返回发现</button></form>
      </dialog>
    </section>
  </main>
</template>
