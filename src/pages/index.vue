<template>
  <div class="container">
    <div>
      <Swiper
        class="swiper-container video_banner"
        :style="`height: ${initHeight}px`"
        :modules="swiperModules"
        :slides-per-view="1"
        :loop="true"
        :autoplay="false"
        :pagination="{ clickable: true, type: 'bullets', renderBullet: renderBullets }"
        :speed="800"
        @swiper="onSwiperInit"
        @slide-change-transition-start="onSwiperSlideChange"
      >
        <SwiperSlide v-for="(item, index) in bannerData" :key="index">
          <video
            v-if="item.type === 'video'"
            :id="`swiperSource_${index}`"
            :src="item.url"
            class="banner-image"
            muted
            autoplay
            @play="onVideoStatrPlay"
            @timeupdate="onVideoPlaying"
            @ended="onVideoEnd"
          />
          <img v-else :id="`swiperSource_${index}`" :src="item.url" :alt="item.title" class="banner-image" />
          <div class="other-bannerceter">
            <h2>{{ item?.title }}</h2>
            <h3>{{ item?.desc }}</h3>
            <p></p>
          </div>
        </SwiperSlide>
      </Swiper>
    </div>
    <!---->
    <div class="wxjb" :style="`background-image: url(${wxjb})`">
      <div class="wxjb-wrap">
        <h2 class="wxjb-title" data-sr-id="0" style="">無 限 進 步</h2>
        <p>我们不断发展和提升，超越现有的限制和成就，追求更高的目标。</p>
        <router-link to="/join-us" class="base-more">
          <i>加 入 我 们</i>
          <svg width="19" height="6" viewBox="0 0 19 6" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M0 5H16L12 1" stroke="white" stroke-width="2"></path>
          </svg>
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup lang="tsx">
import { onMounted, ref } from 'vue';
import { config } from '@src/config';
import { version } from '@/package.json';
import wxjb from '@assets/wxjb.png';
import { Swiper, SwiperSlide } from 'swiper/vue';
import { Pagination } from 'swiper/modules';
import MTB_promotional from '@assets/MTB_promotional.mp4';
import 'swiper/css';
import 'swiper/css/pagination';
import type { Swiper as SwiperInstance } from 'swiper';
import useFetch from '../utils/fetch';

const swiperModules = [Pagination];
const renderBullets = (index: number, className: string) => {
  const grooveId = 'swiperGroove_' + index;
  return `<span class="${className}"><div id="${grooveId}" class="groove"></div></span>`;
};
const defaultBanner = [
  {
    url: MTB_promotional,
    title: '团委学生会 媒体部',
    desc: '一个充满激情与想象力的部门',
    type: 'video',
  },
];
const bannerData = ref([...defaultBanner]);
const initHeight = ref(1080);
// 自动播放默认时长
const autoPlayDefaultDuration = 12000;
var animationFrameInstance: number;
var swiperGlobalIntstance: SwiperInstance;

const onSwiperInit = (swiper: SwiperInstance) => {
  swiperGlobalIntstance = swiper;
  countImageProgress(swiper);
};

const countImageProgress = (swiper?: SwiperInstance, el?: HTMLElement | undefined, progress = 0) => {
  // 由于swiper的activeIndex问题，所以使用realIndex
  const index = swiper?.realIndex;
  const item = bannerData.value[index];
  const progressBar = document.getElementById(`swiperGroove_${index}`) ?? el ?? undefined;
  if (!progressBar) {
    console.warn('progressBar is null', item, index);
    return;
  }
  if (item?.type === 'picture') {
    cancelAnimationFrame(animationFrameInstance);
    let startTime: number;
    const animate = (timestamp: number) => {
      if (!startTime) startTime = timestamp;
      const elapsed = timestamp - startTime;
      const progress = Math.min(elapsed / autoPlayDefaultDuration, 1);

      progressBar.style.width = `${progress * 100}%`;
      // console.log('progress', progress);

      if (progress < 1) {
        cancelAnimationFrame(animationFrameInstance);
        animationFrameInstance = requestAnimationFrame(animate);
      }

      if (progress === 1) {
        swiperToNext(swiper as SwiperInstance);
      }
    };
    progressBar.style.width = '0%';
    animationFrameInstance = requestAnimationFrame(animate);
  } else if (el && progress) {
    cancelAnimationFrame(animationFrameInstance);
    progressBar.style.width = `${progress * 100}%`;
  }
};

