declare global {
  type CONFIG = {
    /**
     * 是否显示招新Console
     */
    RecruitConsole: boolean;
    /**
     * 是否使用View Transition API切换主题
     */
    useViewTransitionToggleTheme: boolean;
    OfficialAPI: string;
    ShareNetdiskAPI: string;
  };

  type ToppicInfo = {
    data: string;
    type: string;
  };

  interface HeaderItemChildren {
    title?: string; // only type=label
    label?: string;
    target?: string; // only type=list or is child
    href?: string; // only type=list or is child
    isRouter?: boolean; // only type=list or is child
    onlyPC?: boolean;
    onlyMobile?: boolean;
    bindParent: number;
    children?: Omit<HeaderItemChildren, 'children'>[];
    /**当CallBack存在时，无论是否为路由都只执行CallBack */
    callBack?: () => void;
  }

  interface HeaderItem {
    label: string;
    extraClass?: string;
    target?: string;
    href?: string;
    isRouter?: boolean;
    type?: 'list' | 'label';
    onlyPC?: boolean;
    onlyMobile?: boolean;
    bindParent: number;
    children?: HeaderItemChildren[];
    /**当CallBack存在时，无论是否为路由都只执行CallBack */
    callBack?: () => void;
  }

  type HeaderData = HeaderItem[];

  export interface FooterItem {
    label: string;
    target?: string;
    href?: string; // when isRouter is true, href is router path
    isRouter?: boolean;
    onlyPC?: boolean;
    onlyMobile?: boolean;
  }

  export interface FooterList {
    title: string;
    children?: FooterItem[];
    onlyPC?: boolean;
    onlyMobile?: boolean;
  }

  export type FooterData = {
    links: FooterList[];
    list: FooterItem[];
  };

  type DefaultConfig = {
    header: HeaderData;
    footer: FooterData;
  };
}
