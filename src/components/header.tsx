// src/components/Header.tsx
import { defineComponent, computed, ref, onMounted, onUnmounted, watch } from 'vue';
import type { PropType } from 'vue';
import useTheme from '@hooks/useTheme';
import useToppic from '@hooks/useToppic';
import useHeader from '@hooks/useHeader';
// import { getDevice } from '@utils/device';
import router from '@src/router';
import Toppic from './toppic';
import fhzsn_red from '@assets/fhzsn_red.png';
import fhzsn_white from '@assets/fhzsn_white.png';
import '@style/header.scss';

export default defineComponent({
  name: 'MTBHeader',
  props: {
    fixed: {
      type: Boolean as PropType<boolean>,
      default: false,
    },
    hiddenToppic: {
      type: Boolean as PropType<boolean>,
      default: false,
    },
    useCustomData: {
      type: Array<HeaderItem>,
      default: undefined,
    },
  },
  setup(props) {
    const { theme, toggleTheme } = useTheme();
    const { toppicInfo } = useToppic();
    const { headerList } = useHeader();
    // const { isMobile } = getDevice();
    const headerConfig = computed(() => {
      return props?.useCustomData ?? headerList.value;
    });
    const fixedHeader = ref(false);
    const scrollY = ref(0);
    const hasToppic = computed(() => !!toppicInfo.value);
    const hasToppic_TOP = computed(() => {
      const y = scrollY.value - 32;
      return hasToppic.value && !props?.hiddenToppic ? Math.max(0, Math.min(-y, 32)) : 0;
    });

    const isNormalTab = (type?: string) => type !== 'list' && type !== 'label';

    const handleScroll = () => {
      scrollY.value = window.scrollY;
      fixedHeader.value = scrollY.value > 32;
    };

    const clickToPath = (item: HeaderItem | HeaderItemChildren, path?: string) => {
      if (item?.callBack) {
        item?.callBack?.();
        return;
      }
      if (!path) {
        console.warn('路径为空');
        return;
      }
      router.push(path);
    };

    onMounted(() => window.addEventListener('scroll', handleScroll));
    onUnmounted(() => window.removeEventListener('scroll', handleScroll));

    watch(hasToppic, (newVal) => newVal && (scrollY.value = window.scrollY));

    return () => (
      <>
        {!props?.hiddenToppic ? <Toppic /> : null}
        <div
          class={[
            'mtb-header',
            'canT-Select',
            hasToppic.value && !props?.hiddenToppic && 'hasToppic',
            (props?.fixed || fixedHeader.value) && 'header-fixed',
          ]}
          style={{ top: `${hasToppic_TOP.value}px` }}
        >
          <div class="wrap">
            <div class="logo">
              <a style={{ width: '100%', height: '100%' }} href="/">
                <img alt="风华正少年" src={fhzsn_red} />
                <img alt="风华正少年" src={fhzsn_white} />
              </a>
            </div>

            <div class="nav">
              <ul class="subnav-ul">
                {headerConfig.value?.map((item, index) => (
                  <li
                    key={index}
                    class={['navView', item?.type === 'list' && 'dropdown', item?.type === 'label' && 'labelCard']}
                  >
                    <div class="navItem">
                      {isNormalTab(item?.type) ? (
                        <a
                          class={['isTabs', item.extraClass]}
                          target={!!item?.isRouter ? undefined : item.target}
                          href={!!item?.isRouter ? 'javascript:void(0)' : item.href}
                          onClick={() => clickToPath(item, item.href)}
                        >
                          <span>{item.label}</span>
                        </a>
                      ) : (
                        <span class="isTabs">{item.label}</span>
                      )}
                    </div>

                    {!isNormalTab(item.type) && (
                      <div
                        class={[
                          item.type === 'list' && 'navItem-type--list',
                          item.type === 'label' && 'navItem-type--label',
                        ]}
                      >
                        {item.type === 'list' && item.children && (
                          <ul>
                            {item.children.map((listItem, listIndex) => (
                              <li key={listIndex}>
                                <a
                                  class="nav-link"
                                  target={!!listItem?.isRouter ? undefined : listItem.target}
                                  href={!!listItem?.isRouter ? 'javascript:void(0)' : listItem.href}
                                  onClick={() => clickToPath(listItem, listItem.href)}
                                >
                                  {listItem.label}
                                </a>
                              </li>
                            ))}
                          </ul>
                        )}

                        {item.type === 'label' && item.children && (
                          <div>
                            {item.children.map((labelItem, labelIndex) => (
                              <div key={labelIndex} class="navItem-labelCard-item">
                                <h2>{labelItem.title || `项目${labelIndex + 1}`}</h2>
                                {labelItem?.children?.map((labelItemListEl, labelItemListIndex) => (
                                  <a
                                    key={labelItemListIndex}
                                    class="nav-link"
                                    target={!!labelItem?.isRouter ? undefined : labelItem.target}
                                    href={!!labelItem?.isRouter ? 'javascript:void(0)' : labelItem.href}
                                    onClick={() => clickToPath(labelItem, labelItem.href)}
                                  >
                                    {labelItemListEl?.label}
                                  </a>
                                ))}
                              </div>
                            ))}
                          </div>
                        )}
                      </div>
                    )}
                  </li>
                ))}
              </ul>
            </div>

            <div class="operation">
              <div class="themeChange" onClick={toggleTheme}>
                {theme.value === 'light' ? (
                  <div class="sun">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                      <path
                        d="M10.412 4.15761C6.75443 4.8942 4 8.12543 4 12C4 16.4183 7.58172 20 12 20C14.9602 20 17.5466 18.3918 18.9302 15.9997C13.9918 15.9622 10 11.9473 10 7C10 6.02085 10.1313 5.06315 10.412 4.15761ZM2 12C2 6.47715 6.47715 2 12 2H13.7337L12.8656 3.50069C12.2871 4.50091 12 5.68848 12 7C12 10.866 15.134 14 19 14C19.4618 14 19.9122 13.9554 20.3475 13.8706L22.0301 13.5428L21.4872 15.1689C20.1623 19.1373 16.4167 22 12 22C6.47715 22 2 17.5228 2 12Z"
                        fill="black"
                      />
                    </svg>
                  </div>
                ) : (
                  <div class="night">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                      <path
                        d="M13 1V4H11V1H13ZM20.4853 4.92848L18.364 7.0498L16.9497 5.63559L19.0711 3.51427L20.4853 4.92848ZM4.9289 3.51431L7.05022 5.63563L5.63601 7.04984L3.51469 4.92852L4.9289 3.51431ZM12 8C9.79086 8 8 9.79086 8 12C8 14.2091 9.79086 16 12 16C14.2091 16 16 14.2091 16 12C16 9.79086 14.2091 8 12 8ZM6 12C6 8.68629 8.68629 6 12 6C15.3137 6 18 8.68629 18 12C18 15.3137 15.3137 18 12 18C8.68629 18 6 15.3137 6 12ZM1 11H4V13H1V11ZM20 11H23V13H20V11ZM7.05024 18.3635L4.92892 20.4848L3.51471 19.0706L5.63603 16.9493L7.05024 18.3635ZM18.3639 16.9493L20.4852 19.0707L19.071 20.4849L16.9497 18.3636L18.3639 16.9493ZM13 20V23H11V20H13Z"
                        fill="black"
                      />
                    </svg>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      </>
    );
  },
});