const onSwiperSlideChange = (swiper: SwiperInstance) => {
  swiperGlobalIntstance = swiper;
  cancelAnimationFrame(animationFrameInstance);
  // 由于swiper的activeIndex问题，所以使用realIndex
  const index = swiper?.realIndex;
  const previousRealIndex = swiper?.previousRealIndex ?? swiper?.previousIndex;
  if (previousRealIndex !== undefined) {
    const prevEl = document.getElementById(`swiperSource_${previousRealIndex}`) as HTMLVideoElement;
    if (prevEl?.tagName === 'VIDEO') {
      prevEl?.pause();
      prevEl.currentTime = 0;
    }
  }
  const item = bannerData.value[index];
  const element = document.getElementById(`swiperSource_${index}`) as HTMLVideoElement;
  if (item?.type === 'picture') {
    countImageProgress(swiper);
  } else if (item?.type === 'video') {
    element?.play();
  }
};

const onVideoStatrPlay = (e: Event) => {
  //重置视频播放进度
  const video = e?.target as HTMLVideoElement;
  video.currentTime = 0;
};

const onVideoPlaying = (e: Event) => {
  const video = e.target as HTMLVideoElement;
  const duration = video?.duration;
  const currentTime = video?.currentTime;
  const progress = currentTime / duration;
  const id = video?.id?.split('_')[1];
  const progressEl = document.getElementById(`swiperGroove_${id}`) as HTMLElement;
  countImageProgress(undefined, progressEl, progress);
};

const onVideoEnd = (e: Event) => {
  // 如果只有一项，则循环播放
  if (bannerData.value.length === 1) {
    (e.target as HTMLVideoElement).currentTime = 0;
    (e.target as HTMLVideoElement)?.play();
    return;
  }
  swiperToNext(swiperGlobalIntstance);
};

// 滑动下一个
const swiperToNext = (swiperInstance: SwiperInstance) => {
  swiperInstance.slideNext();
};

