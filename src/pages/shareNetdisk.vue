<template>
  <div style="height: 56px"></div>
  <!---->
  <div class="top-menu">
    <!-- @change="changeHandler"  -->
    <!--menu-->
    <t-head-menu v-model="menuValue" theme="light" expand-type="popup" :onChange="ChangeMenu">
      <template #logo>
        <span class="menu__title" style="cursor: pointer" @click="showdialog = true">{{ menu_title }}</span>
      </template>
      <!--首页-->
      <t-menu-item value="index"> 首页 </t-menu-item>
      <!--服务-->
      <t-submenu value="services">
        <template #title>
          <span>服务 Services</span>
        </template>
        <t-menu-item value="services-1" href="http://10.3.146.103">设备借出面板</t-menu-item>
        <t-menu-item value="services-2" href="http://10.3.146.103/oa"
          >媒体部<span style="color: var(--td-success-color); font-size: 14px; margin-left: 2px">OA</span></t-menu-item
        >
        <t-menu-item value="services-3" href="./speedtest">速度测试</t-menu-item>
        <t-menu-item value="services-4" disabled>获取文件</t-menu-item>
      </t-submenu>
      <!--直播-->
      <t-submenu value="lives">
        <template #title>
          <span>直播 Lives</span>
        </template>
        <t-menu-item value="lives-1" :disabled="true">校园直播</t-menu-item>
        <t-menu-item value="lives-2" href="http://10.3.146.101:18000">直播管理后台</t-menu-item>
      </t-submenu>
      <!--数据存储-->
      <t-submenu value="storage" tag :popupProps="{ overlayClassName: 'MenuStoragePopupProps' }">
        <template #title>
          <span>数据存储 Storage</span>
        </template>
        <t-menu-item value="storage-1" href="http://10.3.146.102:81/film.php" target="_blank">成片库</t-menu-item>
        <t-menu-item value="storage-2" href="http://10.3.146.102:81/media-lib.php" target="_blank">媒体库</t-menu-item>
        <t-menu-item value="storage-3" href="http://10.3.146.102:81/movie.php" target="_blank">电影网盘</t-menu-item>
        <t-menu-item value="storage-4" href="http://192.168.67.12:81">
          <t-space size="small">
            文件搜索
            <t-tag size="small" theme="primary" variant="outline">v12</t-tag>
          </t-space>
        </t-menu-item>
        <t-menu-item value="storage-5" href="http://192.168.67.13:81">
          <t-space size="small">
            文件搜索
            <t-tag size="small" theme="success" variant="outline">v13</t-tag>
          </t-space>
        </t-menu-item>
      </t-submenu>
      <!--工具-->
      <t-submenu value="tools">
        <template #title>
          <span>工具 Tools</span>
        </template>
        <t-menu-item value="tools-1" :disabled="true">提词器</t-menu-item>
        <t-menu-item value="tools-2" :disabled="true">平台媒体解析</t-menu-item>
        <t-menu-item value="tools-3" :disabled="true">远端发声系统</t-menu-item>
      </t-submenu>
    </t-head-menu>
    <!--dialog-->
    <t-dialog
      v-model:visible="showdialog"
      :confirmBtn="null"
      :cancelBtn="null"
      :closeBtn="false"
      header="顺德中专团委媒体部 共享网盘"
      width="45%"
    >
      <template #body>
        <!--TagBadge-->
        <div style="margin-bottom: 16px">
          <t-space :size="small">
            <a href="https://nodejs.org/cn" target="_blank" title="后台服主框架">
              <img src="https://img.shields.io/badge/Node.JS-grey?style=for-the-badge&logo=node.js" />
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
            <a href="https://tdesign.tencent.com/" target="_blank">
              <img
                src="https://img.shields.io/badge/腾讯企业级设计体系-grey?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAiIGhlaWdodD0iNDAiIHZpZXdCb3g9IjAgMCA0MCA0MCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTE1LjAwNDEgMzcuMDAwMUg4LjUyODE2QzguNDIwODggMzcgOC4zMTQ4NyAzNi45NzY5IDguMjE3MjggMzYuOTMyNEM4LjExOTY5IDM2Ljg4NzkgOC4wMzI3OCAzNi44MjI5IDcuOTYyNCAzNi43NDE5QzcuODkyMDMgMzYuNjYxIDcuODM5ODMgMzYuNTY1OSA3LjgwOTMyIDM2LjQ2M0M3Ljc3ODgxIDM2LjM2MDIgNy43NzA3IDM2LjI1MiA3Ljc4NTUzIDM2LjE0NTdMOS4wNDcxOSAyOS4wMjI5SDE3LjAzMjRMMTUuNzMwOCAzNi40MDEzQzE1LjY5NjIgMzYuNTY5IDE1LjYwNTIgMzYuNzE5OSAxNS40NzMxIDM2LjgyODhDMTUuMzQwOSAzNi45Mzc4IDE1LjE3NTQgMzYuOTk4MiAxNS4wMDQxIDM3LjAwMDFaIiBmaWxsPSIjMDA5QkZGIi8+CjxwYXRoIGQ9Ik0zMy4yMzQxIDEyLjk4ODVIMTEuODY1N0wxMy4yNzExIDUuMDAzMzZIMzQuMzUyQzM0LjQ2NzQgNC45OTIzNCAzNC41ODM5IDUuMDA4NSAzNC42OTE5IDUuMDUwNTZDMzQuOCA1LjA5MjYyIDM0Ljg5NjcgNS4xNTk0IDM0Ljk3NDQgNS4yNDU1NkMzNS4wNTIgNS4zMzE3MiAzNS4xMDgzIDUuNDM0ODYgMzUuMTM4OSA1LjU0NjcyQzM1LjE2OTUgNS42NTg1OCAzNS4xNzM1IDUuNzc2MDUgMzUuMTUwNSA1Ljg4OTcyTDMzLjk2ODcgMTIuMzg5N0MzMy45MzY3IDEyLjU2MDIgMzMuODQ1NCAxMi43MTM4IDMzLjcxMDkgMTIuODIzNEMzMy41NzY0IDEyLjkzMyAzMy40MDc1IDEyLjk5MTUgMzMuMjM0MSAxMi45ODg1WiIgZmlsbD0idXJsKCNwYWludDBfbGluZWFyXzczNl8xMDUpIi8+CjxwYXRoIGQ9Ik0xMS44NjU4IDEyLjk4NzRINC43NTg5OUM0LjY1MDI2IDEyLjk4ODYgNC41NDI1NyAxMi45NjYyIDQuNDQzMzYgMTIuOTIxN0M0LjM0NDE2IDEyLjg3NzIgNC4yNTU4MSAxMi44MTE2IDQuMTg0NDIgMTIuNzI5NkM0LjExMzA0IDEyLjY0NzYgNC4wNjAzMiAxMi41NTEgNC4wMjk5MyAxMi40NDY3QzMuOTk5NTMgMTIuMzQyMyAzLjk5MjE4IDEyLjIzMjUgNC4wMDgzOCAxMi4xMjVMNS4xNjYyMyA1LjYxNzA2QzUuMTk3ODYgNS40NDUwMyA1LjI4ODU4IDUuMjg5NDUgNS40MjI3MSA1LjE3NzE5QzUuNTU2ODQgNS4wNjQ5MyA1LjcyNTk2IDUuMDAzMDMgNS45MDA4NyA1LjAwMjJIMTMuMjcxMkwxMS44NjU4IDEyLjk4NzRaIiBmaWxsPSIjMDA2NEZGIi8+CjxwYXRoIGQ9Ik0xNy4wNDAyIDI4Ljk5ODdIOS4wMzkwNkwxMS44NjU4IDEzLjAwNDRIMTkuODY3TDE3LjA0MDIgMjguOTk4N1oiIGZpbGw9InVybCgjcGFpbnQxX2xpbmVhcl83MzZfMTA1KSIvPgo8ZGVmcz4KPGxpbmVhckdyYWRpZW50IGlkPSJwYWludDBfbGluZWFyXzczNl8xMDUiIHgxPSIxMi41NTEiIHkxPSI5LjAwMzk0IiB4Mj0iMzMuODU5OCIgeTI9IjEyLjgzOTUiIGdyYWRpZW50VW5pdHM9InVzZXJTcGFjZU9uVXNlIj4KPHN0b3Agb2Zmc2V0PSIwLjAzIiBzdG9wLWNvbG9yPSIjRTlGRkZGIi8+CjxzdG9wIG9mZnNldD0iMC4xNyIgc3RvcC1jb2xvcj0iI0M0RkFDOSIvPgo8c3RvcCBvZmZzZXQ9IjAuMzMiIHN0b3AtY29sb3I9IiNBMEY2OTQiLz4KPHN0b3Agb2Zmc2V0PSIwLjQ4IiBzdG9wLWNvbG9yPSIjODJGMjY5Ii8+CjxzdG9wIG9mZnNldD0iMC42MyIgc3RvcC1jb2xvcj0iIzZBRUY0NyIvPgo8c3RvcCBvZmZzZXQ9IjAuNzYiIHN0b3AtY29sb3I9IiM1QUVEMkYiLz4KPHN0b3Agb2Zmc2V0PSIwLjg5IiBzdG9wLWNvbG9yPSIjNEZFQjIwIi8+CjxzdG9wIG9mZnNldD0iMSIgc3RvcC1jb2xvcj0iIzRDRUIxQiIvPgo8L2xpbmVhckdyYWRpZW50Pgo8bGluZWFyR3JhZGllbnQgaWQ9InBhaW50MV9saW5lYXJfNzM2XzEwNSIgeDE9IjE1Ljg1NjciIHkxPSIxMi40MjE1IiB4Mj0iMTYuMDA3OCIgeTI9IjI3LjQ3MDIiIGdyYWRpZW50VW5pdHM9InVzZXJTcGFjZU9uVXNlIj4KPHN0b3Agc3RvcC1jb2xvcj0iIzAwOUJGRiIvPgo8c3RvcCBvZmZzZXQ9IjAuMzUiIHN0b3AtY29sb3I9IiMwMDgxRkUiLz4KPHN0b3Agb2Zmc2V0PSIwLjc1IiBzdG9wLWNvbG9yPSIjMDA2QUZEIi8+CjxzdG9wIG9mZnNldD0iMSIgc3RvcC1jb2xvcj0iIzAwNjJGRCIvPgo8L2xpbmVhckdyYWRpZW50Pgo8L2RlZnM+Cjwvc3ZnPgo="
              />
            </a>
            <img src="https://img.shields.io/badge/Wesley-20B2AA?style=for-the-badge" />
          </t-space>
        </div>
        <!--bodyContent-->
        <t-space :size="160">
          <t-space :size="160">
            <!-- INFORMATION -->
            <t-space direction="vertical">
              <t-space size="small">
                版本<t-tag theme="success" variant="outline">{{ VERSION }}</t-tag>
              </t-space>
              <t-space size="small">
                内部版本<t-tag theme="warning" variant="outline">{{ BACKVERSION }}</t-tag>
              </t-space>
              <t-space size="small">
                构建版本<t-tag theme="success" variant="outline">{{ BUILDVERSION }}</t-tag>
              </t-space>
              <t-space size="small">
                启动模式<t-tag theme="primary" variant="outline">{{ DEBUG ? '开发模式' : '生产环境' }}</t-tag>
              </t-space>
            </t-space>
            <t-space direction="vertical">
              <t-space size="small">
                样式<t-tag theme="primary" variant="outline">{{
                  ThemeMode == 0
                    ? '跟随时间'
                    : ThemeMode == 1
                    ? '浅色模式'
                    : ThemeMode == 2
                    ? '深色模式'
                    : ThemeMode == 3
                    ? '跟随系统'
                    : '错误！'
                }}</t-tag
                ><t-button size="small" @click="ToggleTheme">切换</t-button>
              </t-space>
              <t-space size="small">
                更新日期<t-tag variant="outline">{{ CHANGETIME }}</t-tag>
              </t-space>
              <t-space size="small">
                构建日期<t-tag variant="outline">{{ BUILDDATA }}</t-tag>
              </t-space>
            </t-space>
          </t-space>
          <!-- CHANGELOG -->
          <t-space size="small" direction="vertical">
            <t-space size="small">
              缓存<t-button size="small" variant="outline" @click="CleanCache">清除缓存</t-button>
            </t-space>
          </t-space>
        </t-space>
      </template>
    </t-dialog>
  </div>
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
  <div class="breadcrumb" :class="{ width70p: styleClass.tableWidth }">
    <div style="display: flex; background: var(--breadcrumb-background-color); padding: 6px 8px; border-radius: 6px">
      <span>当前位置：</span>
      <t-breadcrumb :options="BreadcrumbOption" separator="/"></t-breadcrumb>
    </div>
  </div>
  <!---->
  <div class="fileList">
    <t-table
      row-key="epochmt"
      :class="{ width70p: styleClass.tableWidth }"
      :data="filelist"
      :columns="columns"
      empty="该文件夹为空"
      :hover="true"
      :onCellClick="handleColClick"
      :row-class-name="handleRowCursor"
    >
      <template #filename="{ row }" :sadf="row.isfolder == 1">
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
        <t-space size="small" v-if="row.isfolder == 0">
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
</template>
