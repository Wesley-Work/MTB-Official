import { useFetch } from '@utils/fetch';

export function fetchData(
  usePromise?: boolean,
  option?: { successCallback: (_e: any) => {}; failCallback: (_e: any) => {}; completeCallback: (_e: any) => {} },
): Promise<any> | any {
  const normalRequest = () => {
    useFetch({
      url: '/netdisk/getFileList',
      methods: 'GET',
      success: option?.successCallback,
      error: option?.failCallback,
      complete: option?.completeCallback,
    });
  };
  const PromiseRequest = () => {
    return new Promise((resolve, reject) => {
      useFetch({
        url: '/netdisk/getFileList',
        methods: 'GET',
        success: (res: any) => {
          option?.successCallback?.(res);
          resolve(res);
        },
        error: (res: any) => {
          option?.failCallback?.(res);
          reject(res);
        },
        complete: (res: any) => {
          option?.completeCallback?.(res);
        },
      });
    });
  };
  return usePromise ? PromiseRequest() : normalRequest();
}