onMounted(() => {
  initHeight.value = window.innerHeight < 480 ? 680 : window.innerHeight;
  // var a =
  //   '[{"label":"诗词大会讲解视频收集","target":"_self","href":"/"},{"label":"德育资料收集","target":"_self","href":"/"},{"label":"共享网盘","target":"_self","href":"shareNetdisk","isRouter":true},{"label":"服务","type":"list","children":[{"label":"文件搜索（仅内部）","href":"//10.3.146.12:81/","target":"_self"},{"label":"速度测试","href":"speedtest","isRouter":true}]},{"label":"资源","type":"label","children":[{"title":"内部共享","children":[{"label":"成片库","href":"//10.3.146.11"},{"label":"媒体库","href":"//10.3.146.11"},{"label":"德育处资源库","href":"//10.3.146.11"}]},{"title":"外部资料","children":[{"label":"对外共享","href":"//10.3.146.11"}]}]},{"label":"系统","type":"list","children":[{"label":"媒体部OA","href":"//10.3.146.12/","target":"_blank"},{"label":"统一身份认证平台","href":"//10.3.146.13/","target":"_blank"},{"label":"直播系统","href":"//10.3.146.125:12800/","target":"_blank"}]},{"label":"加入我们","href":"","isRouter":true},{"label":"关于媒体部","href":"about","isRouter":true}]';
  // var b = JSON.parse(a);
  // var j = 1001;
  // const d = (h) => {
  //   for (var i = 0; i < h.length; i++) {
  //     h[i]['id'] = j;
  //     j++;
  //     if (h[i]?.children) {
  //       d(h[i].children);
  //     }
  //   }
  // };
  // d(b);
  // var g = JSON.stringify(b);
  // console.log(g);
  useFetch({
    url: '/getBanner',
    success: (res: any) => {
      const result = JSON.parse(res);
      if (result?.errcode !== 0) {
        console.error({ title: '获取Banner失败(Error)', content: `${result?.errcode}:${result?.errmsg}` });
        return;
      }
      const { data } = result;
      // banner not empty
      if (data?.length !== 0) {
        bannerData.value = data;
        return;
      }
      console.warn('Banner内容为空，使用默认值');
    },
    error: (desc: string, res: any) => {
      console.error(desc, res);
    },
  });
  // Console Group
  console.info(
    `%c MTB-Official %c Version: ${version} `,
    'background: #35495e; padding: 4px; border-radius: 3px 0 0 3px; color: #fff',
    'background: #41b883; padding: 4px; border-radius: 0 3px 3px 0; color: #fff',
  );
  console.info(
    `%c Copyright © Wesley %c MTB All Right Reserved %c`,
    `background: rgb(45, 140, 240);border:1px solid rgb(45, 140, 240); padding: 1px; border-radius: 4px 0 0 4px; color: #fff;`,
    `border:1px solid rgb(45, 140, 240); padding: 1px; border-radius: 0 4px 4px 0; color: rgb(45, 140, 240);`,
    'background:transparent',
  );
  // 招新Console
  if (config.RecruitConsole) {
    console.group(
      '%c恭喜你发现了媒体部技术组招新特别渠道！ (互联网班级、有编程经验 优先[不包括编程猫等软件])',
      'color: #1890ff',
    );
    console.info(
      '%c本站使用 Vite6+Vue3(TypeScript); 后端使用Python开发  本站使用Github作为代码管理 https://github.com/Wesley-0808/MTB-Official',
      'color: #1890ff',
    );
    console.info(
      '%c媒体部技术组长期招新！！！！如果你也对网络、编程有兴趣，想加入媒体部技术组，欢迎到我们部门找部长！！！（部门位置：办公楼一楼德育处 隔壁办公室）',
      'color: #07c160',
    );
    console.info('%c技术组很好玩的~~', 'color: rgb(255,152,0)');
    console.groupEnd();
    console.group('%c【技术组简介】', 'color: rgb(255,152,0)');
    console.info('%c1. 维护部门内网络、服务器正常运行，必要时需排查故障、解决问题。', 'font-weight: bold');
    console.info('%c2. 协调部门内工作，保障其他组正常工作。', 'font-weight: bold');
    console.info(
      '%c3. 校园活动后台，包含：灯光、音响、直播、场控等内容，保障活动正常进行，给予技术支持。',
      'font-weight: bold',
    );
    console.info('%c...', 'font-weight: bold');
    console.groupEnd();
  }
});
</script>

<style lang="scss">
// @media screen and (max-width: 960px) {
//   .video_banner .swiper-pagination {
//     width: 100% !important;
//     left: 60% !important;
//     bottom: 2.5rem !important;
//   }

//   .video_banner .other-bannerceter {
//     bottom: -7rem !important;
//     left: 10% !important;
//     transform: none !important;
//   }

//   .video_banner .other-bannerceter h2 {
//     font-size: 18px !important;
//     margin: -16px 0 22px !important;
//   }

