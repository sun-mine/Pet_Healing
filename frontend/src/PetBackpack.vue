<script setup>
import { computed, ref } from 'vue'
import { asset } from './asset'

const props = defineProps({ outfit: { type: Object, required: true } })
defineEmits(['equip', 'close'])

const categories = {
  accessory: {
    label: '饰品', icon: 'head-bow', items: [
      ['head-ribbon', '蓝丝带'], ['top-hat', '蓝礼帽'], ['knit-cap', '橙色针织帽'], ['sun-cap', '棒球帽'],
      ['glasses', '蓝圆眼镜'], ['parasol', '蓝遮阳帽'], ['head-bow', '黄色发结'], ['flower-hat', '花边帽'],
      ['flower', '小黄花'],
    ],
  },
  clothes: {
    label: '衣服', icon: 'vest', items: [
      ['bow-tie', '黄色领结'], ['vest', '黄色马甲'], ['collar', '橙色项圈'], ['bib', '花边围兜'],
      ['bandana', '蓝方巾'], ['scarf', '蓝丝巾'], ['orange-bow', '橙色领结'], ['pendant', '爱心项链'],
      ['ruffle', '花边领饰'],
    ],
  },
  items: {
    label: '物品', icon: 'frisbee', items: [['frisbee', '飞盘'], ['bowl', '食盆'], ['toy', '蓝兔玩偶']],
  },
}

const active = ref('accessory')
const category = computed(() => categories[active.value])

function isEquipped(item) {
  return active.value === 'items' ? props.outfit.items.includes(item) : props.outfit[active.value] === item
}
</script>

<template>
  <section class="backpack-panel" aria-label="背包">
    <div class="backpack-tabs" role="group" aria-label="背包分类">
      <button
        v-for="(tab, key) in categories"
        :key="key"
        type="button"
        :aria-pressed="active === key"
        @click="active = key"
      >
        <img :src="asset(`images/backpack/${tab.icon}.png`)" alt="" />{{ tab.label }}
      </button>
      <button class="backpack-close" type="button" aria-label="关闭背包" @click="$emit('close')">×</button>
    </div>

    <div class="backpack-grid" role="group" :aria-label="category.label">
      <button
        v-for="[item, label] in category.items"
        :key="item"
        type="button"
        :aria-pressed="isEquipped(item)"
        @click="$emit('equip', active, item)"
      >
        <img :src="asset(`images/backpack/${item}.png`)" alt="" />
        <span>{{ label }}</span>
      </button>
      <span v-for="slot in 12 - category.items.length" :key="slot" class="backpack-empty" aria-hidden="true"></span>
    </div>
  </section>
</template>

<style scoped>
.backpack-panel { background: #92b558; }
.backpack-tabs {
  display: flex;
  position: relative;
  min-height: 60px;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 4px 48px;
  background: #fff;
}

.backpack-tabs button {
  display: grid;
  min-width: 46px;
  min-height: 48px;
  justify-items: center;
  padding: 3px 6px;
  border-radius: 12px;
  background: transparent;
  font-size: .8rem;
}
.backpack-tabs img { width: 24px; height: 24px; object-fit: contain; }
.backpack-tabs button[aria-pressed='true'] { background: #fce2df; }
.backpack-tabs .backpack-close {
  position: absolute;
  right: 10px;
  min-width: 36px;
  min-height: 36px;
  place-items: center;
  border-radius: 50%;
  background: var(--pink);
  font-size: 1.35rem;
  line-height: 1;
}

.backpack-grid {
  display: grid;
  min-height: 223px;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  grid-auto-rows: clamp(60px, 8svh, 72px);
  gap: 9px;
  padding: 15px 6%;
}

.backpack-grid button {
  display: grid;
  align-content: center;
  justify-items: center;
  padding: 3px 2px;
  border: 2px solid transparent;
  border-radius: 14px;
  background: var(--cream);
  font-size: .7rem;
}
.backpack-grid button[aria-pressed='true'] { border-color: #406e36; background: #fbf4c5; }
.backpack-grid img { display: block; width: 39px; height: 34px; object-fit: contain; }
.backpack-empty { border-radius: 14px; background: var(--green); }
</style>
