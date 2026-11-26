<script setup>
import { computed } from 'vue'

const props = defineProps({
  pet: { type: Object, required: true },
  label: String,
  sample: Boolean,
  outfit: Object,
})

const original = computed(() => {
  const { shape, color, expression, ears } = props.pet
  return !props.sample && shape === 'square' && color === 'pink' && expression === 'smile' && ears === 'floppy'
})
</script>

<template>
  <div
    class="pet-avatar"
    :class="{ 'pet-avatar--sample': sample }"
    :data-color="pet.color"
    :role="label ? 'img' : undefined"
    :aria-label="label"
    :aria-hidden="label ? undefined : 'true'"
  >
    <img v-if="original" class="avatar-art" src="/images/pet-waving.png" alt="" />
    <template v-else>
      <img v-if="!sample" class="avatar-art avatar-body" src="/images/pet-waving.png" alt="" />
      <div class="avatar-head" :data-shape="pet.shape">
        <div v-if="pet.ears !== 'none'" class="avatar-ears" :data-ears="pet.ears"></div>
        <div class="avatar-face" :data-expression="pet.expression">
          <span class="avatar-eye"></span>
          <span class="avatar-mouth"></span>
          <span class="avatar-eye"></span>
        </div>
      </div>
    </template>
    <img
      v-if="outfit?.accessory"
      class="avatar-accessory"
      :data-item="outfit.accessory"
      :src="`/images/backpack/${outfit.accessory}.png`"
      alt=""
    />
    <img
      v-if="outfit?.clothes"
      class="avatar-clothes"
      :data-item="outfit.clothes"
      :src="`/images/backpack/${outfit.clothes}.png`"
      alt=""
    />
  </div>
</template>

<style>
.pet-avatar {
  position: relative;
  aspect-ratio: 1;
  container-type: inline-size;
  --pet-ink: #302821;
}

