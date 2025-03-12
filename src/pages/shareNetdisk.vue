<template>
  <div>
    <div style="height: 78px"></div>
    <!--header-->
    <MTBHeader :fixed="true" :hiddenToppic="true" :useCustomData="headerConfig" />
    <!---->
    <t-dialog
      v-model:visible="dialogVisible"
      :confirm-btn="null"
      :cancel-btn="null"
      :close-btn="false"
      header="顺德中专团委媒体部 共享网盘"
      width="45%"
    >
      <template #body>
        <!--TagBadge-->
        <div style="margin-bottom: 16px">
          <t-space size="small">
            <a href="https://tdesign.tencent.com/" target="_blank">
              <img
                src="https://img.shields.io/badge/腾讯企业级设计体系-grey?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAiIGhlaWdodD0iNDAiIHZpZXdCb3g9IjAgMCA0MCA0MCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTE1LjAwNDEgMzcuMDAwMUg4LjUyODE2QzguNDIwODggMzcgOC4zMTQ4NyAzNi45NzY5IDguMjE3MjggMzYuOTMyNEM4LjExOTY5IDM2Ljg4NzkgOC4wMzI3OCAzNi44MjI5IDcuOTYyNCAzNi43NDE5QzcuODkyMDMgMzYuNjYxIDcuODM5ODMgMzYuNTY1OSA3LjgwOTMyIDM2LjQ2M0M3Ljc3ODgxIDM2LjM2MDIgNy43NzA3IDM2LjI1MiA3Ljc4NTUzIDM2LjE0NTdMOS4wNDcxOSAyOS4wMjI5SDE3LjAzMjRMMTUuNzMwOCAzNi40MDEzQzE1LjY5NjIgMzYuNTY5IDE1LjYwNTIgMzYuNzE5OSAxNS40NzMxIDM2LjgyODhDMTUuMzQwOSAzNi45Mzc4IDE1LjE3NTQgMzYuOTk4MiAxNS4wMDQxIDM3LjAwMDFaIiBmaWxsPSIjMDA5QkZGIi8+CjxwYXRoIGQ9Ik0zMy4yMzQxIDEyLjk4ODVIMTEuODY1N0wxMy4yNzExIDUuMDAzMzZIMzQuMzUyQzM0LjQ2NzQgNC45OTIzNCAzNC41ODM5IDUuMDA4NSAzNC42OTE5IDUuMDUwNTZDMzQuOCA1LjA5MjYyIDM0Ljg5NjcgNS4xNTk0IDM0Ljk3NDQgNS4yNDU1NkMzNS4wNTIgNS4zMzE3MiAzNS4xMDgzIDUuNDM0ODYgMzUuMTM4OSA1LjU0NjcyQzM1LjE2OTUgNS42NTg1OCAzNS4xNzM1IDUuNzc2MDUgMzUuMTUwNSA1Ljg4OTcyTDMzLjk2ODcgMTIuMzg5N0MzMy45MzY3IDEyLjU2MDIgMzMuODQ1NCAxMi43MTM4IDMzLjcxMDkgMTIuODIzNEMzMy41NzY0IDEyLjkzMyAzMy40MDc1IDEyLjk5MTUgMzMuMjM0MSAxMi45ODg1WiIgZmlsbD0idXJsKCNwYWludDBfbGluZWFyXzczNl8xMDUpIi8+CjxwYXRoIGQ9Ik0xMS44NjU4IDEyLjk4NzRINC43NTg5OUM0LjY1MDI2IDEyLjk4ODYgNC41NDI1NyAxMi45NjYyIDQuNDQzMzYgMTIuOTIxN0M0LjM0NDE2IDEyLjg3NzIgNC4yNTU4MSAxMi44MTE2IDQuMTg0NDIgMTIuNzI5NkM0LjExMzA0IDEyLjY0NzYgNC4wNjAzMiAxMi41NTEgNC4wMjk5MyAxMi40NDY3QzMuOTk5NTMgMTIuMzQyMyAzLjk5MjE4IDEyLjIzMjUgNC4wMDgzOCAxMi4xMjVMNS4xNjYyMyA1LjYxNzA2QzUuMTk3ODYgNS40NDUwMyA1LjI4ODU4IDUuMjg5NDUgNS40MjI3MSA1LjE3NzE5QzUuNTU2ODQgNS4wNjQ5MyA1LjcyNTk2IDUuMDAzMDMgNS45MDA4NyA1LjAwMjJIMTMuMjcxMkwxMS44NjU4IDEyLjk4NzRaIiBmaWxsPSIjMDA2NEZGIi8+CjxwYXRoIGQ9Ik0xNy4wNDAyIDI4Ljk5ODdIOS4wMzkwNkwxMS44NjU4IDEzLjAwNDRIMTkuODY3TDE3LjA0MDIgMjguOTk4N1oiIGZpbGw9InVybCgjcGFpbnQxX2xpbmVhcl83MzZfMTA1KSIvPgo8ZGVmcz4KPGxpbmVhckdyYWRpZW50IGlkPSJwYWludDBfbGluZWFyXzczNl8xMDUiIHgxPSIxMi41NTEiIHkxPSI5LjAwMzk0IiB4Mj0iMzMuODU5OCIgeTI9IjEyLjgzOTUiIGdyYWRpZW50VW5pdHM9InVzZXJTcGFjZU9uVXNlIj4KPHN0b3Agb2Zmc2V0PSIwLjAzIiBzdG9wLWNvbG9yPSIjRTlGRkZGIi8+CjxzdG9wIG9mZnNldD0iMC4xNyIgc3RvcC1jb2xvcj0iI0M0RkFDOSIvPgo8c3RvcCBvZmZzZXQ9IjAuMzMiIHN0b3AtY29sb3I9IiNBMEY2OTQiLz4KPHN0b3Agb2Zmc2V0PSIwLjQ4IiBzdG9wLWNvbG9yPSIjODJGMjY5Ii8+CjxzdG9wIG9mZnNldD0iMC42MyIgc3RvcC1jb2xvcj0iIzZBRUY0NyIvPgo8c3RvcCBvZmZzZXQ9IjAuNzYiIHN0b3AtY29sb3I9IiM1QUVEMkYiLz4KPHN0b3Agb2Zmc2V0PSIwLjg5IiBzdG9wLWNvbG9yPSIjNEZFQjIwIi8+CjxzdG9wIG9mZnNldD0iMSIgc3RvcC1jb2xvcj0iIzRDRUIxQiIvPgo8L2xpbmVhckdyYWRpZW50Pgo8bGluZWFyR3JhZGllbnQgaWQ9InBhaW50MV9saW5lYXJfNzM2XzEwNSIgeDE9IjE1Ljg1NjciIHkxPSIxMi40MjE1IiB4Mj0iMTYuMDA3OCIgeTI9IjI3LjQ3MDIiIGdyYWRpZW50VW5pdHM9InVzZXJTcGFjZU9uVXNlIj4KPHN0b3Agc3RvcC1jb2xvcj0iIzAwOUJGRiIvPgo8c3RvcCBvZmZzZXQ9IjAuMzUiIHN0b3AtY29sb3I9IiMwMDgxRkUiLz4KPHN0b3Agb2Zmc2V0PSIwLjc1IiBzdG9wLWNvbG9yPSIjMDA2QUZEIi8+CjxzdG9wIG9mZnNldD0iMSIgc3RvcC1jb2xvcj0iIzAwNjJGRCIvPgo8L2xpbmVhckdyYWRpZW50Pgo8L2RlZnM+Cjwvc3ZnPgo="
              />
            </a>
            <a href="https://python.org/" target="_blank" title="API服务框架">
              <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=%23fff" />
            </a>
            <a href="https://cn.vuejs.org/" target="_blank" title="主体框架">
              <img src="https://img.shields.io/badge/Vue--Next-grey?style=for-the-badge&logo=vue.js" />
            </a>
            <a href="https://cn.vitejs.dev/guide/ssr.html" target="_blank" title="主要使用框架">
              <img src="https://img.shields.io/badge/Vite_SSR-646CFF?style=for-the-badge&logo=vite&logoColor=%23fff" />
            </a>
            <img src="https://img.shields.io/badge/Wesley-20B2AA?style=for-the-badge" />
          </t-space>
        </div>
        <!--bodyContent-->
      </template>
    </t-dialog>
    <!--取件码弹窗-->
    <t-dialog
      v-model:visible="pickUpCodeDialogVisible"
      :confirm-btn="null"
      :cancel-btn="null"
      header="使用『取件码』获取文件"
      width="40%"
    >
      <template #body>
        <div>
          <NumberInput
            v-model:value="pickUpCodeValue"
            :total="pickUpCodeItemTotal"
            :split="pickUpCodeSplit"
            :extra="pickUpCodeLastIsExtra"
          />
          <div>
            <t-button theme="primary" variant="outline" block size="large"> 查 询 </t-button>
          </div>
        </div>
      </template>
    </t-dialog>
    <!--temp-->
    <div style="width: 60%; margin: 24px auto">
      <div class="t-alert t-alert--info">
        <div class="t-alert__icon">
          <svg fill="none" viewBox="0 0 24 24" width="1em" height="1em" class="t-icon t-icon-info-circle-filled">
            <path
              fill="currentColor"
              d="M12 23a11 11 0 100-22 11 11 0 000 22zM11 8.5v-2h2v2h-2zm2 1.5v7.5h-2V10h2z"
            ></path>
          </svg>
        </div>
        <div class="t-alert__content">
          <div class="t-alert__message">
            <div class="t-alert__description">当前版本正在测试中，如遇Bug，欢迎您向我们</div>
            <div class="t-alert__operation">
              <span
                ><a
                  href="https://www.wenjuan.com/s/UZBZJv0ys7Q/"
                  target="_blank"
                  style="color: inherit; text-decoration: inherit"
                  >报告问题</a
                ></span
              >
            </div>
          </div>
        </div>
      </div>
    </div>
    <!-- <t-alert theme="error">高危操作/出错信息提示</t-alert> -->
    <!--temp-->
    <!---->
    <div class="breadcrumb">
      <div style="display: flex; background: var(--breadcrumb-background-color); padding: 6px 8px; border-radius: 6px">
        <span class="breadcrumb--title">当前位置：</span>
        <t-breadcrumb :options="breadCrumbOption" separator="/"></t-breadcrumb>
      </div>
    </div>
    <!---->
    <div class="fileList">
      <t-table
        row-key="epochmt"
        :data="fileList"
        :columns="tableColumns"
        empty="该文件夹为空"
        :hover="true"
        :on-cell-click="handleColClick"
        :row-class-name="handleRowCursor"
      >
        <template #filename="{ row }">
          <t-space size="small">
            <FolderOpen1Icon v-if="row.isfolder == 1" />
            <FileWordIcon v-else-if="row.suffix == 'doc' || row.suffix == 'docx'" />
            <VideoIcon
              v-else-if="
                row.suffix == 'mp4' ||
                row.suffix == 'avi' ||
                row.suffix == 'rmvb' ||
                row.suffix == 'mov' ||
                row.suffix == 'flv' ||
                row.suffix == 'mkv' ||
                row.suffix == 'mpg' ||
                row.suffix == 'mpge'
              "
            />
            <FileImageIcon
              v-else-if="
                row.suffix == 'png' ||
                row.suffix == 'jpg' ||
                row.suffix == 'jpeg' ||
                row.suffix == 'svg' ||
                row.suffix == 'gif' ||
                row.suffix == 'tiff' ||
                row.suffix == 'bmp'
              "
            />
            <FileCode1Icon
              v-else-if="
                row.suffix == 'vue' ||
                row.suffix == 'js' ||
                row.suffix == 'css' ||
                row.suffix == 'html' ||
                row.suffix == 'json' ||
                row.suffix == 'py' ||
                row.suffix == 'ts'
              "
            />
            <FilePdfIcon v-else-if="row.suffix == 'pdf'" />
            <FileZipIcon
              v-else-if="
                row.suffix == 'zip' ||
                row.suffix == 'rar' ||
                row.suffix == '7z' ||
                row.suffix == 'tag.gz' ||
                row.suffix == 'gz' ||
                row.suffix == 'bz2'
              "
            />
            <FilePowerpointIcon v-else-if="row.suffix == 'pptx' || row.suffix == 'ppt'" />
            <FileExcelIcon v-else-if="row.suffix == 'xlsx' || row.suffix == 'xls'" />
            <FileIcon v-else />
            {{ row.filename }}
          </t-space>
        </template>
        <template #operation="{ row }">
          <!-- <span>{{ row }}</span> -->
          <t-space v-if="row.isfolder == 0" size="small">
            <t-button variant="dashed" ghost @click.end="handleCopyFileDownloadUrl(row)">
              <fileCopyIcon />
            </t-button>
            <t-button variant="dashed" theme="primary" ghost @click.end="handleFileDownload(row)">
              <DownloadIcon />
            </t-button>
          </t-space>
        </template>
      </t-table>
    </div>
    <!---->
    <WesleyFooter />
  </div>
