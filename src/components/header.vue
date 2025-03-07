<template>
  <Toppic />
  <div
    class="mtb-header"
    :class="{ hasToppic: hasToppic, 'header-fixed': defaultProps.fixed || fixedHeader }"
    :style="{ top: hasToppic_TOP + 'px' }"
  >
    <div class="wrap">
      <div class="logo">
        <a style="width: 100%; height: 100%" href="/">
          <img alt="风华正少年" src="@assets/fhzsn_red.png" />
          <img alt="风华正少年" src="@assets/fhzsn_white.png" />
        </a>
      </div>
      <div class="nav">
        <ul class="subnav-ul fl">
          <li
            v-for="(item, index) in headerConfig"
            :key="index"
            class="navView"
            :class="{ dropdown: item?.type === 'list', labelCard: item.type === 'label' }"
          >
            <div class="navItem">
              <a
                v-if="isNormalTab(item?.type)"
                class="isTabs"
                :class="item.extraClass"
                :target="item.target"
                :href="`javascript:void(${index})`"
                @click="clickToPath(item.href)"
              >
                <span>{{ item.label }}</span>
              </a>
              <span v-else class="isTabs">{{ item.label }}</span>
            </div>
            <!--Extra View-->
            <div
              v-if="!isNormalTab(item.type)"
              :class="{
                'navItem-type--list': item.type === 'list',
                'navItem-type--label': item.type === 'label',
              }"
              :style="{ '--index-padding-width': '24px' }"
            >
              <!---->
              <ul v-if="item.type === 'list' && item.children">
                <li v-for="listItem in item.children" :key="listItem.id || listItem.label">
                  <a :href="listItem.href || '#'" :target="listItem.target || '_self'" class="nav-link">
                    {{ listItem.label }}
                  </a>
                </li>
              </ul>
              <!---->
              <div v-else-if="item.type === 'label' && item.children">
                <div
                  v-for="(labelItem, labelIndex) in item.children"
                  :key="labelItem.id || labelItem.label"
                  class="navItem-labelCard-item"
                >
                  <h2>{{ labelItem.title || `项目${labelIndex + 1}` }}</h2>
                  <a
                    v-for="(labelItemListEl, labelItemListIndex) in labelItem?.children"
                    :key="labelItemListIndex"
                    :href="labelItem.href || '#'"
                    :target="labelItem.target || '_self'"
                    class="nav-link"
                  >
                    {{ labelItemListEl?.label }}
                  </a>
                </div>
              </div>
              <!---->
            </div>
          </li>
        </ul>
      </div>
      <div class="operation">
        <div class="themeChange" @click="toggleTheme">
          <div v-if="theme === 'light'" class="sun">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path
                d="M13 1V4H11V1H13ZM20.4853 4.92848L18.364 7.0498L16.9497 5.63559L19.0711 3.51427L20.4853 4.92848ZM4.9289 3.51431L7.05022 5.63563L5.63601 7.04984L3.51469 4.92852L4.9289 3.51431ZM12 8C9.79086 8 8 9.79086 8 12C8 14.2091 9.79086 16 12 16C14.2091 16 16 14.2091 16 12C16 9.79086 14.2091 8 12 8ZM6 12C6 8.68629 8.68629 6 12 6C15.3137 6 18 8.68629 18 12C18 15.3137 15.3137 18 12 18C8.68629 18 6 15.3137 6 12ZM1 11H4V13H1V11ZM20 11H23V13H20V11ZM7.05024 18.3635L4.92892 20.4848L3.51471 19.0706L5.63603 16.9493L7.05024 18.3635ZM18.3639 16.9493L20.4852 19.0707L19.071 20.4849L16.9497 18.3636L18.3639 16.9493ZM13 20V23H11V20H13Z"
                fill="black"
              />
            </svg>
          </div>
          <div v-else class="night">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path
                d="M10.412 4.15761C6.75443 4.8942 4 8.12543 4 12C4 16.4183 7.58172 20 12 20C14.9602 20 17.5466 18.3918 18.9302 15.9997C13.9918 15.9622 10 11.9473 10 7C10 6.02085 10.1313 5.06315 10.412 4.15761ZM2 12C2 6.47715 6.47715 2 12 2H13.7337L12.8656 3.50069C12.2871 4.50091 12 5.68848 12 7C12 10.866 15.134 14 19 14C19.4618 14 19.9122 13.9554 20.3475 13.8706L22.0301 13.5428L21.4872 15.1689C20.1623 19.1373 16.4167 22 12 22C6.47715 22 2 17.5228 2 12Z"
                fill="black"
              />
            </svg>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="tsx">