[data-color='peach'] { --pet-color: #ffb260; --body-filter: sepia(1) saturate(2.6); }
[data-color='pink'] { --pet-color: #ffbac6; }
[data-color='sky'] { --pet-color: #88cdeb; --body-filter: hue-rotate(211deg) saturate(1.45); }
[data-color='lime'] { --pet-color: #c4d330; --body-filter: sepia(1) saturate(3.2) hue-rotate(10deg) brightness(.88); }
[data-color='blue'] { --pet-color: #6b8cc2; --body-filter: hue-rotate(238deg) saturate(1.6) brightness(.79); }
[data-color='yellow'] { --pet-color: #ffda41; --body-filter: sepia(1) saturate(3.7) hue-rotate(9deg); }

[data-shape='triangle'] { --head-radius: 83% 28% 29% 30% / 88% 41% 31% 25%; --head-rotation: -12deg; }
[data-shape='square'] { --head-radius: 42% 42% 33% 33% / 45% 45% 34% 34%; }
[data-shape='pear'] { --head-radius: 44% 50% 44% 45% / 69% 67% 30% 30%; }
[data-shape='flower'] {
  --head-fill:
    radial-gradient(ellipse 25% 42% at 50% 49%, var(--pet-color) 97%, transparent),
    radial-gradient(ellipse 24% 30% at 32% 34%, var(--pet-color) 97%, transparent),
    radial-gradient(ellipse 25% 31% at 69% 36%, var(--pet-color) 97%, transparent),
    radial-gradient(ellipse 27% 29% at 27% 58%, var(--pet-color) 97%, transparent),
    radial-gradient(ellipse 28% 28% at 72% 61%, var(--pet-color) 97%, transparent),
    radial-gradient(ellipse 25% 26% at 50% 74%, var(--pet-color) 97%, transparent);
}
[data-shape='oval'] { --head-radius: 50%; --head-width: 79%; }
[data-shape='round'] { --head-radius: 50%; }

.avatar-art { position: absolute; inset: 0; width: 100%; height: 100%; }
.avatar-body { clip-path: inset(64.5% 25% 0 25%); filter: var(--body-filter, none); }

.avatar-head { position: absolute; inset: 24.5% 21% 35%; }
.avatar-head::before, .shape-swatch {
  border-radius: var(--head-radius);
  rotate: var(--head-rotation, 0deg);
}

.avatar-head::before {
  content: '';
  position: absolute;
  inset: 0;
  width: var(--head-width, 100%);
  margin-inline: auto;
  background: var(--head-fill, radial-gradient(ellipse at 36% 29%, #fff3, transparent 74%), var(--pet-color));
}

.avatar-face {
  position: absolute;
  inset: 41% 29% 22%;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.avatar-eye {
  width: 28%;
  aspect-ratio: 1;
  border-radius: 50%;
  background: radial-gradient(circle at 53% 51%, var(--pet-ink) 44%, #fff 48%);
}

.avatar-mouth {
  align-self: flex-end;
  display: grid;
  width: 28%;
  height: 65%;
  place-items: center;
  border-radius: 42% 42% 50% 50%;
  background: #fff8eb;
}

.avatar-mouth::before {
  content: '';
  width: 45%;
  aspect-ratio: 1;
  border-radius: 48%;
  background: var(--pet-ink);
}

.avatar-mouth::after {
  content: '';
  width: 36%;
  height: .31em;
  border: max(1px, .65cqw) solid var(--pet-ink);
  border-top: 0;
  border-radius: 0 0 55% 55%;
  font-size: 5cqw;
}

.avatar-face::before, .avatar-face::after {
  content: '';
  position: absolute;
  top: 47%;
  width: 20%;
  height: 18%;
  border-radius: 50%;
  background: #ff9eaa85;
}
.avatar-face::before { left: -14%; }
.avatar-face::after { right: -14%; }

[data-expression='wink'] .avatar-eye:last-child,
[data-expression='sleepy'] .avatar-eye {
  height: 25%;
  border-bottom: max(1px, .8cqw) solid var(--pet-ink);
  background: transparent;
}
[data-expression='happy'] .avatar-eye {
  height: 29%;
  border-top: max(1px, .8cqw) solid var(--pet-ink);
  background: transparent;
}
[data-expression='surprised'] .avatar-mouth::after { height: 30%; border-top: max(1px, .65cqw) solid; border-radius: 50%; }
[data-expression='shy'] .avatar-eye { scale: .7; }
[data-expression='shy']::before, [data-expression='shy']::after { background: #f47793b0; }
[data-expression='sleepy'] .avatar-mouth { scale: .7; }

.avatar-ears { position: absolute; inset: -10% -1% auto; z-index: 1; height: 46%; }
.avatar-ears::before, .avatar-ears::after {
  content: '';
  position: absolute;
  top: 0;
  width: 31%;
  height: 52%;
  border-radius: 100% 90% 42% 45%;
  background: var(--pet-ink);
  rotate: -24deg;
}
.avatar-ears::before { left: 1%; }
.avatar-ears::after { right: 1%; scale: -1 1; rotate: 24deg; }
[data-ears='rabbit']::before, [data-ears='rabbit']::after { inset-block-start: -34%; width: 15%; height: 100%; border-radius: 80%; }
[data-ears='rabbit']::before { left: 16%; }
[data-ears='rabbit']::after { right: 16%; }
[data-ears='bear']::before, [data-ears='bear']::after { width: 27%; height: 76%; border-radius: 50%; box-shadow: inset 0 0 0 1.6cqw var(--pet-ink); background: var(--pet-color); }
[data-ears='cat']::before, [data-ears='cat']::after { top: 6%; width: 28%; height: 72%; clip-path: polygon(68% 0, 100% 100%, 0 86%); }
[data-ears='sprout']::before { top: -42%; left: 42%; width: 16%; height: 80%; border-radius: 100% 5% 100% 5%; background: #5e8d46; rotate: 36deg; }
[data-ears='sprout']::after { content: none; }

.pet-avatar--sample .avatar-head { inset: 23% 10% 7%; }

.avatar-accessory, .avatar-clothes {
  position: absolute;
  left: 49%;
  z-index: 3;
  translate: -50% 0;
  object-fit: contain;
}

.avatar-accessory { top: 11%; width: 23%; height: 20%; }
.avatar-accessory[data-item='flower'] { top: 8%; left: 53%; width: 16%; }
.avatar-accessory[data-item='head-ribbon'], .avatar-accessory[data-item='head-bow'] { top: 17%; left: 66%; width: 16%; }
.avatar-accessory[data-item='glasses'] { top: 35%; width: 32%; height: 18%; }
.avatar-clothes { top: 60.5%; width: 19%; height: 15%; }
.avatar-clothes[data-item='vest'] { top: 63%; width: 25%; height: 18%; }
.avatar-clothes[data-item='bib'], .avatar-clothes[data-item='bandana'] { top: 61.5%; width: 22%; height: 17%; }
</style>
