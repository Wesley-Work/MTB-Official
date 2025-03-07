declare global {
  export interface FooterItem {
    label: string;
    target?: string;
    href?: string; // when isRouter is true, href is router path
    isRouter?: boolean;
    onlyPC: boolean;
    onlyMobile: boolean;
  }

  export interface FooterList {
    title: string;
    children: FooterItem[];
    onlyPC: boolean;
    onlyMobile: boolean;
  }

  export type FooterData = {
    links: FooterList[];
    list: FooterItem[];
  };
}