import { computed, defineComponent, onMounted, onUnmounted, ref, watch, type PropType } from 'vue';
import useTheme from '@hooks/useTheme';
import useToppic from '@hooks/useToppic';
import useHeader from '@hooks/useHeader';
import { getDevice } from '@utils/device';
import router from '../router';
import Toppic from './toppic.vue';

const { theme, toggleTheme } = useTheme();
const { toppicInfo } = useToppic();
const { headerList } = useHeader();
const { isMobile, isPC } = getDevice();

const isNormalTab = (type: string | undefined) => {
  return type !== 'list' && type !== 'label';
};
const headerConfig = computed(() => headerList.value as HeaderData);

const defaultProps = defineProps({
  fixed: {
    type: Boolean as PropType<boolean>,
    default: false,
  },
});

const fixedHeader = ref(false);
const scrollY = ref(0);
const hasToppic = computed(() => {
  return !!toppicInfo.value;
});
const hasToppic_TOP = computed(() => {
  // 需要的top就是当前页面滑动距离 - 32px(消息高度) 若大于 32px 则显示，否则不显示
  const y = scrollY.value - 32;
  return hasToppic.value ? Math.max(0, Math.min(-y, 32)) : 0;
});

const handleScroll = () => {
  scrollY.value = window.scrollY;
  fixedHeader.value = scrollY.value > 32;
};

const clickToPath = (path: string | undefined) => {
  if (!path) {
    console.warn('路径为空，请检查！');
    return;
  }
  router.push(path);
};

watch(hasToppic, (newVal) => {
  if (newVal) {
    scrollY.value = window.scrollY;
  }
});

onMounted(() => {
  window.addEventListener('scroll', handleScroll, { passive: true });
});

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll);
});
</script>

<script lang="tsx">
export default defineComponent({
  name: 'MTBHeader',
});
</script>