</template>

<script setup lang="tsx">
import { ref, defineComponent } from 'vue';
import useClipboard from 'vue-clipboard3';
import { useRouter } from 'vue-router';
import MTBHeader from '@components/header';
import WesleyFooter from '@components/wesley_footer';
import NumberInput from '@components/numberInput';
import {
  FolderOpen1Icon,
  FileWordIcon,
  FileExcelIcon,
  FileZipIcon,
  FilePdfIcon,
  FileCode1Icon,
  FileIcon,
  FileImageIcon,
  VideoIcon,
  DownloadIcon,
  FileCopyIcon,
} from 'tdesign-icons-vue-next';

const router = useRouter();
const { toClipboard } = useClipboard();
const headerConfig: HeaderData = [
  {
    label: '返回 官网',
    href: '/',
    isRouter: true,
  },
  {
    label: '『取件码』取件',
    callBack: () => {
      pickUpCodeDialogVisible.value = true;
    },
  },
  {
    label: '问题反馈',
    href: 'https://wj.qq.com/s2/14786781/3fb8/',
    target: '_blank',
  },
  {
    label: 'Github Repository',
    href: 'https://github.com/Wesley-0808/MTB-Official/',
    target: '_blank',
  },
];
const dialogVisible = ref(false);
const pickUpCodeDialogVisible = ref(false);
const pickUpCodeItemTotal = ref(8);
const pickUpCodeValue = ref('');
// 从后往前数，几项为额外项
const pickUpCodeLastIsExtra = ref(2);
// 以几项进行分隔
const pickUpCodeSplit = ref(3);
const fileList = ref([]);
const menuValue = ref('index');
const breadCrumbOption = ref([{ content: '首页', href: '/' }]);
const tableColumns = [
  {
    colKey: 'filename',
    title: '文件名',
    width: 300,
  },
  {
    colKey: 'mt',
    title: '修改时间',
    width: 170,
    ellipsis: true,
  },
  {
    colKey: 'filesize',
    title: '文件大小',
    width: 120,
    cell: (h, { col, row }) => {
      const { isfolder } = row;
      if (isfolder != 1) {
        const { filesize } = row;
        const kb = filesize / 1024;
        const mb = kb / 1024;
        const gb = mb / 1024;
        let unit = 'KB';
        if (kb >= 1024 && mb < 1024) {
          unit = 'MB';
          return <span>{`${mb.toFixed(2)} ${unit}`}</span>;
        }
        if (mb >= 1024) {
          unit = 'GB';
          return <span>{`${gb.toFixed(2)} ${unit}`}</span>;
        }
        return <span>{`${kb.toFixed(2)} ${unit}`}</span>;
      }
      return <span>-</span>;
    },
  },
  {
    colKey: 'operation',
    title: '操作',
    width: 150,
  },
];
const updateBreadCrumb = () => {
  const { search } = location;
  var searchParams = new URLSearchParams(search);
  var path = searchParams.get('dir');
  if (!path) {
    path = '/';
  }
  // 因为目录是/xxx/xxx/xxx这样的，所以要slice(1)去掉第一项
  var item;
  try {
    item = path.split('/').slice(1);
  } catch {
    item = [path];
  }
  var BCO = this.$data.BreadcrumbOption;
  // 遍历地址栏
  for (const key in item) {
    if (Object.hasOwnProperty.call(item, key)) {
      const element = item[key];
      var name = [];
      var targetURL;
      // 非第一项
      if (key != 0) {
        for (let index = 0; index <= key; index++) {
          const element = item[index];
          name.push(element);
        }
        targetURL = name.join('/');
      } else {
        targetURL = element;
      }
      const BCitem = { content: element, href: `/?dir=/${targetURL}` };
      BCO.push(BCitem);
    }
  }
};
const fetchFileList = () => {
  console.warn('Server无法获取文件列表，尝试获取文件列表');
  // const { search } = location;
  // var searchParams = new URLSearchParams(search);
  // var path = searchParams.get('dir');
  // console.log(path);
  // axios.post('http://10.3.146.100:9090/getFileList', { path: path }).then((res) => {
  //   console.log(res);
  //   if (res.data.errcode == 0) {
  //     this.$data.filelist = res.data.data.filelist;
  //   } else {
  //     if (res.data.errcode == -404) {
  //       this.$data.loaded = false;
  //       this.$data.notfound = true;
  //     } else {
  //       this.$notify.error({ title: '获取文件列表失败', content: `${res.data.errcode}:${res.data.errmsg}` });
  //     }
  //   }
  //   console.log(this.$data.filelist);
  // });
};

