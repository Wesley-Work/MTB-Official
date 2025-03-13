// import { NotifyPlugin } from 'tdesign-vue-next';
// import { config } from '@config/config';
import type { FetchOptions } from '../types/fetch';
import { getAPI } from './common';
function SpliceParameter(DATA: object | string | undefined) {
  if (Object.prototype.toString.call(DATA) !== '[object Object]') return false;
  // PASS
  const ParameterOBJ = [];
  for (const [key, value] of Object.entries(DATA as object)) {
    const keys = encodeURIComponent(key);
    const values = value === null ? '' : encodeURIComponent(value);
    ParameterOBJ.push(`${keys}=${values}`);
  }
  const ParameterSRT = ParameterOBJ.join('&');
  return ParameterSRT;
}

/**
 * 请求后端公共方法
 * @ 支持传入方法或Promise形式获取结果
 * @useFetch
 * @param option
 * @returns Promise
 * @example
 * useFetch({
 *  url: URL,
 *  methods: METHODS,
 *  header: object,
 *  data: object,
 *  success: function,
 *  error: function,
 *  complete: function,
 * })
 *
 */
export function useFetch(option: FetchOptions) {
  return new Promise<Boolean | string>(async (resolve, reject) => {
    try {
      function emitComplete(res: any) {
        if (option.complete && typeof option.complete === 'function') {
          option.complete(res);
        }
      }
      function emitError(et: any, res: any) {
        if (option.error && typeof option.error === 'function') {
          option.error(et, res);
        }
        console.error(et, res);
        emitComplete(res);
        reject(res);
      }
      function emitSuccess(res: any) {
        if (option.success && typeof option.success === 'function') {
          option.success(JSON.stringify(res));
        }
        emitComplete(JSON.stringify(res));
        resolve(JSON.stringify(res));
      }
      if (Object.prototype.toString.call(option) !== '[object Object]') resolve(false);

      // 优先header使用提供的内容 若没提供则使用默认值
      const headers = {
        'Content-Type':
          (option?.header as Record<string, string>)?.['Content-Type'] ??
          'application/x-www-form-urlencoded; charset=UTF-8',
      };
      const method = option?.methods?.toUpperCase() || 'GET';
      let finalUrl = option?.useCustomURL ? option?.url : getAPI() + option?.url;
      let bodyValue: string | null = null;

      if (method === 'GET' && option?.data) {
        const query = SpliceParameter(option.data);
        finalUrl += query ? `?${query}` : '';
      } else {
        bodyValue = SpliceParameter(option.data) || null;
      }
      // fetch 请求
      await fetch(finalUrl, {
        method: option?.methods ? option?.methods.toUpperCase() : 'GET',
        headers: {
          ...headers,
        },
        body: bodyValue,
      })
        .then((response) => {
          if (response.ok) {
            return response.json();
          } else {
            throw new Error('Network response was no well.');
          }
        })
        .then((data) => {
          emitSuccess(data);
        })
        .catch((err) => {
          emitError('RequestError', err);
        })
        .finally(() => {});
    } catch (e) {
      console.error('Fetch Module Error: ', e);
    }
  });
}

export default useFetch;
