<script setup>
import { computed, ref } from 'vue'
import PetAvatar from './PetAvatar.vue'
import PetBackpack from './PetBackpack.vue'
import ProfileCenter from './ProfileCenter.vue'
import SleepMeditation from './SleepMeditation.vue'

const customization = {
  shape: {
    title: '选择宠物的形状',
    options: [['triangle', '三角形'], ['square', '方形'], ['pear', '梨形'], ['flower', '花朵形'], ['oval', '椭圆形'], ['round', '圆形']],
    next: 'color',
  },
  color: {
    title: '给你的宠物选个颜色',
    options: [['peach', '蜜桃橙'], ['pink', '樱花粉'], ['sky', '天空蓝'], ['lime', '嫩芽绿'], ['blue', '矢车菊蓝'], ['yellow', '向日葵黄']],
    next: 'expression',
  },
  expression: {
    title: '给你的宠物选个表情',
    options: [['smile', '微笑'], ['wink', '眨眼'], ['happy', '开心'], ['surprised', '惊讶'], ['shy', '害羞'], ['sleepy', '困倦']],
    next: 'ears',
  },
  ears: {
    title: '给你的宠物选一对耳朵',
    options: [['floppy', '小狗耳'], ['rabbit', '兔子耳'], ['bear', '小熊耳'], ['sprout', '小芽'], ['none', '无耳朵'], ['cat', '小猫耳']],
    next: 'appearance',
  },
}

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
const previous = {
  shape: 'design', color: 'shape', expression: 'color', ears: 'expression', appearance: 'ears',
  name: 'appearance', feeling: 'name', concern: 'feeling', result: 'concern',
}
const outcomes = [
  ['↓', '焦虑水平'], ['↑', '睡眠质量'], ['↓', '神经敏感性'],
  ['↑', '自我效能感'], ['↑', '自爱程度'], ['↓', '抑郁情绪'],
]
const topics = ['暴食', '焦虑', '失眠', '专注力差', '精神紧绷']
const tabs = [
  { label: '宠物', page: 'home' },
  { label: '地图' },
  { label: '发现', page: 'discover' },
  { label: '我的', page: 'profile' },
]
const profileKey = 'pet-healing-profile'
const savedProfile = JSON.parse(localStorage.getItem(profileKey))
const page = ref(savedProfile ? 'home' : 'design')
const noticeReturn = ref('home')
const pet = ref(savedProfile?.pet ?? { shape: '', color: 'lime', expression: 'smile', ears: 'none' })
const petName = ref(savedProfile?.name ?? '')
const nickname = ref(savedProfile?.nickname ?? '')
const outfit = ref(savedProfile?.outfit ?? { accessory: 'top-hat', clothes: 'collar', items: ['bowl', 'toy'] })
const redesign = ref(null)
const backpackOpen = ref(false)
const answers = ref({ feeling: '', concern: '' })
const sleepOpen = ref(false)
const exerciseDialog = ref(null)
const assessment = computed(() => assessments[page.value])
const customStep = computed(() => customization[page.value])
const onMain = computed(() => tabs.some((tab) => tab.page === page.value))
const previewPet = computed(() => redesign.value?.pet ?? pet.value)
const nameInput = computed({
  get: () => redesign.value?.name ?? petName.value,
  set(name) {
    if (redesign.value) redesign.value.name = name
    else petName.value = name
  },
})

function openNotice() {
  noticeReturn.value = page.value
  page.value = 'notice'
}

function saveProfile() {
  localStorage.setItem(profileKey, JSON.stringify({
    name: petName.value, nickname: nickname.value, pet: pet.value, outfit: outfit.value,
  }))
}

function updateProfile(details) {
  nickname.value = details.nickname
  petName.value = details.petName
  saveProfile()
}

function startRedesign() {
  redesign.value = { pet: { ...pet.value }, name: petName.value }
  page.value = 'shape'
}

function back() {
  if (page.value === 'shape' && redesign.value) {
    redesign.value = null
    page.value = 'profile'
  } else {
    page.value = previous[page.value]
  }
}

function finishNaming() {
  if (!redesign.value) {
    page.value = 'feeling'
    return
  }

  pet.value = redesign.value.pet
  petName.value = redesign.value.name
  redesign.value = null
  saveProfile()
  page.value = 'home'
}

function confirmNotice() {
  page.value = noticeReturn.value
  if (page.value === 'home') saveProfile()
}

function changeOutfit(category, item) {
  if (category === 'items') {
    const items = outfit.value.items
    outfit.value.items = items.includes(item) ? items.filter((entry) => entry !== item) : [...items, item]
  } else {
    outfit.value[category] = outfit.value[category] === item ? '' : item
  }
}

function closeBackpack() {
  saveProfile()
  backpackOpen.value = false
}
</script>