// 表格行按下
const handleColClick = (e) => {
  if (e.colIndex != 0) return;
  if (e.row.isfolder == 0) return;
  // this.$store.dispatch('appendPath', `${e.row.filename}`)
  const { search } = location;
  var searchParams = new URLSearchParams(search);
  var path = searchParams.get('dir');
  if (!path) {
    path = '/';
  }
  try {
    path.split('/').slice(1);
  } catch {
    NEWUrl = replaceUrlParam(location.href, 'dir', `/${e.row.filename}`);
    location.href = NEWUrl;
  }
  var item = path.split('/').slice(1);
  if (item.length == 1) {
    item = [];
  }
  var NEWUrl;
  if (item.length == 1) {
    NEWUrl = replaceUrlParam(location.href, 'dir', `${path}/${e.row.filename}`);
  } else {
    NEWUrl = replaceUrlParam(location.href, 'dir', `/${e.row.filename}`);
  }
  location.href = NEWUrl;
};
// 文件夹列鼠标指针
const handleRowCursor = (e) => {
  if (e.row.isfolder == 1) {
    return 'Isfloder';
  }
  // return {
  //     rowIndex: 0,
  //     row: e.row,
  //     type: 'body',
  // }
};
// 替换浏览器参数
const replaceUrlParam = (url, key, value) => {
  if (url.indexOf(key) > -1) {
    let reg = new RegExp(`((?=${key}=).*?(?=&))|((?=${key}=).*)`);
    url = url.replace(reg, `${key}=${value}`);
  } else {
    let join = url.indexOf('?') > -1 ? '&' : '?';
    url += `${join}${key}=${value}`;
  }
  return url;
};
// 复制下载链接
const handleCopyFileDownloadUrl = (fileEx) => {
  const { download_url } = fileEx;
  try {
    toClipboard(download_url);
    // this.$message.success('复制成功');
  } catch (e) {
    console.info(e);
    // this.$message.error('复制失败！');
  }
};
// 点击下载
const handleFileDownload = (fileEx) => {
  const { download_url } = fileEx;
  var a = document.createElement('a');
  a.href = download_url;
  a.download = fileEx.name;
  a.click();
  const content = () => {
    return (
      <div>
        <span>已自动开始下载，如未开始请点击</span>
        <a
          class="t-link t-link--theme-primary t-link--hover-color"
          style="padding: 0 3px"
          href={download_url}
          download={fileEx.name}
        >
          这里
        </a>
        <span>重试</span>
      </div>
    );
  };
  // this.$message.success({ content: content });
};