<style lang="scss">
.waitHeader {
  position: relative;
  top: 0px;
  transition: all 0.28s ease-in-out;
}
.mtb-header.header-fixed + .waitHeader {
  top: 78px !important;
}
.mtb-header {
  display: flex;
  flex-direction: column;
  width: 100%;
  // background: linear-gradient(180deg, rgba(0, 0, 0, 0.3) 0%, rgba(0, 0, 0, 0) 100%);
  background: transparent;
  position: fixed;
  top: 0;
  left: 0;
  z-index: 1305;
  transition: background 0.28s ease-in-out, top 0.28s ease-in-out;

  &:hover,
  &.header-fixed {
    background: var(--td-bg-color-container);
    box-shadow: var(--td-shadow-1);
    .wrap {
      .logo {
        img:first-of-type {
          display: block;
        }
        img {
          display: none;
        }
      }
      .nav {
        .subnav-ul {
          a.isTabs,
          span.isTabs {
            color: var(--td-text-color-primary);
          }
        }
      }
      .operation .themeChange {
        .sun,
        .night {
          padding: 8px;
          position: absolute;
          svg path {
            fill: var(--td-text-color-primary);
          }
        }
      }
    }
  }
  .wrap {
    height: 78px;
    width: 78%;
    margin: 0px auto;
    font-size: 0;
    display: flex;
    align-items: center;

    .logo {
      position: relative;
      display: inline-block;
      vertical-align: middle;
      width: 190px;
      height: 43.5px;
      img {
        position: absolute;
        top: 0;
        width: 100%;
      }
      img:first-of-type {
        display: none;
      }
    }
    .nav {
      display: inline-block;
      vertical-align: middle;
      width: calc(100% - 280px);
      font-size: 0;
      padding-left: 128px;
      ul,
      .subnav-ul {
        list-style: none;
        vertical-align: middle;
        display: flex;
        max-width: 900px;
        height: 100%;
        li + li {
          padding-left: 36px;
        }
        > li {
          display: inline-block;
          vertical-align: top;
          &.navView {
            font-size: 14px;
            line-height: 14px;
            display: flex;
            text-wrap: nowrap;
            &.dropdown {
              position: relative;
              .navItem-type--list {
                position: absolute;
                display: flex;
                flex-direction: column;
                color: #000;
                top: 64px;
                left: calc(50% + var(--index-padding-width));
                pointer-events: none;
                opacity: 0;
                transform: translate(-50%, 6px);
                transition: all 0.28s ease-in-out;
                ul {
                  position: relative;
                  overflow: visible;
                  display: flex;
                  flex-direction: column;
                  align-content: stretch;
                  vertical-align: middle;
                  margin: 0;
                  list-style: none;
                  background: var(--td-bg-color-container);
                  color: var(--td-text-color-primary);
                  white-space: nowrap;
                  box-shadow: var(--td-shadow-2);
                  align-items: stretch;
                  padding: 8px 0;
                  font-size: 14px;
                  border-radius: 2px;
                  li {
                    padding-left: 0;
                    cursor: pointer;
                    transition: all 0.28s ease-in-out;
                    &:hover {
                      background: #f6f6f6;
                    }
                    a {
                      height: 40px;
                      padding: 0 16px;
                      display: flex;
                      align-items: center;
                      justify-content: flex-start;
                      vertical-align: middle;
                      color: var(--td-text-color-primary);
                    }
                  }
                }
              }
            }
            &.labelCard {
              .navItem-type--label {
                pointer-events: auto;
                width: 100%;
                background: var(--td-bg-color-container);
                left: 0;
                z-index: 0;
                opacity: 0;
                position: absolute;
                top: 64px;
                height: auto;
                min-height: 80px;
                box-shadow: var(--td-shadow-2);
                color: var(--td-text-color-primary);
                pointer-events: none;
                transform: translateY(6px);
                transition: all 0.28s ease-in-out;
                align-items: center;
                display: flex;
                justify-content: center;
                padding: 48px 0;
                .navItem-labelCard-item {
                  display: inline-block;
                  width: 180px;
                  margin: 0 24px 0 0;
                  font-size: 14px;
                  line-height: 30px;
                  color: #333;
                  vertical-align: top;
                  transition: all 0.28s ease-in-out;
                  text-align: center;
                  height: auto;
                  > h2 {
                    font-size: 16px;
                    font-weight: 700;
                    color: var(--td-text-color-primary);
                    margin-bottom: 10px;
                  }
                  > a {
                    display: block;
                    margin: 0 25px;
                    color: var(--td-text-color-primary);
                    cursor: pointer;
                    transition: all 0.28s ease-in-out;
                  }
                }
              }
            }
            .navItem {
              font-size: 16px;
              font-weight: 600;
            }
          }
          a.isTabs,
          span.isTabs {
            line-height: 78px;
            transition: all 0.28s ease-in-out;
            color: var(--td-text-color-anti);
            vertical-align: middle;
            font-weight: 500;
            font-size: 16px;
            cursor: pointer;
            position: relative;
            justify-content: center;
            letter-spacing: -0.02em;
            word-spacing: 0;
            height: 100%;
            display: flex;
            align-items: center;
            &::after {
              content: ' ';
              display: flex;
              width: 0;
              height: 3px;
              background: var(--td-text-color-primary);
              transition: all 0.28s ease-in-out;
              transform: translate(-50%);
              bottom: 22px;
              left: 50%;
              position: absolute;
            }
          }

          &:hover {
            .navItem-type--list {
              opacity: 1 !important;
              transform: translate(-50%, 12px) !important;
              pointer-events: auto !important;
              animation: disable-pointer-events 0.3s;
            }
            .navItem-type--label {
              opacity: 1 !important;
              transform: translateY(12px) !important;
              pointer-events: auto !important;
              animation: disable-pointer-events 0.3s;
            }
            a::after,
            span::after {
              width: 100%;
            }
          }
        }
      }
    }

    .operation {
      display: inline-block;
      vertical-align: middle;
      font-size: 0;

      .themeChange {
        position: relative;
        height: 40px;
        width: 40px;
        transition: all 0.28s ease-in-out;
        border-radius: 4px;
        &:hover {
          background: var(--td-bg-color-container-hover);
        }
        .sun,
        .night {
          padding: 8px;
          position: absolute;
          svg path {
            fill: var(--td-text-color-anti);
          }
        }
      }
    }
  }
  img {
    object-fit: cover;
  }
}

@keyframes disable-pointer-events {
  0%,
  99% {
    pointer-events: none;
  }
  100% {
    pointer-events: auto;
  }
}
</style>