//   .video_banner .other-bannerceter h3 {
//     font-size: 14px !important;
//   }
// }
.swiper-pagination-lock {
  display: block !important;
  .swiper-pagination-bullet:only-child {
    display: block !important;
  }
}
.video_banner {
  width: 100%;
  background: #040000;
  @keyframes swiper-fade {
    0% {
      transform: translateY(-10px);
      opacity: 0;
    }

    to {
      transform: translateY(0);
      opacity: 1;
    }
  }
  @keyframes Banner_progress {
    0% {
      width: 0px;
    }

    to {
      width: 100%;
    }
  }
  .swiper-slide {
    height: auto !important;
    overflow: hidden;
    &::after {
      content: '';
      position: absolute;
      width: 100%;
      height: 100%;
      left: 0;
      top: 0;
      z-index: 1;
      background: linear-gradient(180deg, rgb(255 255 255 / 0%) 30.34%, var(--td-mask-active));
    }
    video,
    img {
      width: 100%;
      height: 100%;
      object-fit: cover;
    }
    .other-bannerceter {
      position: absolute;
      bottom: 64px;
      width: 1200px;
      left: 50%;
      transform: translate(-50%);
      font-size: 16px;
      color: #fff;
      z-index: 2;
      h3 {
        height: 128px;
        font-size: 18px;
        position: relative;
        margin: 32px 0 24px;
        opacity: 0;
      }
      h2 {
        font-size: 48px;
        margin: 32px 0 24px;
        padding: 8px 0;
        opacity: 0;
      }
    }
    &.swiper-slide-active .other-bannerceter {
      h3 {
        animation: swiper-fade 0.5s 0.3s linear forwards;
      }
      h2 {
        animation: swiper-fade 0.8s 0.8s linear forwards;
      }
    }
  }
  .swiper-pagination {
    width: 1200px;
    left: 50%;
    transform: translate(-50%) !important;
    -webkit-transform: translateX(-50%) !important;
    bottom: 232px;
    text-align: left;
    .swiper-pagination-bullet {
      width: 13%;
      height: 3px;
      background-color: #ffffff4d;
      opacity: 1;
      border-radius: 0;
      margin: 0 10px 0 0 !important;
      position: relative;
      &.swiper-pagination-bullet-active > .groove {
        height: 100%;
        width: 0;
        position: absolute;
        left: 0;
        top: 0;
        background: #fff;
        z-index: 200;
      }
    }
  }
}

.wxjb {
  height: 525px;
  background-size: cover !important;
  background-repeat: no-repeat !important;
  background-position: 90% 50%;
  min-height: 400px;
  padding-top: 125px;
  position: relative;
  text-align: center;
  font-size: 16px;
  line-height: 30px;
  color: #333;
  &::after {
    content: '';
    position: absolute;
    width: 100%;
    height: 100%;
    left: 0;
    top: 0;
    z-index: 1;
    background-image: radial-gradient(transparent 2px, var(--td-mask-active) 2px);
    background-size: 5px 5px;
    -webkit-backdrop-filter: saturate(50%) blur(4px);
    backdrop-filter: saturate(50%) blur(4px);
    filter: brightness(0.78);
  }
  .wxjb-wrap {
    color: #fff;
    position: relative;
    z-index: 2;
    text-shadow: 0.125rem 0.125rem 2px black;
    padding: 0 32px;
    .wxjb-title {
      text-shadow: 3px 5px 2px black;
      font-weight: 700;
      font-size: 50px;
      margin-bottom: 38px;
      background-image: none;
      padding: 0;
      color: #fff;
    }
    .base-more {
      line-height: 54px;
      margin: 50px auto 0;
      display: block;
      font-size: 16px;
      color: #fff;
      text-align: center;
      transition: all 0.6s cubic-bezier(0.215, 0.61, 0.355, 1) 0s;
      position: relative;
      overflow: hidden;
      width: 160px;
      height: 54px;
      border: 2px solid rgba(255, 255, 255, 0.5);
      text-shadow: 0px 0px 20px black;
      &::before {
        content: ' ';
        display: block;
        position: absolute;
        right: 0;
        top: 0;
        width: 0;
        height: 100%;
        background: #1d70f2;
        z-index: 1;
        transition: all 0.4s;
      }
      &:hover {
        border: 2px solid #1d70f2;
        &:before {
          left: 0;
          width: 100%;
        }
        i {
          color: #fff;
          padding: 0 5px;
        }
      }
      i {
        position: relative;
        z-index: 2;
        transition: all 0.3s ease-out;
        -webkit-transition: all 0.3s ease-out;
        font-weight: 700;
      }
      svg {
        z-index: 2;
        position: relative;
        margin-left: 10px;
        margin-top: -5px;
        vertical-align: middle;
      }
    }
  }
}
</style>
