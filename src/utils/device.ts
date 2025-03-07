// 获取设备类型
export function getDevice() {
  const ua = navigator.userAgent;
  const isAndroid = /(Android);?[\s\/]+([\d.]+)?/.test(ua);
  const isIOS = /(iPad|iPhone|iPod)(?:.*OS\s([\d_]+))?/.test(ua);
  const isMobile = isAndroid || isIOS || ua.includes('windows phone');
  return {
    isAndroid,
    isIOS,
    isPC: !isMobile,
    isMobile,
  };
}
