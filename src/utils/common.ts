/**
 * 判断是否为内网[简单判断]
 */
export const isInternet = () => {
  const url = location.href;
  // 只判断146是因为服务部署于146段
  return (
    url.includes('10.3.146') ||
    url.includes('192.168.67') ||
    url.includes('mtb.sdzz.net') ||
    url.includes('internet-mtb.sdzz.wesley.net.cn')
  );
};

/**
 * 判断是否为在媒体部内[简单判断]
 */
export const isMTBInternet = () => {
  const url = location.href;
  return (
    url.includes('192.168.67') ||
    url.includes('mtb.sdzz.net') ||
    url.includes('internet-mtb.wesley.net.cn') ||
    url.includes('localhost')
  );
};

export const getAPI = () => {
  return isMTBInternet() ? 'http://192.168.67.14/api' : 'http://10.3.146.11/api';
};

export const countFileSize = (fileSize: number) => {
  const kb = fileSize / 1024;
  const mb = kb / 1024;
  const gb = mb / 1024;
  let unit = 'Byte';
  let size = fileSize === 0 ? 0 : fileSize.toFixed(2);
  if (fileSize > 1024) {
    size = kb.toFixed(2);
    unit = 'KB';
  }
  if (kb >= 1024 && mb < 1024) {
    unit = 'MB';
    size = mb.toFixed(2);
  }
  if (mb >= 1024) {
    unit = 'GB';
    size = gb.toFixed(2);
  }
  return {
    size,
    unit,
  };
};

export const fileIsImage = (filename: string) => {
  const fileSuffixs = filename.split('.');
  const suffix = fileSuffixs[fileSuffixs.length - 1];
  return (
    suffix.includes('png') ||
    suffix.includes('jpg') ||
    suffix.includes('jpeg') ||
    suffix.includes('svg') ||
    suffix.includes('gif') ||
    suffix.includes('tiff') ||
    suffix.includes('bmp')
  );
};

export const fileIsVideo = (filename: string) => {
  const fileSuffixs = filename.split('.');
  const suffix = fileSuffixs[fileSuffixs.length - 1];
  return (
    suffix.includes('mp4') ||
    suffix.includes('avi') ||
    suffix.includes('rmvb') ||
    suffix.includes('mov') ||
    suffix.includes('flv') ||
    suffix.includes('mkv') ||
    suffix.includes('mpg') ||
    suffix.includes('mpge')
  );
};

export const fileIsZip = (filename: string) => {
  const fileSuffixs = filename.split('.');
  const suffix = fileSuffixs[fileSuffixs.length - 1];
  return (
    suffix.includes('zip') ||
    suffix.includes('rar') ||
    suffix.includes('7z') ||
    suffix.includes('tag.gz') ||
    suffix.includes('gz') ||
    suffix.includes('bz2')
  );
};

export const fileIsPdf = (filename: string) => {
  const fileSuffixs = filename.split('.');
  const suffix = fileSuffixs[fileSuffixs.length - 1];
  return suffix.includes('pdf');
};

export const fileIsPpt = (filename: string) => {
  const fileSuffixs = filename.split('.');
  const suffix = fileSuffixs[fileSuffixs.length - 1];
  return suffix.includes('pptx') || suffix.includes('ppt');
};

export const fileIsXls = (filename: string) => {
  const fileSuffixs = filename.split('.');
  const suffix = fileSuffixs[fileSuffixs.length - 1];
  return suffix.includes('xlsx') || suffix.includes('xls');
};

export const fileIsCode = (filename: string) => {
  const fileSuffixs = filename.split('.');
  const suffix = fileSuffixs[fileSuffixs.length - 1];
  return (
    suffix.includes('vue') ||
    suffix.includes('js') ||
    suffix.includes('css') ||
    suffix.includes('html') ||
    suffix.includes('json') ||
    suffix.includes('py') ||
    suffix.includes('ts')
  );
};

export const fileIsDoc = (filename: string) => {
  const fileSuffixs = filename.split('.');
  const suffix = fileSuffixs[fileSuffixs.length - 1];
  return suffix.includes('doc') || suffix.includes('docx');
};
