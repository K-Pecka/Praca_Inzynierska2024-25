<template>
  <footer>
    <div class="footer">
      <div class="footer__top">
        <div class="footer__logo">
          <slot name="logo"> </slot>
        </div>

        <div
          class="footer__links"
          v-if="footerData.links && footerData.links.length > 0"
        >
          <ul>
            <li v-for="(link, index) in footerData.links" :key="index">
              <a :href="link.href">{{ link.label }}</a>
            </li>
          </ul>
        </div>
      </div>
      <hr />
      <div class="footer__bottom" v-if="footerData.footerText">
        <p>{{ footerData.footerText }}</p>
      </div>
    </div>
  </footer>
</template>

<script lang="ts" setup>
import { defineProps, PropType } from "vue";

interface Link {
  href: string;
  label: string;
}

interface FooterData {
  links: Link[];
  footerText?: string;
}

const props = defineProps({
  footerData: {
    type: Object as PropType<FooterData>,
    required: true,
  },
});
</script>

<style scoped lang="scss">
@use "@/assets/style" as *;
* {
  color: var(--text-color);
  font-family: var(--font-family);
}
footer {
  padding: 3rem;
  background-color: var(--secondary-color);
  font-family: Arial, sans-serif;
}
.footer {
  width: 83vw;
  margin: auto;
}

.footer__top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.footer__logo {
  @include font-large;
  @include gradient-text;
  font-size: 2rem;
  display: flex;
  align-items: center;
}

.footer__logo img {
  width: 50px;
  height: 50px;
  margin-right: 10px;
}

.footer__name {
  font-size: 1.5rem;
  font-weight: bold;
}

.footer__links ul {
  display: flex;
  list-style: none;
  gap: 2rem;
  padding: 0.5rem;
  margin: 0;
}

.footer__links li {
  margin: 5px 0;
  @include font-regular;
}

.footer__links a {
  text-decoration: none;
}

.footer__links a:hover {
  text-decoration: underline;
}
hr {
  color: #0000001c;
}
.footer__bottom {
  text-align: center;
  margin-top: 20px;
}

.footer__bottom p {
  margin: 0;
  font-size: 1rem;
}
</style>