<template>
  <main class="app-shell" :class="{ 'app-shell--main': onMain, 'app-shell--pet': page === 'home', 'app-shell--profile': page === 'profile' }"
    @keydown.esc="backpackOpen && closeBackpack()">
    <SleepMeditation v-if="page === 'meditation'" :pet="pet" :outfit="outfit" @close="page = 'discover'" />

    <section v-else-if="!onMain" class="onboarding" :class="`onboarding--${page}`">
      <button
        v-if="previous[page]"
        class="back-button"
        type="button"
        aria-label="返回上一步"
        @click="back"
      >
        <span aria-hidden="true"></span>
      </button>

      <template v-if="page === 'design'">
        <div class="design-intro notice-card">
          <h1 class="notice-title">设计你的宠物</h1>
          <p>选一个形状和颜色，再为它搭配喜欢的表情和耳朵。</p>
        </div>
        <button class="primary-button step-action" type="button" @click="page = 'shape'">开始定制</button>
      </template>

      <template v-else-if="customStep">
        <h1 class="step-title">{{ customStep.title }}</h1>
        <PetAvatar v-if="previewPet.shape" class="step-pet custom-pet" :pet="previewPet" label="宠物形象预览" />
        <div v-if="page !== 'shape'" class="chosen-parts" aria-hidden="true">
          <span class="shape-swatch" :data-shape="previewPet.shape"></span>
          <span v-if="page !== 'color'" class="color-swatch" :data-color="previewPet.color"></span>
          <PetAvatar v-if="page === 'ears'" :pet="{ ...previewPet, ears: 'none' }" sample />
        </div>
        <div class="custom-options" role="group" :aria-label="customStep.title">
          <button
            v-for="[value, label] in customStep.options"
            :key="value"
            type="button"
            :aria-label="label"
            :aria-pressed="previewPet[page] === value"
            @click="previewPet[page] = value"
          >
            <span v-if="page === 'shape'" class="shape-swatch" :data-shape="value"></span>
            <span v-else-if="page === 'color'" class="color-swatch" :data-color="value"></span>
            <PetAvatar v-else class="pet-swatch" :pet="{ ...previewPet, [page]: value }" sample />
          </button>
        </div>
        <button class="primary-button custom-action" type="button" :disabled="!previewPet[page]" @click="page = customStep.next">
          {{ page === 'ears' ? '完成定制' : '下一步' }}
        </button>
      </template>

      <template v-else-if="page === 'appearance'">
        <h1 class="step-title">确认你的宠物形象</h1>
        <PetAvatar class="step-pet" :pet="previewPet" label="定制好的宠物形象" />
        <button class="primary-button step-action" type="button" @click="page = 'name'">确定</button>
      </template>

      <form v-else-if="page === 'name'" class="name-form" @submit.prevent="finishNaming">
        <label class="name-field">
          <span class="sr-only">宠物名字</span>
          <input v-model.trim="nameInput" maxlength="20" placeholder="输入宠物的名字" />
          <span class="name-count">{{ nameInput.length }}/20</span>
        </label>
        <PetAvatar class="step-pet" :pet="previewPet" label="等你起名的宠物" />
        <button v-show="nameInput" class="primary-button name-action" type="submit" :disabled="!nameInput">完成</button>
        <p v-if="!nameInput" class="name-hint">接下来的旅程由我来陪伴你<br />给我起个名字吧</p>
      </form>

      <template v-else-if="assessment">
        <h1 class="step-title">{{ assessment.prompt(petName) }}</h1>
        <PetAvatar class="step-pet assessment-pet" :pet="pet" />
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
        <button class="primary-button" type="button" @click="confirmNotice">确定</button>
      </template>
    </section>

    <template v-else-if="page === 'home'">
      <section class="pet-home" :class="{ 'pet-home--dressing': backpackOpen }" aria-label="宠物主界面">
        <template v-if="!backpackOpen">
          <header class="pet-home-header">
            <button class="help-button" type="button" aria-label="旅程须知" @click="openNotice">?</button>
            <div class="pet-affection">
              <meter min="0" max="100" value="60" aria-label="亲密值"></meter>
              <span>亲密值</span>
            </div>
          </header>
          <p class="pet-greeting">你好呀，我是{{ petName }}<br />去「发现」看看吧！</p>
          <button class="pet-backpack" type="button" @click="backpackOpen = true">
            <span class="pet-prop" aria-hidden="true"></span>
            背包
          </button>
        </template>
        <button v-else class="pet-save-outfit" type="button" @click="closeBackpack">保存装扮</button>

        <PetAvatar class="pet-home-avatar" :pet="pet" :label="petName" :outfit="outfit" />
        <img v-for="item in outfit.items" :key="item" class="pet-scene-item" :class="`pet-scene-item--${item}`"
          :src="`/images/backpack/${item}.png`" alt="" />
      </section>

      <PetBackpack v-if="backpackOpen" :outfit="outfit" @equip="changeOutfit" @close="closeBackpack" />
    </template>

    <ProfileCenter v-else-if="page === 'profile'" :nickname="nickname" :pet-name="petName"
      @save="updateProfile" @help="openNotice" @redesign="startRedesign" />

    <section v-else class="discover" aria-label="发现">
      <header class="discover-header">
        <button class="help-button" type="button" aria-label="旅程须知" @click="openNotice">?</button>
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
        <button type="button" @click="exerciseDialog.showModal()">白噪音</button>
        <button type="button" @click="page = 'meditation'">助眠冥想</button>
      </div>
      <div class="sleeping-pet" :class="{ 'sleeping-pet--small': sleepOpen }">
        <img src="/images/pet-sleeping.png" alt="倚在花丛里打盹的小狗" />
      </div>

      <dialog ref="exerciseDialog" class="exercise-dialog" aria-labelledby="exercise-title">
        <h2 id="exercise-title">白噪音</h2>
        <p>听一会儿平稳的背景声，把注意力轻轻放回此刻。</p>
        <form method="dialog"><button class="primary-button" type="submit">返回发现</button></form>
      </dialog>
    </section>

    <nav v-if="onMain && !backpackOpen" class="bottom-bar" aria-label="主导航">
      <component
        :is="tab.page ? 'button' : 'span'"
        v-for="tab in tabs"
        :key="tab.label"
        :type="tab.page ? 'button' : undefined"
        :aria-current="tab.page === page ? 'page' : undefined"
        @click="page = tab.page || page"
      >
        <i class="tab-icon" aria-hidden="true"></i>{{ tab.label }}
      </component>
    </nav>
  </main>
</template>