const ChangeMenu = (e) => {
  menuValue.value = 'index';
};
/**
 * @GetDateString
 * @获取当前时间 yyyy-mm-dd hh:mm:ss
 * @return {String}
 */
const GetDateString = () => {
  var Dates = new Date();
  return Dates.toLocaleString().replaceAll('/', '-');
};

const filenamePrefix = [];
const HandleFileName = (row) => {};
</script>

<script lang="tsx">
export default defineComponent({
  name: 'MTBShareNetdisk',
});
</script>

<style lang="scss">
:root {
  --breadcrumb-background-color: var(--td-gray-color-4);
  --ripple-color: rgba(0, 0, 0, 0.35);
}

:root[theme-mode='dark'] {
  --breadcrumb-background-color: var(--td-gray-color-12);
  --ripple-color: rgb(75, 75, 75);
}

.t-menu__operations {
  .t-button {
    margin-left: 8px;
  }
}

.t-head-menu .t-menu {
  justify-content: flex-end !important;
  padding-right: 12px;
}

.top-menu {
  position: fixed;
  top: 0px;
  left: 0px;
  width: 100%;
  z-index: 90;

  > div {
    padding-left: 36px;
    padding-right: 24px;

    .menu__title {
      font-size: 20px;
      font-weight: bold;
      letter-spacing: 0.3px;
    }
  }
}

