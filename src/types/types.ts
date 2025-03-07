declare global {
  export interface FooterItem {
    label: string;
    target?: string;
    href?: string;
    isRouter?: boolean;
  }

  export interface FooterList {
    title: string;
    children: FooterItem[];
  }

  export type FooterData = FooterList[];
}