.MenuStoragePopupProps {
  margin-left: 16px !important;
}

.breadcrumb {
  display: flex;
  flex-direction: row;
  margin: 16px auto !important;
}

.breadcrumb,
.fileList {
  width: 60%;
  margin: 0 auto;
  transition: all 0.28s cubic-bezier(0.645, 0.045, 0.355, 1);
}

.breadcrumb.width70p,
.fileList:has(.width70p) {
  width: 70%;
  margin: 0 auto;
}

.fileList {
  box-shadow: 0 3px 1px -2px rgba(0, 0, 0, 0.2), 0 2px 2px 0 rgba(0, 0, 0, 0.14), 0 1px 5px 0 rgba(0, 0, 0, 0.12);

  .t-table td {
    padding: 14px var(--td-comp-paddingLR-l);
    line-height: var(--td-line-height-body-large);
    font-size: 14px;
  }

  .t-button.t-button--variant-dashed.t-button--theme-default.t-button--ghost {
    color: var(--td-text-color-primary);
    border-color: var(--td-text-color-primary);
  }

  .t-button--ghost {
    --ripple-color: var(--ripple-color);
  }

  .t-button--variant-dashed.t-button--ghost:hover,
  .t-button--variant-dashed.t-button--ghost:focus-visible {
    color: var(--td-brand-color-hover) !important;
    border-color: var(--td-brand-color-hover) !important;
  }

  .t-button--variant-dashed {
    height: 28px;
  }

  .Isfloder > td:first-child {
    cursor: pointer;
  }
}

.t-message__list {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.breadcrumb--title {
  display: flex;
  align-items: center;
  color: var(--td-text-color-primary);
}
</style>
